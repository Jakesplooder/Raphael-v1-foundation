import json
import os
import unittest
import hashlib
from pathlib import Path

class GoldenMasterTests(unittest.TestCase):
    def test_golden_master_integrity(self):
        golden_dir = Path(__file__).resolve().parent / "golden" / "v4.2-pre-D1"
        manifest_path = golden_dir / "manifest.json"
        
        self.assertTrue(manifest_path.exists(), "Golden Master manifest.json not found")
        
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
            
        fixtures = manifest.get("fixtures", {})
        self.assertGreater(len(fixtures), 0, "No fixtures found in manifest")
        
        for rel_path, expected_hash in fixtures.items():
            file_path = golden_dir / rel_path
            self.assertTrue(file_path.exists(), f"Fixture missing: {rel_path}")
            
            sha256 = hashlib.sha256()
            with open(file_path, "rb") as f:
                for block in iter(lambda: f.read(4096), b""):
                    sha256.update(block)
                    
            actual_hash = sha256.hexdigest()
            self.assertEqual(expected_hash, actual_hash, f"Golden Master corrupted! Hash mismatch for {rel_path}")

if __name__ == '__main__':
    unittest.main()
