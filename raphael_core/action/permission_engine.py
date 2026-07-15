import logging

logger = logging.getLogger("rrk.action.permissions")

class PermissionEngine:
    """
    Validates whether an employee role has the authority to execute an action.
    """
    def __init__(self):
        # Role -> Allowed Permissions
        self.role_policies = {
            "Marketing Employee": {
                "allowed": ["MARKETING_EXECUTION", "COMMERCE_EXECUTION"],
                "requires_approval": ["MARKETING_SPEND"]
            },
            "CEO Agent": {
                "allowed": ["MARKETING_EXECUTION", "COMMERCE_EXECUTION", "MARKETING_SPEND", "CAPITAL_ALLOCATION"],
                "requires_approval": ["VENTURE_CREATION"]
            },
            "Executive Council": {
                "allowed": ["*"] # Full access
            }
        }

    def check_permission(self, role: str, required_permission: str, cost: float = 0) -> str:
        """
        Returns 'APPROVED', 'DENIED', or 'REQUIRES_APPROVAL'
        """
        if required_permission == "NONE":
            return "APPROVED"
            
        policy = self.role_policies.get(role, {"allowed": [], "requires_approval": []})
        
        if "*" in policy.get("allowed", []):
            return "APPROVED"
            
        if required_permission in policy.get("allowed", []):
            return "APPROVED"
            
        if required_permission in policy.get("requires_approval", []):
            logger.info(f"Permission {required_permission} for {role} requires CEO approval.")
            return "REQUIRES_APPROVAL"
            
        return "DENIED"
