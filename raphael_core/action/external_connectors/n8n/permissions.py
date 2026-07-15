class AutomationPermissions:
    """
    Manages authority levels for external execution to prevent agents from 
    taking destructive external actions (e.g., deleting databases) without approval.
    """
    def __init__(self):
        self.role_policies = {
            "Marketing Employee": ["CREATE_SOCIAL_POST", "UPDATE_CAMPAIGN"],
            "Backend Engineer": ["DEPLOY_INFRASTRUCTURE", "MANAGE_DATABASE"],
            "CEO": ["*"] # Full authority
        }

    def can_execute(self, role: str, action: str) -> bool:
        allowed = self.role_policies.get(role, [])
        if "*" in allowed:
            return True
        return action in allowed
