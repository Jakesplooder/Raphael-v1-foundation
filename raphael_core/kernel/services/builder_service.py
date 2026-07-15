import re
from datetime import datetime
from typing import Dict, Any, List

from ..models.builder import BuildRequest, BuildClassification
from ..repositories.builder_repository import MarkdownBuildRepository

class BuilderService:
    """
    Handles business logic for the Builder subsystem, isolated from persistence and execution.
    """
    def __init__(self, repository: MarkdownBuildRepository):
        self.repository = repository

    def process_request(self, description: str, metadata: Dict[str, Any] = None) -> BuildRequest:
        req = BuildRequest(description=description, metadata=metadata or {})
        self.repository.save_request(req)
        return req

    def _build_external_risk_flags(self, description: str) -> List[str]:
        lowered = description.lower()
        rules = [
            ("payments", ["payment", "payments", "stripe", "billing", "checkout", "subscription"]),
            ("external APIs", ["external api", "third-party api", "openai api", "google api", "shopify api", "etsy api"]),
            ("publishing/deployment", ["publish", "deploy", "production", "app store", "launch"]),
            ("client delivery", ["client", "customer delivery", "agency"]),
            ("user data/authentication", ["users", "login", "authentication", "accounts", "personal data"]),
            ("commerce platforms", ["shopify", "etsy", "amazon", "printify", "woocommerce", "marketplace"]),
            ("revenue/business risk", ["revenue", "make money", "monetize", "saas", "business", "sell"]),
        ]
        return [label for label, terms in rules if any(term in lowered for term in terms)]

    def classify_request(self, request: BuildRequest) -> BuildClassification:
        clean = request.description.strip()
        lowered = clean.lower()
        
        high_terms = [
            "saas", "marketplace", "agency client", "client app", "shopify", "etsy", "automation",
            "ai product", "make money", "monetize", "revenue", "payments", "payment", "stripe",
            "external api", "publishing", "publish", "deploy", "customer", "multi-tenant", "subscription",
        ]
        medium_terms = [
            "dashboard", "crud", "portfolio app", "internal tool", "api-backed", "api backed",
            "database", "backend", "frontend app", "multi-file", "multi page", "multi-page",
            "admin", "authentication", "login", "users", "prototype",
        ]
        low_terms = [
            "click counter", "calculator", "static landing page", "landing page", "basic form",
            "simple form", "small python script", "one-file", "one file", "utility", "button click",
        ]
        risks = self._build_external_risk_flags(clean)
        
        if any(term in lowered for term in high_terms) or {"payments", "external APIs", "commerce platforms"} & set(risks):
            level, label = 3, "High"
        elif any(term in lowered for term in medium_terms):
            level, label = 2, "Medium"
        elif any(term in lowered for term in low_terms):
            level, label = 1, "Low"
        else:
            level, label = 1, "Low" # Default fallback
            
        councils: List[str] = []
        if level >= 2:
            councils += ["Research Council", "Operations Council"]
        if risks or level >= 3:
            councils.append("Governance Council")
        if level >= 3:
            councils += ["Executive Council", "Portfolio Council", "Financial Council"]
            if any(term in lowered for term in ["agency", "client", "service"]):
                councils.append("Agency Council")
            if any(term in lowered for term in ["shopify", "etsy", "commerce", "marketplace", "product", "pod"]):
                councils.append("Commerce Council")
            if any(term in lowered for term in ["content", "media", "creator", "video", "podcast"]):
                councils.append("Creator Council")
                
        councils = list(dict.fromkeys(councils))
        
        build_type = (
            "Business / Strategic Application" if level == 3 else
            "Product Application" if level == 2 else 
            "Utility"
        )
        
        route = {
            1: "Developer Agent + Builder workspace generation",
            2: "Technical/product review, tracked task, then confirmed Builder generation",
            3: "Opportunity, council deliberation, execution plan, tracked task, then plan approval",
        }[level]
        
        classification = BuildClassification(
            request_id=request.id,
            complexity_level=level,
            complexity_label=label,
            build_type=build_type,
            recommended_route=route,
            required_councils=councils,
            external_risk_flags=risks
        )
        
        self.repository.save_classification(classification)
        return classification

    def get_workflow_templates(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Returns the registered Workflow Templates for the Builder.
        Defines the execution modes (Draft, Assisted, Autonomous) enforcing the FSM.
        """
        draft_phases = [
            {"name": "Scaffold Workspace", "action": "SCAFFOLD", "provider": "local_builder"},
            {"name": "Scan Workspace", "action": "SCAN", "provider": "local_builder"},
            {"name": "Generate Code", "action": "GENERATE", "provider": "local_builder"},
            {"name": "Update CodeGraph", "action": "UPDATE_GRAPH", "provider": "local_builder"}
        ]
        
        assisted_phases = draft_phases + [
            {"name": "Layered Validation", "action": "VALIDATE", "provider": "local_builder"},
            {"name": "Initial Compile", "action": "COMPILE", "provider": "local_builder"},
            {"name": "Code Review", "action": "REVIEW", "provider": "local_builder"},
            {"name": "Await Human Approval", "action": "AWAIT_APPROVAL", "provider": "system"}
        ]
        
        autonomous_phases = draft_phases + [
            {"name": "Layered Validation", "action": "VALIDATE", "provider": "local_builder"},
            {"name": "Initial Compile", "action": "COMPILE", "provider": "local_builder"},
            {"name": "Autonomous Patching", "action": "PATCH", "provider": "local_builder"},
            {"name": "Final Compile", "action": "COMPILE", "provider": "local_builder"},
            {"name": "Code Review", "action": "REVIEW", "provider": "local_builder"},
            {"name": "Commit Changes", "action": "COMMIT", "provider": "local_builder"},
            {"name": "Archive Artifacts", "action": "ARCHIVE", "provider": "local_builder"}
        ]
        
        return {
            "Builder Draft Workflow": draft_phases,
            "Builder Assisted Workflow": assisted_phases,
            "Builder Autonomous Workflow": autonomous_phases
        }
