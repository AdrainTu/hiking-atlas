import copy,json,tempfile,unittest
from pathlib import Path
from accounts import Accounts
from catalog import SEED
from import_domestic import import_batch,validate
ROOT=Path(__file__).resolve().parent
class ExpansionTests(unittest.TestCase):
 def setUp(self):self.temp=tempfile.TemporaryDirectory();self.store=Accounts(Path(self.temp.name)/'db');self.batch=json.loads((ROOT/'domestic-expansion-20261011.json').read_text(encoding='utf-8'))
 def tearDown(self):self.temp.cleanup()
 def test_provenance_metrics_and_domestic_coverage(self):
  rows=validate(self.batch);self.assertEqual(len(rows),109)
  self.assertFalse({r['id'] for r in rows}&{r['id'] for r in SEED['routes']})
  provinces={p for r in SEED['routes']+rows for p in r.get('province','').split(' / ') if p};self.assertEqual(len(provinces),34)
  for r in rows:self.assertTrue(r['photoPending']);self.assertTrue(r['locationOnly']);self.assertEqual(len(r['points']),1);self.assertIn('GPX',r['dataNotes']);self.assertEqual(r['season'],[])
  for rid in ['gongga-grand','gongga-small','small-wutai-new','qinling-ice-new']:
   r=next(r for r in rows if r['id']==rid);self.assertTrue(r['infoOnly']);self.assertTrue(any('gov' in u for _,u in r['sources']))
  gongga=next(r for r in rows if r['id']=='gongga-grand');self.assertEqual(gongga['altitude'],4920);self.assertNotEqual(gongga['altitude'],7556)
 def test_preview_atomic_insert_and_rerun_preserves_edits(self):
  self.assertEqual(import_batch(self.store,self.batch)['new'],109)
  with self.store.connect() as db:self.assertEqual(db.execute('SELECT COUNT(*) AS n FROM catalog_routes').fetchone()['n'],95)
  self.assertEqual(import_batch(self.store,self.batch,True)['new'],109)
  with self.store.connect() as db:
   db.execute("UPDATE catalog_routes SET status='archived',data=? WHERE id='gongga-small'",(json.dumps({'id':'gongga-small','name':'Admin edited'}),))
  self.assertEqual(import_batch(self.store,self.batch,True)['new'],0)
  with self.store.connect() as db:
   row=db.execute("SELECT status,data FROM catalog_routes WHERE id='gongga-small'").fetchone();self.assertEqual(row['status'],'archived');self.assertEqual(json.loads(row['data'])['name'],'Admin edited')
   self.assertEqual(db.execute('SELECT COUNT(*) AS n FROM admin_audit').fetchone()['n'],109)
 def test_expanded_library_can_be_saved_as_footprints(self):
  import_batch(self.store,self.batch,True)
  user,_=self.store.register({'username':'FootprintFixture','password':'fixture-long-password'},None)
  with self.store.connect() as db:ids=[r['id'] for r in db.execute('SELECT id FROM catalog_routes').fetchall()]
  self.assertEqual(len(ids),204)
  result=self.store.preferences(user,{'userId':user['id'],'favorites':ids,'completed':ids,'gear':{}})
  self.assertEqual(len(result['completed']),204)
 def test_bad_batches_do_not_change_database(self):
  for change in [{'id':'bad id'},{'country':'Elsewhere'},{'points':[[0,0]]},{'sources':[['bad','https://name:secret@example.com']]},{'routeVersion':''}]:
   document=copy.deepcopy(self.batch);document['routes'][-1].update(change)
   with self.assertRaises(Exception):import_batch(self.store,document,True)
  with self.store.connect() as db:self.assertEqual(db.execute('SELECT COUNT(*) AS n FROM catalog_routes').fetchone()['n'],95)
if __name__=='__main__':unittest.main()
