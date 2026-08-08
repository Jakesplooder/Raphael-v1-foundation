from typing import Dict, Any

class EmbedBuilder:
    @staticmethod
    def build_decision_pending(payload: Dict[str, Any]) -> str:
        return (
            "🚨 **Approval Required**\n\n"
            f"**Decision:** {payload.get('decision_id', 'Unknown')}\n"
            f"**Action:** {payload.get('proposal', 'Unknown Proposal')}\n"
            f"**Business:** {payload.get('business_id', 'Unknown')}\n"
            f"**Expected Return:** {payload.get('expected_return', 'N/A')}\n"
            f"**Risk Level:** {payload.get('risk_level', 'Unknown')}\n\n"
            "[Approve]\n[Reject]"
        )

    @staticmethod
    def build_experiment_completed(payload: Dict[str, Any]) -> str:
        return (
            "🔬 **Experiment Completed**\n\n"
            f"**Experiment:** {payload.get('experiment_id', 'Unknown')}\n"
            f"**Target:** {payload.get('target_asset_id', 'Unknown')}\n"
            f"**Winner:** {payload.get('winner', 'Unknown')}\n"
            f"**Result:** {payload.get('result_summary', 'N/A')}\n"
            f"**Recommendation:** {payload.get('recommendation', 'None')}"
        )

    @staticmethod
    def build_optimization_completed(payload: Dict[str, Any]) -> str:
        return (
            "📈 **Optimization Completed**\n\n"
            f"**Asset:** {payload.get('asset_id', 'Unknown')}\n"
            f"**Diagnosis:** {payload.get('diagnosis', 'Unknown')}\n"
            f"**Experiment:** {payload.get('experiment_id', 'Unknown')}\n"
            f"**Status:** {payload.get('status', 'Unknown')}"
        )
        
    @staticmethod
    def build_generic(event_type: str, payload: Dict[str, Any]) -> str:
        lines = [f"**Event:** {event_type}\n"]
        for k, v in payload.items():
            lines.append(f"**{k}:** {v}")
        return "\n".join(lines)
