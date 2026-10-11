"""Allowlisted website administration. No generic SQL or secret-column access."""
import hashlib,json,os,time
from accounts import AccountError

def admin_ids():return {int(x) for x in os.environ.get('ATLAS_DATA_ADMIN_IDS','').split(',') if x.strip().isdigit()}
def allowed(user):return bool(user and user['id'] in admin_ids())
def require(user):
    if not allowed(user):raise AccountError(403,'数据管理仅对指定管理员开放。')
def initialize(store,postgres=False):
    identity='BIGSERIAL PRIMARY KEY' if postgres else 'INTEGER PRIMARY KEY'
    with store.connect() as db:db.execute(f'CREATE TABLE IF NOT EXISTS admin_audit (id {identity},actor_id BIGINT NOT NULL,actor_name TEXT NOT NULL,kind TEXT NOT NULL,target TEXT NOT NULL,action TEXT NOT NULL,reason TEXT NOT NULL,snapshot TEXT NOT NULL,created_at BIGINT NOT NULL)')
TABLES={
 'users':('users','id,username,created_at','username'),
 'comments':('comments','id,route_id,user_id,category,content,created_at','content'),
 'submissions':('route_submissions','id,user_id,data,created_at','data'),
 'photos':('route_photos','id,route_id,user_id,caption,status,reason,created_at,reviewed_by,reviewed_at','caption'),
 'follows':('follows','follower_id,followed_id,created_at',''),
 'audit':('admin_audit','id,actor_id,actor_name,kind,target,action,reason,created_at','reason')}
def kind_info(kind):
    if kind not in TABLES:raise AccountError(404,'管理栏目不存在。')
    return TABLES[kind]
def summary(store,user):
    require(user)
    with store.connect() as db:
        counts={k:db.execute('SELECT COUNT(*) AS n FROM '+v[0]).fetchone()['n'] for k,v in TABLES.items()}
        counts['pending']=db.execute("SELECT COUNT(*) AS n FROM route_photos WHERE status='pending'").fetchone()['n']
    return {'counts':counts,'user':user}
def listing(store,user,kind,search='',page='1'):
    require(user);table,columns,field=kind_info(kind)
    if not isinstance(search,str) or len(search)>100:raise AccountError(400,'搜索内容过长。')
    try:page=int(page);assert 1<=page<=100000
    except (ValueError,TypeError,AssertionError):raise AccountError(400,'分页参数不正确。') from None
    where='';params=[]
    if search and field:where=' WHERE LOWER('+field+') LIKE ?';params=['%'+search.casefold().replace('%','').replace('_','')+'%']
    order='created_at DESC,follower_id DESC,followed_id DESC' if kind=='follows' else 'created_at DESC,id DESC'
    with store.connect() as db:
        total=db.execute('SELECT COUNT(*) AS n FROM '+table+where,tuple(params)).fetchone()['n']
        rows=db.execute('SELECT '+columns+' FROM '+table+where+' ORDER BY '+order+' LIMIT 25 OFFSET ?',tuple(params+[(page-1)*25])).fetchall()
    items=[dict(r) for r in rows]
    for r in items:
        if kind=='submissions':
            route=json.loads(r.pop('data'));r.update(name=route['name'],province=route['province'],description=route['description'],level=route['level'],distance=route['distance'],days=route['days']);r['route']=route
    return {'items':items,'total':total,'page':page,'pageSize':25}
def snapshot(db,kind,rid):
    table,columns,_=kind_info(kind)
    if kind not in ('users','comments','submissions','photos'):raise AccountError(400,'此栏目仅供查看。')
    row=db.execute('SELECT '+columns+' FROM '+table+' WHERE id=?',(rid,)).fetchone()
    if not row:raise AccountError(404,'记录已不存在。')
    data=dict(row);impact={}
    if kind=='users':
        for key,table in [('comments','comments'),('submissions','route_submissions'),('photos','route_photos')]:impact[key]=db.execute('SELECT COUNT(*) AS n FROM '+table+' WHERE user_id=?',(rid,)).fetchone()['n']
        impact['follows']=db.execute('SELECT COUNT(*) AS n FROM follows WHERE follower_id=? OR followed_id=?',(rid,rid)).fetchone()['n']
        # Deleting authored routes also deletes other users' comments/photos on them.
        for key,table in [('routeComments','comments'),('routePhotos','route_photos')]:impact[key]=db.execute('SELECT COUNT(*) AS n FROM '+table+' WHERE route_id IN (SELECT id FROM route_submissions WHERE user_id=?) AND user_id<>?',(rid,rid)).fetchone()['n']
    elif kind=='submissions':
        for key,table in [('comments','comments'),('photos','route_photos')]:impact[key]=db.execute('SELECT COUNT(*) AS n FROM '+table+' WHERE route_id=?',(rid,)).fetchone()['n']
    return data,impact

def fingerprint(data,impact):return hashlib.sha256(json.dumps([data,impact],sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def preview(store,user,kind,rid):
    require(user)
    if kind in ('users','comments'):
        try:rid=int(rid);assert 0<rid<9223372036854775807
        except (ValueError,TypeError,AssertionError):raise AccountError(400,'记录编号不正确。') from None
    with store.connect() as db:data,impact=snapshot(db,kind,rid)
    return {'record':data,'impact':impact,'version':fingerprint(data,impact)}
def mutate(store,user,kind,rid,payload):
    require(user)
    if payload.get('userId')!=user['id']:raise AccountError(409,'账号已切换，请重新登录。')
    action=payload.get('action');reason=payload.get('reason','')
    if action not in ('delete','edit','approve','reject'):raise AccountError(400,'操作不支持。')
    if not isinstance(reason,str) or not 2<=len(reason.strip())<=400:raise AccountError(400,'请填写 2–400 字的操作原因。')
    table,_,_=kind_info(kind)
    if kind not in ('users','comments','submissions','photos'):raise AccountError(400,'此栏目仅供查看。')
    if kind in ('users','comments'):
        try:rid=int(rid);assert 0<rid<9223372036854775807
        except (ValueError,TypeError,AssertionError):raise AccountError(400,'记录编号不正确。') from None
    with store.connect() as db:
        if isinstance(store.database,str):db.execute('SELECT id FROM '+table+' WHERE id=? FOR UPDATE',(rid,))
        data,impact=snapshot(db,kind,rid)
        if payload.get('version')!=fingerprint(data,impact):raise AccountError(409,'数据已变化，请刷新后重新确认。')
        if action=='delete':
            expected=data['username'] if kind=='users' else str(rid)
            if payload.get('confirmation')!=expected:raise AccountError(400,'确认文字不匹配。')
            if kind=='users' and int(data['id']) in admin_ids():raise AccountError(400,'不能删除管理员账号。')
            if kind=='users':
                for linked in ['comments','route_photos']:db.execute('DELETE FROM '+linked+' WHERE route_id IN (SELECT id FROM route_submissions WHERE user_id=?)',(rid,))
            if kind=='submissions':
                for linked in ['comments','route_photos']:db.execute('DELETE FROM '+linked+' WHERE route_id=?',(rid,))
            db.execute('DELETE FROM '+table+' WHERE id=?',(rid,))
        elif kind=='comments' and action=='edit':
            value=payload.get('content');category=payload.get('category')
            from comments import CATEGORIES
            if not isinstance(value,str) or not 2<=len(value.strip())<=2000 or not isinstance(category,str) or category not in CATEGORIES:raise AccountError(400,'评论正文或类型不正确。')
            db.execute('UPDATE comments SET content=?,category=? WHERE id=?',(value.strip(),category,rid))
        elif kind=='submissions' and action=='edit':
            value=payload.get('description');name=payload.get('name');route=json.loads(data['data'])
            if not isinstance(name,str) or not 2<=len(name.strip())<=80 or not isinstance(value,str) or not 20<=len(value.strip())<=4000:raise AccountError(400,'线路名称或介绍长度不正确。')
            route['name']=name.strip();route['description']=value.strip()
            db.execute('UPDATE route_submissions SET data=? WHERE id=?',(json.dumps(route,ensure_ascii=False),rid))
        elif kind=='photos' and action in ('approve','reject'):
            if data['status'] not in ('pending','approved'):raise AccountError(409,'此照片已拒绝，请刷新。')
            if action=='approve' and data['status']!='pending':raise AccountError(400,'照片已通过。')
            db.execute('UPDATE route_photos SET status=?,reason=?,reviewed_by=?,reviewed_at=? WHERE id=?',('approved' if action=='approve' else 'rejected',reason.strip(),user['id'],int(time.time()),rid))
        else:raise AccountError(400,'此记录不支持该操作。')
        # Keep the safe pre-change record for audit; photos never include image bytes.
        db.execute('INSERT INTO admin_audit(actor_id,actor_name,kind,target,action,reason,snapshot,created_at) VALUES(?,?,?,?,?,?,?,?)',(user['id'],user['username'],kind,str(rid),action,reason.strip(),json.dumps(data,ensure_ascii=False),int(time.time())))
    return {'ok':True}
