"""Route-scoped community comments shared by SQLite and PostgreSQL."""
import re
import time
from pathlib import Path
from accounts import AccountError

ROOT=Path(__file__).resolve().parent
ROUTES=set()
for name in ['trails.js','china-trails.js']:
    ROUTES.update(re.findall(r'''["']?\bid["']?\s*:\s*["']([a-z0-9-]+)["']''',(ROOT/'web'/name).read_text(encoding='utf-8')))
CATEGORIES={'experience','conditions','gear','question'}

def initialize(store,postgres=False):
    identity='BIGSERIAL PRIMARY KEY' if postgres else 'INTEGER PRIMARY KEY'
    with store.connect() as db:
        db.execute(f'''CREATE TABLE IF NOT EXISTS comments (
            id {identity}, route_id TEXT NOT NULL,
            user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            category TEXT NOT NULL, content TEXT NOT NULL,
            created_at BIGINT NOT NULL
        )''')
        db.execute('CREATE INDEX IF NOT EXISTS comments_route_id ON comments(route_id,id)')

def discuss(store,route,user=None,data=None,before=None):
    from submissions import exists
    if not exists(store,route):raise AccountError(404,'线路不存在。')
    if data is not None:
        if not user:raise AccountError(401,'登录后即可分享经验。')
        if data.get('userId')!=user['id']:raise AccountError(409,'账号已切换，请刷新后重试。')
        content=data.get('content');category=data.get('category','experience')
        if not isinstance(category,str) or category not in CATEGORIES:raise AccountError(400,'请选择有效的讨论类型。')
        if not isinstance(content,str) or not 2<=len(content.strip())<=2000:raise AccountError(400,'评论需要 2–2000 个字符。')
        store.rate_limit('comments:'+str(user['id']),limit=10)
        with store.connect() as db:
            row=db.execute('INSERT INTO comments (route_id,user_id,category,content,created_at) VALUES (?,?,?,?,?) RETURNING id',
                (route,user['id'],category,content.strip(),int(time.time()))).fetchone()
        return {'id':row['id']}
    try:
        cursor=int(before) if before is not None else 9223372036854775807
        if not 0<cursor<=9223372036854775807:raise ValueError()
    except (ValueError,TypeError):raise AccountError(400,'分页参数不正确。') from None
    with store.connect() as db:
        rows=db.execute('''SELECT comments.id,category,content,comments.created_at,username,comments.user_id
            FROM comments JOIN users ON users.id=comments.user_id
            WHERE route_id=? AND comments.id<? ORDER BY comments.id DESC LIMIT 21''',(route,cursor)).fetchall()
        total=db.execute('SELECT COUNT(*) AS count FROM comments WHERE route_id=?',(route,)).fetchone()['count']
    items=[dict(row) for row in rows[:20]]
    return {'comments':items,'total':total,'next':items[-1]['id'] if len(rows)>20 else None}
