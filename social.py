"""Public hiking profiles and authenticated following relationships."""
import json
import time
from accounts import AccountError

def initialize(store):
    with store.connect() as db:
        db.execute('''CREATE TABLE IF NOT EXISTS follows (
            follower_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            followed_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            created_at BIGINT NOT NULL, PRIMARY KEY (follower_id,followed_id),
            CHECK (follower_id<>followed_id))''')
        db.execute('CREATE INDEX IF NOT EXISTS follows_followed ON follows(followed_id,follower_id)')

def number(value,default=None):
    try:
        result=int(value) if value is not None else default
        if result is None or not 0<=result<9223372036854775807:raise ValueError()
        return result
    except (TypeError,ValueError):raise AccountError(400,'用户或分页参数不正确。') from None

def profile(store,uid,viewer=None):
    uid=number(uid)
    with store.connect() as db:
        row=db.execute('SELECT id,username FROM users WHERE id=?',(uid,)).fetchone()
        if not row:raise AccountError(404,'用户不存在。')
        saved=db.execute('SELECT data FROM preferences WHERE user_id=?',(uid,)).fetchone()
        following=db.execute('SELECT COUNT(*) AS count FROM follows WHERE follower_id=?',(uid,)).fetchone()['count']
        followers=db.execute('SELECT COUNT(*) AS count FROM follows WHERE followed_id=?',(uid,)).fetchone()['count']
        followed=bool(viewer and db.execute('SELECT 1 FROM follows WHERE follower_id=? AND followed_id=?',(viewer['id'],uid)).fetchone())
    from comments import ROUTES
    completed=[item for item in json.loads(saved['data']).get('completed',[]) if item in ROUTES] if saved else []
    return {'user':dict(row),'completed':completed,'followingCount':following,'followerCount':followers,'isFollowing':followed}

def people(store,search='',before=None,uid=None,kind=None):
    cursor=number(before,0)
    if not isinstance(search,str) or len(search)>24:raise AccountError(400,'搜索词最多 24 个字符。')
    query=search.strip().casefold().replace('\\','\\\\').replace('%','\\%').replace('_','\\_')
    with store.connect() as db:
        if uid is not None:
            uid=number(uid)
            if not db.execute('SELECT 1 FROM users WHERE id=?',(uid,)).fetchone():raise AccountError(404,'用户不存在。')
            if kind=='following':sql='SELECT users.id,username FROM users JOIN follows ON users.id=follows.followed_id WHERE follows.follower_id=? AND users.id>? ORDER BY users.id LIMIT 21'
            elif kind=='followers':sql='SELECT users.id,username FROM users JOIN follows ON users.id=follows.follower_id WHERE follows.followed_id=? AND users.id>? ORDER BY users.id LIMIT 21'
            else:raise AccountError(404,'列表不存在。')
            rows=db.execute(sql,(uid,cursor)).fetchall()
        else:
            rows=db.execute("SELECT id,username FROM users WHERE id>? AND username_key LIKE ? ESCAPE '\\' ORDER BY id LIMIT 21",(cursor,'%'+query+'%')).fetchall()
    users=[dict(row) for row in rows[:20]]
    return {'users':users,'next':users[-1]['id'] if len(rows)>20 else None}

def follow(store,uid,viewer,data):
    if not viewer:raise AccountError(401,'登录后即可关注同行者。')
    uid=number(uid)
    if data.get('userId')!=viewer['id']:raise AccountError(409,'账号已切换，请重新打开个人主页。')
    if uid==viewer['id']:raise AccountError(400,'不能关注自己。')
    enabled=data.get('following')
    if type(enabled) is not bool:raise AccountError(400,'关注状态不正确。')
    store.rate_limit('follow:'+str(viewer['id']),limit=60)
    with store.connect() as db:
        if not db.execute('SELECT 1 FROM users WHERE id=?',(uid,)).fetchone():raise AccountError(404,'用户不存在。')
        if enabled:db.execute('INSERT INTO follows (follower_id,followed_id,created_at) VALUES (?,?,?) ON CONFLICT(follower_id,followed_id) DO NOTHING',(viewer['id'],uid,int(time.time())))
        else:db.execute('DELETE FROM follows WHERE follower_id=? AND followed_id=?',(viewer['id'],uid))
    return profile(store,uid,viewer)
