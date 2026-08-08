from typing import Any, Dict
import uuid
import time
from raphael_core.kernel.event_bus import emit

class ApprovalManager:
    def __init__(self):
        self.pending_approvals = {}
        
    def request_approval(self, request_type: str, requested_action: str, risk_level: str, requested_by: str, payload: Dict[str, Any]):
        approval_id = f"approve_{uuid.uuid4().hex[:8]}"
        self.pending_approvals[approval_id] = {
            "approval_id": approval_id,
            "request_type": request_type,
            "requested_action": requested_action,
            "risk_level": risk_level,
            "requested_by": requested_by,
            "timestamp": time.time(),
            "payload": payload
        }
        
        # Emits an event that NotificationGateway will pick up
        emit("APPROVAL.REQUIRED", "ApprovalManager", self.pending_approvals[approval_id])
        return approval_id
        
    def grant_approval(self, approval_id: str, approved_by: str):
        if approval_id in self.pending_approvals:
            req = self.pending_approvals.pop(approval_id)
            event_payload = {
                "approval_id": approval_id,
                "request_type": req["request_type"],
                "requested_action": req["requested_action"],
                "risk_level": req["risk_level"],
                "requested_by": req["requested_by"],
                "approved_by": approved_by,
                "timestamp": time.time(),
                "signature": f"hash_{approval_id}_{approved_by}",
                "original_payload": req["payload"]
            }
            emit("APPROVAL.GRANTED", "ApprovalManager", event_payload)
            return True
        return False
        
    def reject_approval(self, approval_id: str, rejected_by: str):
        if approval_id in self.pending_approvals:
            req = self.pending_approvals.pop(approval_id)
            emit("APPROVAL.REJECTED", "ApprovalManager", {
                "approval_id": approval_id,
                "rejected_by": rejected_by,
                "timestamp": time.time()
            })
            return True
        return False

approval_manager = ApprovalManager()
