import runpy
import unittest

module = runpy.run_path(__file__.replace("test_usage.py", "antigravity-usage"))

class UsageTests(unittest.TestCase):
    def test_truncated_varint(self):
        with self.assertRaises(ValueError):
            list(module['proto_fields'](b'\x80'))

    def test_truncated_field(self):
        with self.assertRaises(ValueError):
            list(module['proto_fields'](b'\x0a\x05x'))

    def test_empty_model_is_unpriced(self):
        pricing = module['PricingEngine'].__new__(module['PricingEngine'])
        pricing.models = {'example': {'input': 1, 'output': 2}}
        self.assertIsNone(pricing.rate(''))

    def test_default_discovery_is_cli_only(self):
        import tempfile
        import sqlite3
        from pathlib import Path
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            for source in ['antigravity-cli', 'antigravity', 'antigravity-ide']:
                directory = home / '.gemini' / source / 'conversations'
                directory.mkdir(parents=True)
                con = sqlite3.connect(directory / 'sample.db')
                con.execute('CREATE TABLE gen_metadata (data BLOB)')
                con.execute('INSERT INTO gen_metadata VALUES (?)', (b'\x0a\x06\x9a\x01\x03gpt',))
                con.commit()
                con.close()
            with patch('pathlib.Path.home', return_value=home):
                loaded = runpy.run_path(str(Path(__file__).with_name('antigravity-usage')))
            store = loaded['ConversationStore']()
            self.assertEqual(store.dirs, [home / '.gemini/antigravity-cli/conversations'])
            result = store.aggregate(None)
            self.assertEqual(sum(c['tokens'] for c in result['by_month'].values()), 5600)
