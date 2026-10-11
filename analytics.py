"""First-party, pseudonymous page views; no IP addresses or account associations."""
import os
import re
import hashlib
from datetime import datetime, timedelta, timezone
from accounts import AccountError
TZ=timezone(timedelta(hours=8))
def initialize(store):
    with store.connect() as db:
        db.execute("CREATE TABLE IF NOT EXISTS analytics_events (day TEXT NOT NULL,event_id TEXT NOT NULL,visitor TEXT NOT NULL,route TEXT NOT NULL,PRIMARY KEY(day,event_id))")
        db.execute("CREATE INDEX IF NOT EXISTS analytics_day ON analytics_events(day)")
def allowed(user):
    ids={int(x) for x in os.environ.get('ATLAS_ANALYTICS_ADMIN_IDS','').split(',') if x.strip().isdigit()}
    return bool(user and user['id'] in ids)
def record(store,data):
    visitor=data.get('visitor');event=data.get('event');route=data.get('route','')
    if not all(isinstance(v,str) and re.fullmatch(r'[a-f0-9]{32}',v) for v in (visitor,event)):
        raise AccountError(400,'统计标识格式不正确。')
    if not isinstance(route,str) or len(route)>90:raise AccountError(400,'线路格式不正确。')
    if route:
        from submissions import exists
        if not exists(store,route):raise AccountError(400,'线路不存在。')
    now=datetime.now(TZ);day=now.date().isoformat()
    digest=hashlib.sha256((day+visitor).encode()).hexdigest()
    with store.connect() as db:
        # Retries are idempotent; a per-browser cap limits accidental loops.
        count=db.execute('SELECT COUNT(*) AS n FROM analytics_events WHERE day=? AND visitor=?',(day,digest)).fetchone()['n']
        if count<500:
            db.execute('INSERT INTO analytics_events(day,event_id,visitor,route) VALUES(?,?,?,?) ON CONFLICT(day,event_id) DO NOTHING',(day,event,digest,route))
        db.execute('DELETE FROM analytics_events WHERE day<?',((now.date()-timedelta(days=89)).isoformat(),))
    return {'ok':True}
def report(store,user,days):
    if not allowed(user):raise AccountError(403,'访问统计仅对指定管理员开放。')
    if days not in ('7','30','90'):raise AccountError(400,'请选择 7、30 或 90 天。')
    end=datetime.now(TZ).date();start=end-timedelta(days=int(days)-1)
    with store.connect() as db:
        rows=db.execute('SELECT day,COUNT(*) AS pv,COUNT(DISTINCT visitor) AS uv FROM analytics_events WHERE day>=? GROUP BY day ORDER BY day',(start.isoformat(),)).fetchall()
        top=db.execute("SELECT route,COUNT(*) AS pv,COUNT(DISTINCT day || visitor) AS visitor_days FROM analytics_events WHERE day>=? AND route<>'' GROUP BY route ORDER BY pv DESC LIMIT 10",(start.isoformat(),)).fetchall()
        first=db.execute('SELECT MIN(day) AS day FROM analytics_events').fetchone()['day']
    values={r['day']:dict(r) for r in rows}
    daily=[values.get((start+timedelta(days=i)).isoformat(),{'day':(start+timedelta(days=i)).isoformat(),'pv':0,'uv':0}) for i in range(int(days))]
    return {'daily':daily,'top':[dict(r) for r in top],'firstDay':first,'timezone':'Asia/Shanghai','retentionDays':90}
