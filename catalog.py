"""Canonical editable route catalog; stable IDs and non-destructive visibility."""
import json,time,secrets,math,re
from pathlib import Path
from accounts import AccountError
ROOT=Path(__file__).resolve().parent
SEED=json.loads((ROOT/'catalog-seed.json').read_text(encoding='utf-8'))
def initialize(store):
 with store.connect() as db:
  db.execute("CREATE TABLE IF NOT EXISTS catalog_routes (id TEXT PRIMARY KEY,data TEXT NOT NULL,origin TEXT NOT NULL,status TEXT NOT NULL DEFAULT 'published',user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,created_at BIGINT NOT NULL,updated_at BIGINT NOT NULL,revision BIGINT NOT NULL DEFAULT 1)")
  db.execute('CREATE TABLE IF NOT EXISTS catalog_meta (id TEXT PRIMARY KEY)')
  db.execute('CREATE INDEX IF NOT EXISTS catalog_status ON catalog_routes(status,origin)')
  if not db.execute("SELECT id FROM catalog_meta WHERE id='seed-95-v1'").fetchone():
   now=int(time.time())
   for r in SEED['routes']:db.execute('INSERT INTO catalog_routes(id,data,origin,status,user_id,created_at,updated_at) VALUES(?,?,?,?,?,?,?) ON CONFLICT(id) DO NOTHING',(r['id'],json.dumps(r,ensure_ascii=False),'curated','published',None,now,now))
   db.execute("INSERT INTO catalog_meta(id) VALUES('seed-95-v1') ON CONFLICT(id) DO NOTHING")
  db.execute("INSERT INTO catalog_routes(id,data,origin,status,user_id,created_at,updated_at) SELECT id,data,'community','published',user_id,created_at,created_at FROM route_submissions WHERE 1=1 ON CONFLICT(id) DO NOTHING")
def bootstrap(store):
 with store.connect() as db:
  rows=db.execute("SELECT data FROM catalog_routes WHERE status='published' AND origin<>'community' ORDER BY created_at,id").fetchall()
  ids=[r['id'] for r in db.execute('SELECT id FROM catalog_routes').fetchall()]
 return {'routes':[json.loads(r['data']) for r in rows],'meta':SEED['meta'],'knownIds':ids}
def route_exists(store,rid,public=True):
 if not isinstance(rid,str) or len(rid)>50:return False
 with store.connect() as db:
  row=db.execute('SELECT status FROM catalog_routes WHERE id=?',(rid,)).fetchone()
  if row:return not public or row['status']=='published'
  return bool(db.execute('SELECT id FROM route_submissions WHERE id=?',(rid,)).fetchone())
def valid_ids(store,ids,public=False):
 if not isinstance(ids,list) or len(ids)>500 or not all(isinstance(rid,str) and len(rid)<=50 for rid in ids):return set()
 if not ids:return set()
 with store.connect() as db:
  sql='SELECT id FROM catalog_routes WHERE id IN ('+','.join('?' for _ in ids)+')'+(" AND status='published'" if public else '')
  found={r['id'] for r in db.execute(sql,tuple(ids)).fetchall()}
  extra=db.execute("SELECT r.id FROM route_submissions r LEFT JOIN catalog_routes c ON c.id=r.id WHERE c.id IS NULL AND r.id IN ("+','.join('?' for _ in ids)+')',tuple(ids)).fetchall()
 return found|{r['id'] for r in extra}
def normalize(values,base=None):
 if not isinstance(values,dict):raise AccountError(400,'线路字段不正确。')
 r=dict(base or {'english':'Managed Trail','country':'中国','continent':'亚洲','flag':'🇨🇳','type':'管理员维护','tags':['精选线路'],'subtitle':'山野探索','highlights':[],'season':[],'gear':[],'itinerary':[],'sources':[],'videos':[],'logistics':'请核实交通接驳。','stay':'请核实合法住宿。','food':'自备饮水与食物。','permit':'出发前核实开放、预约及通行许可。','risks':'核实天气与路况，根据个人能力安排。','photoTip':'尊重环境与他人隐私。','locationOnly':True,'infoOnly':False,'photoPending':True,'accessText':'出发前核实开放','access':'planning'})
 allowed={'routeVersion','dataNotes','name','english','country','continent','province','description','subtitle','type','logistics','stay','food','permit','risks','photoTip','accessText','distance','altitude','days','level','points','season','gear','itinerary','highlights','tags','sources','videos','infoOnly','locationOnly'}
 if set(values)-allowed:raise AccountError(400,'包含不支持修改的字段。')
 r.setdefault('infoOnly',False);r.setdefault('locationOnly',False);r.setdefault('videos',[]);r.setdefault('sources',[]);r.setdefault('photoTip','');r.setdefault('province','')
 r.update(values)
 for key,low,high in [('routeVersion',0,2000),('dataNotes',0,4000),('name',2,80),('description',20,8000),('country',1,100),('province',0,80),('english',0,150),('subtitle',0,300),('type',0,150),('logistics',0,2000),('stay',0,2000),('food',0,2000),('permit',0,3000),('risks',0,3000),('photoTip',0,2000),('accessText',0,300)]:
  value=r.get(key,'')
  if not isinstance(value,str) or not low<=len(value.strip())<=high:raise AccountError(400,'字段 '+key+' 长度不正确。')
  r[key]=value.strip()
 if r.get('continent') not in ['亚洲','欧洲','非洲','北美洲','南美洲','大洋洲']:raise AccountError(400,'请选择有效的大洲。')
 if r['country'].startswith('中国'):
  from submissions import PROVINCES
  r['province']=' / '.join(p.strip() for p in r['province'].split('/'))
  if not r['province'] or any(p not in PROVINCES for p in r['province'].split(' / ')):raise AccountError(400,'中国线路请选择有效省区；跨省用 / 分隔。')
  r['country']='中国 · '+r['province'];r['flag']='🇨🇳'
 elif not base or r['country']!=base.get('country'):r['flag']='🏔️'
 for k,lo,hi in [('distance',0,2000),('altitude',0,9000),('days',0,90),('level',2,4)]:
  v=r.get(k)
  if type(v) not in (int,float) or not math.isfinite(v) or not lo<=v<=hi or k in ('days','level') and int(v)!=v:raise AccountError(400,'字段 '+k+' 数值不正确。')
 for k in ['infoOnly','locationOnly']:
  if type(r[k]) is not bool:raise AccountError(400,'线路展示开关不正确。')
 points=r.get('points')
 if not isinstance(points,list) or not 1<=len(points)<=300 or any(not isinstance(p,list) or len(p)!=2 or any(type(v) not in (int,float) or not math.isfinite(v) for v in p) or not -90<=p[0]<=90 or not -180<=p[1]<=180 for p in points):raise AccountError(400,'请提供 1–300 个合法经纬度坐标点。')
 if not isinstance(r.get('season'),list) or len(r['season'])>12 or any(type(v)is not int or not 1<=v<=12 for v in r['season']):raise AccountError(400,'季节月份应为 1–12。')
 for k,limit in [('gear',50),('highlights',30),('tags',20)]:
  if not isinstance(r.get(k),list) or len(r[k])>limit or any(not isinstance(v,str) or not 1<=len(v)<=500 for v in r[k]):raise AccountError(400,'字段 '+k+' 请逐行填写文字。')
 if not r['gear']:raise AccountError(400,'请填写装备建议。')
 itinerary=r.get('itinerary')
 if not isinstance(itinerary,list) or not 1<=len(itinerary)<=40 or any(not isinstance(p,list) or len(p)!=2 or any(not isinstance(v,str) or len(v)>2000 for v in p) for p in itinerary):raise AccountError(400,'行程请使用标题和说明的成对格式。')
 for k in ['sources']:
  if not isinstance(r.get(k),list) or len(r[k])>30 or any(not isinstance(p,list) or len(p)!=2 or not all(isinstance(v,str) for v in p) or len(p[0])>300 or len(p[1])>2000 or not re.match(r'^https://[^\s]+$',p[1]) for p in r[k]):raise AccountError(400,'来源和视频请填写标题及 HTTPS 链接。')
 videos=r.get('videos',[])
 if not isinstance(videos,list) or len(videos)>30:raise AccountError(400,'视频最多 30 条。')
 normalized=[]
 for video in videos:
  if isinstance(video,list) and len(video)==2:video={'title':video[0],'url':video[1]}
  if not isinstance(video,dict) or not isinstance(video.get('title'),str) or len(video['title'])>300 or not isinstance(video.get('url'),str) or len(video['url'])>2000 or not re.match(r'^https://[^\s]+$',video['url']):raise AccountError(400,'视频请填写标题和 HTTPS 链接。')
  old=next((v for v in (base or {}).get('videos',[]) if isinstance(v,dict) and v.get('url')==video['url'] and v.get('title')==video['title']),None)
  item=dict(old or {k:v for k,v in video.items() if k in ('title','url','bvid','platform','checked')})
  if not old:
   match=re.search(r'^https://(?:www\.)?bilibili\.com/video/(BV[A-Za-z0-9]+)',video['url'])
   if match:item['bvid']=match.group(1);item['platform']='B站'
   else:item.pop('bvid',None);item['platform']='视频链接'
  normalized.append(item)
 r['videos']=normalized
 if not base or r['distance']!=base.get('distance'):r['distanceText']='约 '+str(r['distance'])+' km' if r['distance'] else '里程待核实'
 if not base or r['altitude']!=base.get('altitude'):r['altitudeText']=str(r['altitude'])+' m' if r['altitude'] else '海拔待核实'
 r['altitudeLabel']=r.get('altitudeLabel','参考海拔')
 if not base or r['days']!=base.get('days'):r['duration']=(str(r['days'])+' 天 · 参考') if r['days'] else '天数待核实'
 if not base or r['season']!=base.get('season'):r['seasonText']='参考月份：'+','.join(map(str,r['season'])) if r['season'] else '请核实季节与天气'
 return r

def admin_listing(store,user,search='',page='1',status=''):
 from admin import require
 require(user)
 try:page=int(page);assert 1<=page<=100000
 except (ValueError,AssertionError):raise AccountError(400,'页码不正确。') from None
 if not isinstance(search,str) or len(search)>100 or status not in ('','draft','published','archived'):raise AccountError(400,'筛选条件不正确。')
 sql=' FROM catalog_routes WHERE 1=1';args=[]
 if search:sql+=' AND LOWER(data) LIKE ?';args.append('%'+search.casefold().replace('%','').replace('_','')+'%')
 if status:sql+=' AND status=?';args.append(status)
 with store.connect() as db:
  total=db.execute('SELECT COUNT(*) AS n'+sql,tuple(args)).fetchone()['n']
  rows=db.execute('SELECT id,data,status,origin,updated_at,revision'+sql+' ORDER BY updated_at DESC,id LIMIT 25 OFFSET ?',tuple(args+[(page-1)*25])).fetchall()
 items=[]
 for row in rows:
  item=dict(row);r=json.loads(item.pop('data'));item.update(name=r.get('name',''),province=r.get('province',''),country=r.get('country',''),level=r.get('level'),distance=r.get('distance'),days=r.get('days'));items.append(item)
 return {'items':items,'total':total,'page':page,'pageSize':25}
def preview(store,user,rid):
 from admin import require,fingerprint
 require(user)
 with store.connect() as db:
  row=db.execute('SELECT id,data,status,origin,user_id,created_at,updated_at,revision FROM catalog_routes WHERE id=?',(rid,)).fetchone()
  if not row:raise AccountError(404,'线路不存在。')
  record=dict(row);impact={k:db.execute('SELECT COUNT(*) AS n FROM '+t+' WHERE route_id=?',(rid,)).fetchone()['n'] for k,t in [('comments','comments'),('photos','route_photos')]}
 return {'record':record,'impact':impact,'version':fingerprint(record,{})}
def save(store,user,payload,rid=None):
 from admin import require,fingerprint
 require(user)
 if payload.get('userId')!=user['id']:raise AccountError(409,'账号已切换。')
 reason=payload.get('reason','');status=payload.get('status');action=payload.get('action','edit')
 if not isinstance(reason,str) or not 2<=len(reason.strip())<=400 or status not in ('published','draft','archived') or action not in ('edit','visibility','create'):raise AccountError(400,'状态或操作原因不正确。')
 now=int(time.time())
 with store.connect() as db:
  if rid:
   suffix=' FOR UPDATE' if isinstance(store.database,str) else ''
   row=db.execute('SELECT id,data,status,origin,user_id,created_at,updated_at,revision FROM catalog_routes WHERE id=?'+suffix,(rid,)).fetchone()
   if not row:raise AccountError(404,'线路不存在。')
   old=dict(row);impact={k:db.execute('SELECT COUNT(*) AS n FROM '+t+' WHERE route_id=?',(rid,)).fetchone()['n'] for k,t in [('comments','comments'),('photos','route_photos')]}
   if payload.get('version')!=fingerprint(old,{}):raise AccountError(409,'线路或关联数据已变化，请重新打开后保存。')
   r=normalize(payload.get('route',{}),json.loads(old['data'])) if action=='edit' else json.loads(old['data'])
   encoded=json.dumps(r,ensure_ascii=False);db.execute('UPDATE catalog_routes SET data=?,status=?,updated_at=?,revision=revision+1 WHERE id=?',(encoded,status,now,rid))
   if old['origin']=='community':db.execute('UPDATE route_submissions SET data=? WHERE id=?',(encoded,rid))
  else:
   if action!='create':raise AccountError(400,'新线路请选择创建操作。')
   r=normalize(payload.get('route'));rid='a-'+secrets.token_hex(12);r['id']=rid;old={};encoded=json.dumps(r,ensure_ascii=False)
   db.execute('INSERT INTO catalog_routes(id,data,status,origin,created_at,updated_at) VALUES(?,?,?,?,?,?)',(rid,encoded,status,'managed',now,now))
  db.execute('INSERT INTO admin_audit(actor_id,actor_name,kind,target,action,reason,snapshot,created_at) VALUES(?,?,?,?,?,?,?,?)',(user['id'],user['username'],'routes',rid,action,reason.strip(),json.dumps(old,ensure_ascii=False),now))
 return {'ok':True,'id':rid,'status':status}
