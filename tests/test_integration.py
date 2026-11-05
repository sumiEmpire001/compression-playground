"""Integration and property-based-style deterministic codec checks."""
import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from compression import encode_runs, decode


class ProductionCodecTests(unittest.TestCase):
    def test_randomized_round_trips(self):
        rng = random.Random(20261105)
        for size in (0, 1, 2, 3, 127, 255, 256, 511, 4096, 16384):
            with self.subTest(size=size):
                payload = bytes(rng.randrange(256) for _ in range(size))
                self.assertEqual(decode(encode_runs(payload)), payload)

    def test_repeated_byte_runs_at_boundaries(self):
        for size in (254, 255, 256, 510, 511, 65535):
            with self.subTest(size=size):
                payload = b"\x00" * size
                self.assertEqual(decode(encode_runs(payload)), payload)

    def test_corrupted_header_rejected(self):
        with self.assertRaises(ValueError):
            decode(b"BAD!" + encode_runs(b"hello")[4:])

    def test_truncated_payload_rejected(self):
        payload = encode_runs(b"AAABBB")
        with self.assertRaises(ValueError):
            decode(payload[:-1])

    def test_empty_cli_roundtrip(self):
        self.cli_roundtrip(b"")

    def test_binary_cli_roundtrip(self):
        self.cli_roundtrip(bytes(range(256)) * 20)

    def cli_roundtrip(self, payload):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, packed, restored = (root / name for name in ("input.bin", "output.rle", "restored.bin"))
            source.write_bytes(payload)
            script = Path(__file__).resolve().parents[1] / "compression.py"
            for action, before, after in (("compress", source, packed), ("decompress", packed, restored)):
                result = subprocess.run(
                    [sys.executable, str(script), action, str(before), str(after)],
                    capture_output=True, text=True, timeout=20, check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(restored.read_bytes(), payload)


if __name__ == "__main__":
    unittest.main()
