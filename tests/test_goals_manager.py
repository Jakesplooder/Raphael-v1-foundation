import unittest
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

from raphael_core.goals_manager import GoalsManager, _read_text

class TestGoalsManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_path = Path(self.temp_dir.name)
        
        # Create mock vault structure
        self.vault_path = self.data_path / "vault"
        raphael_dir = self.vault_path / "00_Raphael"
        raphael_dir.mkdir(parents=True)
        
        self.goals_file = raphael_dir / "Goals.md"
        with open(self.goals_file, "w", encoding="utf-8") as f:
            f.write("""# Goals
## GOAL-001 Migrate to RRK
### Title
Migrate Goals Subsystem

### Status
Active

### Priority
High

### Next Milestone
D1 Complete

## GOAL-002 Something Else
### Title
Another Goal

### Status
Pending

### Priority
Medium

### Next Milestone
TBD
""")
            
    def tearDown(self):
        self.temp_dir.cleanup()

    @patch("raphael_core.goals_manager.os.environ.get")
    def test_goals_manager_parsing(self, mock_env):
        mock_env.return_value = self.temp_dir.name
        
        mgr = GoalsManager()
        items = mgr.get_all_goals()
        
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["id"], "GOAL-001")
        self.assertEqual(items[0]["title"], "Migrate Goals Subsystem")
        self.assertEqual(items[0]["status"], "Active")
        self.assertEqual(items[0]["priority"], "High")
        self.assertEqual(items[0]["milestone"], "D1 Complete")
        
        self.assertEqual(items[1]["id"], "GOAL-002")
        self.assertEqual(items[1]["title"], "Another Goal")
        self.assertEqual(items[1]["status"], "Pending")

    @patch("raphael_core.goals_manager.os.environ.get")
    def test_goals_manager_lifecycle(self, mock_env):
        mock_env.return_value = self.temp_dir.name
        mgr = GoalsManager()
        
        # We can't trivially run async methods in standard unittest without asyncio.run
        import asyncio
        asyncio.run(mgr.initialize())
        asyncio.run(mgr.start())
        self.assertEqual(mgr.status(), "GoalsManager running")
        self.assertTrue(asyncio.run(mgr.heartbeat()))
        
        asyncio.run(mgr.stop())
        self.assertFalse(asyncio.run(mgr.heartbeat()))
        asyncio.run(mgr.shutdown())

if __name__ == '__main__':
    unittest.main()
