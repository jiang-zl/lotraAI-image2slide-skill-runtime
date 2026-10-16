"""Publication guards without credentials/network/uploads."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest
from uuid import uuid4

HERE=Path(__file__).resolve().parents[1]
SCRIPT=HERE/'tools/publish_v134.py'
spec=importlib.util.spec_from_file_location('v134_publisher',SCRIPT)
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)

class PublisherGuards(unittest.TestCase):
 def setUp(self):
  self.root=HERE/'.lotraAI-build/publisher-checks'/uuid4().hex;self.root.mkdir(parents=True)
  self.file=self.root/'asset.bin';self.file.write_bytes(b'0123456789')
 def test_part_is_verified_at_declared_offset(self):
  row={'bytes':4,'source_bytes':10,'offset':3,'sha256':hashlib.sha256(b'3456').hexdigest()}
  self.assertTrue(p.local_matches(self.file,row));row['offset']=4
  self.assertFalse(p.local_matches(self.file,row))
 def test_path_escape_is_rejected(self):
  for name in ('../asset.bin','x/../../asset.bin','x\\asset.bin'):
   with self.assertRaises(ValueError):p.local(self.root,name)
 def test_conflicting_remote_digest_is_not_a_match(self):
  row={'bytes':10,'sha256':hashlib.sha256(self.file.read_bytes()).hexdigest()}
  self.assertFalse(p.matching({'name':'asset.bin','size':10,'state':'uploaded','digest':'sha256:'+'a'*64},row))
 def test_check_local_does_not_require_publication_credentials(self):
  repositories=[{'repository':n,'commit':'0'*40,'previous_branches':{'release':'0'*40,'1.34.0':'0'*40}} for n in sorted(p.ALLOWED)]
  plan={'schema':'lotra-prepared-publication-1','version':'1.34.0','tag':'v1.34.0','publication_revision':1,
   'repositories':repositories,'groups':[{'repository':r['repository'],'tag':'v1.34.0',
    'assets':[{'name':'asset.bin','path':'asset.bin','bytes':10,'sha256':hashlib.sha256(self.file.read_bytes()).hexdigest()}]} for r in repositories]}
  file=self.root/'Publish-plan.json';file.write_text(json.dumps(plan),encoding='utf-8')
  result=subprocess.run([sys.executable,'-I','-X','utf8','-B',str(SCRIPT),'--plan',str(file),'--asset-root',str(self.root),'--check-local'],capture_output=True,text=True,timeout=30)
  self.assertEqual(result.returncode,0,result.stdout+result.stderr)
  self.assertFalse(json.loads((self.root/'Local-check.json').read_bytes())['network'])
 def test_historical_retirement_is_refused_before_network(self):
  with self.assertRaises(ValueError):p.cleanup(None,{'cleanup':[{'tag':'v1.33.0'}]})
 def test_missing_runtime_group_cannot_activate_release_branches(self):
  with self.assertRaises(ValueError):p.targets({'groups':[{'repository':'jiang-zl/lotraAI-image2slide-skill'}],'repositories':[]})

if __name__=='__main__':unittest.main(verbosity=2)
