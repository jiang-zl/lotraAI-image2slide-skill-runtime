"""Entry downloads retain the same content pins through official API fallback."""
import contextlib,hashlib,importlib.util,json,shutil,unittest,uuid
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
TESTS=ROOT/'.lotraAI-build/entry-tests';TESTS.mkdir(parents=True,exist_ok=True)
spec=importlib.util.spec_from_file_location('lotra_entry',ROOT/'tools/install_lotra.py')
entry=importlib.util.module_from_spec(spec);spec.loader.exec_module(entry)


@contextlib.contextmanager
def cache():
    folder=TESTS/uuid.uuid4().hex;folder.mkdir()
    try:yield folder
    finally:
        if not folder.resolve().is_relative_to(TESTS.resolve()):raise ValueError('Unexpected test cleanup path')
        shutil.rmtree(folder)


class EntryFallback(unittest.TestCase):
    def record(self,data):
        return {'url':'https://github.com/jiang-zl/lotraAI-image2slide-skill/releases/download/v1.35.3/release.json',
                'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}

    def test_verified_cache_does_not_download(self):
        data=b'catalog';record=self.record(data)
        with cache() as folder,patch.object(entry,'request') as network:
            (folder/record['sha256']).write_bytes(data)
            self.assertEqual(entry.fetch(record,folder).read_bytes(),data);network.assert_not_called()

    def test_api_fallback_retains_original_hash(self):
        data=b'catalog';record=self.record(data)
        release=json.dumps({'tag_name':'v1.35.3','id':7}).encode()
        assets=json.dumps([{'name':'release.json','id':8,'size':len(data),'state':'uploaded'}]).encode()
        with cache() as folder,patch.object(entry,'request') as network:
            network.side_effect=[RuntimeError('fixture timeout'),(release,None),(assets,None),(data,None)]
            self.assertEqual(entry.fetch(record,folder).read_bytes(),data)
            self.assertEqual(network.call_args.kwargs['headers']['Accept'],'application/octet-stream')

    def test_wrong_api_asset_size_is_rejected(self):
        data=b'catalog';record=self.record(data)
        release=json.dumps({'tag_name':'v1.35.3','id':7}).encode()
        assets=json.dumps([{'name':'release.json','id':8,'size':999,'state':'uploaded'}]).encode()
        with cache() as folder,patch.object(entry,'request') as network:
            network.side_effect=[RuntimeError('fixture timeout'),(release,None),(assets,None)]
            with self.assertRaisesRegex(ValueError,'identity differs'):entry.fetch(record,folder)

    def test_transport_success_without_matching_hash_is_rejected(self):
        data=b'catalog';record=self.record(data)
        with cache() as folder,patch.object(entry,'request',return_value=(b'changed',None)):
            with self.assertRaisesRegex(ValueError,'hash differs'):entry.fetch(record,folder)


if __name__=='__main__':unittest.main(verbosity=2)
