"""Private pending uploads, normalized JPEGs and explicit moderator decisions."""
import base64
import binascii
import hashlib
from io import BytesIO
import os
import re
import secrets
import time
import warnings
from accounts import AccountError
from submissions import exists

MAX_IMAGE=240000
def initialize(store,postgres=False):
    binary='BYTEA' if postgres else 'BLOB'
    with store.connect() as db:
        db.execute(f'''CREATE TABLE IF NOT EXISTS route_photos (
            id TEXT PRIMARY KEY,route_id TEXT NOT NULL,user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            caption TEXT NOT NULL,image {binary} NOT NULL,digest TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',reason TEXT NOT NULL DEFAULT '',created_at BIGINT NOT NULL,
            reviewed_by BIGINT,reviewed_at BIGINT,UNIQUE(route_id,user_id,digest))''')
        db.execute('CREATE INDEX IF NOT EXISTS route_photos_status ON route_photos(status,route_id,created_at)')

def moderator(user):
    ids={int(value) for value in os.environ.get('ATLAS_MODERATOR_IDS','').split(',') if value.strip().isdigit()}
    return bool(user and user['id'] in ids)

def normalize(encoded):
    from PIL import Image,ImageOps,UnidentifiedImageError
    if not isinstance(encoded,str) or len(encoded)>1000000:raise AccountError(413,'图片数据过大，请压缩后再试。')
    try:raw=base64.b64decode(encoded,validate=True)
    except (binascii.Error,ValueError):raise AccountError(400,'图片编码不正确。') from None
    if not raw or len(raw)>750000:raise AccountError(413,'图片为空或过大。')
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('error',Image.DecompressionBombWarning)
            with Image.open(BytesIO(raw)) as original:
                if original.format not in ['JPEG','PNG','WEBP'] or getattr(original,'n_frames',1)!=1:raise AccountError(400,'仅支持静态 JPEG、PNG、WebP 照片。')
                if original.width<64 or original.height<64 or original.width*original.height>4000000:raise AccountError(400,'图片尺寸需至少 64×64，压缩后不超过 400 万像素。')
                original.load();image=ImageOps.exif_transpose(original).convert('RGB')
                image.thumbnail((1600,1600))
                output=BytesIO();image.save(output,'JPEG',quality=80,optimize=True)
                if output.tell()>MAX_IMAGE:
                    image.thumbnail((1100,1100));output=BytesIO();image.save(output,'JPEG',quality=65,optimize=True)
                if output.tell()>MAX_IMAGE:raise AccountError(413,'压缩后图片仍过大，请选择更小的照片。')
                return output.getvalue()
    except AccountError:raise
    except (UnidentifiedImageError,OSError,ValueError,Image.DecompressionBombError,Image.DecompressionBombWarning):raise AccountError(400,'图片无法安全解码，请选择有效照片。') from None

def upload(store,route,user,data):
    if not user:raise AccountError(401,'登录后即可上传线路照片。')
    if data.get('userId')!=user['id']:raise AccountError(409,'账号已切换，请重新打开上传窗口。')
    if not exists(store,route):raise AccountError(404,'线路不存在。')
    caption=data.get('caption')
    if not isinstance(caption,str) or not 2<=len(caption.strip())<=200:raise AccountError(400,'请填写 2–200 字的照片说明。')
    if data.get('rightsConfirmed') is not True:raise AccountError(400,'请确认有权公开这张线路照片。')
    store.rate_limit('photo-upload:'+str(user['id']),limit=5)
    image=normalize(data.get('image'));digest=hashlib.sha256(image).hexdigest();rid=secrets.token_hex(16)
    with store.connect() as db:
        if isinstance(store.database,str):db.execute('SELECT pg_advisory_xact_lock(73910486)')
        else:db.execute('BEGIN IMMEDIATE')
        if db.execute('SELECT 1 FROM route_photos WHERE route_id=? AND user_id=? AND digest=?',(route,user['id'],digest)).fetchone():raise AccountError(409,'这张照片已提交过。')
        if db.execute("SELECT COUNT(*) AS count FROM route_photos WHERE user_id=? AND status='pending'",(user['id'],)).fetchone()['count']>=10:raise AccountError(429,'最多保留 10 张待审核照片，请等待处理。')
        if db.execute('SELECT COALESCE(SUM(LENGTH(image)),0) AS size FROM route_photos').fetchone()['size']+len(image)>50000000:raise AccountError(507,'相册存储额度已满，请联系管理员。')
        db.execute('INSERT INTO route_photos (id,route_id,user_id,caption,image,digest,created_at) VALUES (?,?,?,?,?,?,?)',(rid,route,user['id'],caption.strip(),image,digest,int(time.time())))
    return {'id':rid,'status':'pending','message':'基础文件检查通过，照片等待人工审核；通过后才公开。'}

def listing(store,route,user=None,before=None):
    if not exists(store,route):raise AccountError(404,'线路不存在。')
    stamp,rid=photo_cursor(before)
    with store.connect() as db:
        rows=db.execute("SELECT route_photos.id,caption,route_photos.created_at,username,user_id FROM route_photos JOIN users ON users.id=user_id WHERE route_id=? AND status='approved' AND (route_photos.created_at<? OR (route_photos.created_at=? AND route_photos.id<?)) ORDER BY route_photos.created_at DESC,route_photos.id DESC LIMIT 51",(route,stamp,stamp,rid)).fetchall()
        own=db.execute('SELECT id,caption,status,reason,created_at FROM route_photos WHERE route_id=? AND user_id=? ORDER BY created_at DESC LIMIT 30',(route,user['id'])).fetchall() if user else []
    return {'photos':[dict(row) for row in rows[:50]],'next':str(rows[49]['created_at'])+':'+rows[49]['id'] if len(rows)>50 else None,'mine':[dict(row) for row in own],'canModerate':moderator(user)}

def photo_cursor(before):
    if before is None:return 9223372036854775807,'z'
    if not isinstance(before,str) or not re.fullmatch(r'[0-9]{1,19}:[a-f0-9]{32}',before):raise AccountError(400,'分页参数不正确。')
    stamp,rid=before.split(':')
    if not 0<int(stamp)<=9223372036854775807:raise AccountError(400,'分页参数不正确。')
    return int(stamp),rid

def image_data(store,rid,user):
    with store.connect() as db:row=db.execute('SELECT image,status,user_id FROM route_photos WHERE id=?',(rid,)).fetchone()
    if not row or (row['status']!='approved' and not(user and (user['id']==row['user_id'] or moderator(user)))):raise AccountError(404,'照片不存在或尚未公开。')
    return bytes(row['image'])

def queue(store,user,status='pending'):
    if not moderator(user):raise AccountError(403,'只有照片审核员可以查看审核队列。')
    if status not in ['pending','approved']:raise AccountError(400,'审核列表类型不正确。')
    with store.connect() as db:rows=db.execute("SELECT route_photos.id,route_id,caption,route_photos.created_at,username,user_id,status FROM route_photos JOIN users ON users.id=user_id WHERE status=? ORDER BY route_photos.created_at,route_photos.id LIMIT 50",(status,)).fetchall()
    return {'photos':[dict(row) for row in rows]}

def review(store,rid,user,data):
    if not moderator(user):raise AccountError(403,'只有照片审核员可以审核。')
    if data.get('userId')!=user['id']:raise AccountError(409,'账号已切换。')
    decision=data.get('decision');reason=data.get('reason','')
    if decision not in ['approved','rejected'] or not isinstance(reason,str) or len(reason)>400:raise AccountError(400,'审核决定或原因不正确。')
    if decision=='rejected' and not reason.strip():raise AccountError(400,'拒绝时请填写原因。')
    with store.connect() as db:
        row=db.execute('SELECT user_id,status FROM route_photos WHERE id=?',(rid,)).fetchone()
        if not row:raise AccountError(404,'照片不存在。')
        expected=data.get('expectedStatus','pending')
        if expected not in ['pending','approved'] or row['status']!=expected:raise AccountError(409,'这张照片已处理，请刷新队列。')
        cursor=db.execute("UPDATE route_photos SET status=?,reason=?,reviewed_by=?,reviewed_at=? WHERE id=? AND status=?",(decision,reason.strip(),user['id'],int(time.time()),rid,expected))
        if cursor.rowcount!=1:raise AccountError(409,'这张照片已被其他审核员处理。')
    return {'id':rid,'status':decision}
