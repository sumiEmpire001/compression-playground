import unittest
from compression import encode_runs,decode


class CompressionTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(decode(encode_runs(b"")),b"")
    def test_single(self):
        self.assertEqual(decode(encode_runs(b"A")),b"A")
    def test_repeats(self):
        self.assertEqual(decode(encode_runs(b"AAAAABBBB")),b"AAAAABBBB")
    def test_long_run(self):
        self.assertEqual(decode(encode_runs(b"X"*600)),b"X"*600)
    def test_binary(self):
        self.assertEqual(decode(encode_runs(bytes(range(256)))),bytes(range(256)))
    def test_invalid_header(self):
        with self.assertRaises(ValueError): decode(b"invalid")
    def test_invalid_length(self):
        with self.assertRaises(ValueError): decode(b"RLE1\x02")
    def test_size_limit(self):
        with self.assertRaises(ValueError): decode(encode_runs(b"A"*100),max_output=50)
    def test_zero_count(self):
        with self.assertRaises(ValueError): decode(b"RLE1\x00A")


if __name__=="__main__":
    unittest.main()
