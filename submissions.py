"""Account-owned public route submissions stored in the persistent database."""
import json
import math
import secrets
import time
from accounts import AccountError

PROVINCES=['北京','天津','河北','山西','内蒙古','辽宁','吉林','黑龙江','上海','江苏','浙江','安徽','福建','江西','山东','河南','湖北','湖南','广东','广西','海南','重庆','四川','贵州','云南','西藏','陕西','甘肃','青海','宁夏','新疆','香港','澳门','台湾']

def initialize(store):
    with store.connect() as db:
        db.execute('''CREATE TABLE IF NOT EXISTS route_submissions (
            id TEXT PRIMARY KEY,user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            data TEXT NOT NULL,created_at BIGINT NOT NULL)''')
        db.execute('CREATE INDEX IF NOT EXISTS route_submissions_owner ON route_submissions(user_id,id)')

def exists(store,rid):
    from comments import ROUTES
    if isinstance(rid,str) and rid in ROUTES:return True
    if not isinstance(rid,str) or len(rid)>50:return False
    with store.connect() as db:return bool(db.execute('SELECT 1 FROM route_submissions WHERE id=?',(rid,)).fetchone())

def valid_ids(store,ids):
    from comments import ROUTES
    if not isinstance(ids,list) or len(ids)>200 or not all(isinstance(rid,str) and len(rid)<=50 for rid in ids):return set()
    known=set(ids)&ROUTES;missing=set(ids)-known
    if missing:
        with store.connect() as db:
            rows=db.execute('SELECT id FROM route_submissions WHERE id IN ('+','.join('?' for _ in missing)+')',tuple(missing)).fetchall()
        known.update(row['id'] for row in rows)
    return known

def text(data,key,limit,default='',minimum=0):
    value=data.get(key,default)
    if not isinstance(value,str) or not minimum<=len(value.strip())<=limit:raise AccountError(400,'字段 '+key+' 的长度不正确。')
    return value.strip()

def numeric(value,low,high):
    if type(value) not in [int,float] or not math.isfinite(value) or not low<=value<=high:raise AccountError(400,'里程、海拔或坐标超出有效范围。')
    return value

def publish(store,user,data):
    if not user:raise AccountError(401,'登录后即可投稿线路。')
    if data.get('userId')!=user['id']:raise AccountError(409,'账号已切换，请重新打开投稿窗口。')
    name=text(data,'name',80,minimum=2);province=text(data,'province',20)
    if province not in PROVINCES:raise AccountError(400,'请选择有效的省区。')
    description=text(data,'description',4000,minimum=20)
    distance=numeric(data.get('distance'),0.1,1000);altitude=numeric(data.get('altitude',0),0,9000)
    days=numeric(data.get('days'),1,60);level=data.get('level')
    if type(days) is not int or type(level) is not int or level not in [2,3,4]:raise AccountError(400,'请选择有效的天数与难度。')
    points=data.get('points')
    if not isinstance(points,list) or not 1<=len(points)<=300:raise AccountError(400,'请填写位置或导入最多 300 个展示轨迹点。')
    for point in points:
        if not isinstance(point,list) or len(point)!=2:raise AccountError(400,'轨迹点格式不正确。')
        numeric(point[0],17,55);numeric(point[1],73,136)
    location_only=len(points)==1
    if location_only:points=[points[0],points[0]]
    season=data.get('season',[3,4,5,9,10,11])
    if not isinstance(season,list) or not season or not all(type(m) is int and 1<=m<=12 for m in season):raise AccountError(400,'月份格式不正确。')
    gear=text(data,'gear',1500,'防滑徒步鞋\n雨衣\n饮水与食物\n离线地图与充电宝\n急救包').splitlines()
    gear=list(dict.fromkeys(g.strip() for g in gear if g.strip()))
    if not 5<=len(gear)<=30:raise AccountError(400,'请提供 5–30 条装备建议，每行一条。')
    itinerary=text(data,'itinerary',3000,'确认入口、天气与开放范围\n按计划行走，预留折返与返程时间').splitlines()
    itinerary=[['第 '+str(i+1)+' 段',line.strip()] for i,line in enumerate(itinerary) if line.strip()]
    if not 2<=len(itinerary)<=30:raise AccountError(400,'请填写 2–30 个行程分段，每行一段。')
    rid='u-'+str(time.time_ns())+'-'+secrets.token_hex(5)
    route=dict(id=rid,name=name,english='Community Trail',country='中国 · '+province,province=province,continent='亚洲',flag='🇨🇳',level=level,distance=distance,distanceText=f'投稿参考约 {distance:g} km',days=days,duration=f'{days} 天 · 用户参考',altitude=altitude,altitudeText=f'投稿参考约 {altitude:g} m' if altitude else '投稿未提供海拔',altitudeLabel='投稿参考海拔（非核验）',season=sorted(set(season)),seasonText='投稿参考月份，请结合天气确认',type='社区投稿 / 用户轨迹' if not location_only else '社区投稿 / 位置标注',tags=['社区投稿','用户经验'],subtitle='来自同行者的路线分享',description=description,highlights=[name,'用户贡献的徒步经验'],gear=gear,itinerary=itinerary,points=points,locationOnly=location_only,community=True,photoPending=True,sources=[],videos=[],access='community',accessText='社区投稿 · 未经独立核验',author={'id':user['id'],'username':user['username']},created_at=int(time.time()))
    for key,default in {'logistics':'请向作者核实入口与接驳。','stay':'按行程提前确认合法住宿。','food':'自带饮水与食物，补给点请提前确认。','permit':'投稿不代表通行许可；出发前向管理部门核实开放与预约。','risks':'注意天气、体力及路况；用户轨迹不等于安全或合法通行证明。','photoTip':'沿开放步道拍摄，尊重当地环境。'}.items():route[key]=text(data,key,1500,default)
    store.rate_limit('route-submit:'+str(user['id']),limit=5)
    with store.connect() as db:db.execute('INSERT INTO route_submissions (id,user_id,data,created_at) VALUES (?,?,?,?)',(rid,user['id'],json.dumps(route,ensure_ascii=False),route['created_at']))
    return {'route':route}

def listing(store,before=None,owner=None):
    if before is not None and (not isinstance(before,str) or len(before)>50):raise AccountError(400,'分页参数不正确。')
    params=[before or 'z'];sql='SELECT data,id FROM route_submissions WHERE id<?'
    if owner is not None:sql+=' AND user_id=?';params.append(owner)
    with store.connect() as db:rows=db.execute(sql+' ORDER BY id DESC LIMIT 51',tuple(params)).fetchall()
    return {'routes':[json.loads(row['data']) for row in rows[:50]],'next':rows[49]['id'] if len(rows)>50 else None}

def get_route(store,rid):
    with store.connect() as db:row=db.execute('SELECT data FROM route_submissions WHERE id=?',(rid,)).fetchone()
    if not row:raise AccountError(404,'投稿线路不存在。')
    return {'route':json.loads(row['data'])}
