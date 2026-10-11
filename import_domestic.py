"""Preview by default; --apply inserts only new stable route IDs, never overwrites."""
import argparse,json,os,re,time
from pathlib import Path
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parent
def validate(document):
 from catalog import normalize
 routes=document.get('routes');batch=document.get('batch')
 if not isinstance(batch,str) or not re.fullmatch('[a-z0-9-]{1,80}',batch) or not isinstance(routes,list) or not routes:raise ValueError('Invalid route batch')
 ids=set()
 for r in routes:
  if not isinstance(r,dict) or not re.fullmatch('[a-z0-9-]{1,50}',r.get('id','')) or r['id'] in ids:raise ValueError('Invalid or duplicate ID')
  ids.add(r['id']);normalize({},r)
  if not r['country'].startswith('中国') or not r['locationOnly'] or len(r['points'])!=1:raise ValueError('Expansion must use domestic regional markers')
  if not 17<=r['points'][0][0]<=55 or not 73<=r['points'][0][1]<=136:raise ValueError('Regional marker outside domestic catalog area')
  if not r.get('sources') or not r.get('routeVersion') or not r.get('dataNotes'):raise ValueError('Missing provenance')
  for _,url in r['sources']:
   parsed=urlsplit(url)
   if parsed.scheme!='https' or not parsed.hostname or parsed.username or parsed.password:raise ValueError('Invalid source URL')
 return routes
def import_batch(store,document,apply=False):
 routes=validate(document);now=int(time.time());inserted=0;existing=0
 import admin
 if apply:admin.initialize(store,postgres=isinstance(store.database,str))
 with store.connect() as db:
  if apply and isinstance(store.database,str):db.execute('SELECT pg_advisory_xact_lock(73910487)')
  elif apply:db.execute('BEGIN IMMEDIATE')
  for r in routes:
   if db.execute('SELECT id FROM catalog_routes WHERE id=?',(r['id'],)).fetchone():existing+=1;continue
   if not apply:inserted+=1;continue
   result=db.execute('INSERT INTO catalog_routes(id,data,origin,status,created_at,updated_at) VALUES(?,?,?,?,?,?) ON CONFLICT(id) DO NOTHING RETURNING id',(r['id'],json.dumps(r,ensure_ascii=False),'curated','published',now,now)).fetchone()
   if not result:existing+=1;continue
   inserted+=1
   db.execute('INSERT INTO admin_audit(actor_id,actor_name,kind,target,action,reason,snapshot,created_at) VALUES(?,?,?,?,?,?,?,?)',(0,'系统公开资料整理（应用户请求）','routes',r['id'],'create','批次 '+document['batch']+'；仅插入新线路，来源与版本均在详情内。','{}',now))
  if apply:db.execute('INSERT INTO catalog_meta(id) VALUES(?) ON CONFLICT(id) DO NOTHING',(document['batch'],))
 return {'mode':'applied' if apply else 'preview','new':inserted,'alreadyPresent':existing,'batchSize':len(routes)}
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--apply',action='store_true');parser.add_argument('--file',default=str(ROOT/'domestic-expansion-20261011.json'));args=parser.parse_args()
 values={}
 if (ROOT/'.env').exists():
  for line in (ROOT/'.env').read_text(encoding='utf-8-sig').splitlines():
   if '=' in line and not line.lstrip().startswith('#'):
    k,v=line.split('=',1);values[k.strip()]=v.strip().strip(chr(34)).strip(chr(39))
 from postgres_accounts import PostgresAccounts
 dsn=os.environ.get('DATABASE_URL') or values.get('DATABASE_URL')
 if not dsn:raise RuntimeError('DATABASE_URL unavailable')
 store=PostgresAccounts(dsn);document=json.loads(Path(args.file).read_text(encoding='utf-8'));print(json.dumps(import_batch(store,document,args.apply),ensure_ascii=True))
if __name__=='__main__':main()
