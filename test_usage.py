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
