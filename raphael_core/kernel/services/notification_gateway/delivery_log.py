import json
import uuid
import time
from pathlib import Path

class DeliveryLedger:
    def __init__(self, log_dir=r"C:\RaphaelOS\Notifications"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.ledger_file = self.log_dir / "delivery_ledger.jsonl"
        
    def log_delivery(self, event_type: str, provider: str, status: str, attempts: int = 1):
        record = {
            "notification_id": f"notif_{uuid.uuid4().hex[:8]}",
            "event": event_type,
            "provider": provider,
            "status": status,
            "attempts": attempts,
            "timestamp": time.time()
        }
        
        with open(self.ledger_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
            
        return record["notification_id"]
