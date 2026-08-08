import os
import json
import shutil
import datetime
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional

from raphael_core.kernel.event_bus import emit

class MissionContext:
    def __init__(self, mission_id: str, brand_id: str, active_dir: Path):
        self.mission_id = mission_id
        self.brand_id = brand_id
        self.active_dir = active_dir
        
        self.research_dir = active_dir / "research"
        self.content_dir = active_dir / "content"
        self.qa_dir = active_dir / "qa"
        self.publishing_dir = active_dir / "publishing"
        
        # Ensure subdirectories exist
        for d in [self.research_dir, self.content_dir, self.qa_dir, self.publishing_dir]:
            os.makedirs(d, exist_ok=True)
            
        self.reasoning_trace = {
            "mission": f"{brand_id} #{mission_id}",
            "objective": "Pending",
            "decisions": []
        }

class MissionArtifactPipeline:
    def __init__(self, os_root: Path = Path(r"C:\RaphaelOS")):
        self.os_root = os_root
        self.missions_root = self.os_root / "Missions"
        
        self.active_dir = self.missions_root / "Active"
        self.review_ready_dir = self.missions_root / "Review" / "Ready"
        self.review_approved_dir = self.missions_root / "Review" / "Approved"
        self.review_rejected_dir = self.missions_root / "Review" / "Rejected"
        self.review_needs_revision_dir = self.missions_root / "Review" / "Needs_Revision"
        self.archive_dir = self.missions_root / "Archive"
        self.reports_dir = self.missions_root / "Reports"
        self.evidence_dir = self.os_root / "Evidence"
        
        self._ensure_structure()

    def _ensure_structure(self):
        dirs = [
            self.active_dir, self.review_ready_dir, self.review_approved_dir,
            self.review_rejected_dir, self.review_needs_revision_dir,
            self.archive_dir, self.reports_dir,
            self.evidence_dir / "Metrics",
            self.evidence_dir / "Quality",
            self.evidence_dir / "Learning"
        ]
        for d in dirs:
            os.makedirs(d, exist_ok=True)

    def start_mission(self, mission_id: str, brand_id: str, objective: str) -> MissionContext:
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        folder_name = f"{date_str}_{brand_id}_{mission_id}"
        mission_dir = self.active_dir / folder_name
        
        os.makedirs(mission_dir, exist_ok=True)
        
        ctx = MissionContext(mission_id, brand_id, mission_dir)
        ctx.reasoning_trace["objective"] = objective
        
        # Write initial mission.json and objective.md
        mission_info = {
            "mission_id": mission_id,
            "brand_id": brand_id,
            "status": "ACTIVE",
            "started_at": datetime.datetime.now().isoformat()
        }
        (mission_dir / "mission.json").write_text(json.dumps(mission_info, indent=2))
        (mission_dir / "objective.md").write_text(f"# Objective\n\n{objective}")
        
        emit("MISSION.CREATED", "MissionArtifactPipeline", {"mission_id": mission_id, "brand_id": brand_id})
        
        return ctx

    def log_decision(self, ctx: MissionContext, decision: str, confidence: float, evidence: List[str]):
        ctx.reasoning_trace["decisions"].append({
            "decision": decision,
            "confidence": confidence,
            "evidence": evidence
        })
        self._save_reasoning_trace(ctx)

    def _save_reasoning_trace(self, ctx: MissionContext):
        trace_path = ctx.active_dir / "reasoning_trace.json"
        trace_path.write_text(json.dumps(ctx.reasoning_trace, indent=2))

    def write_artifact(self, ctx: MissionContext, category: str, filename: str, content: str, is_binary: bool = False):
        """
        category: 'research', 'content', 'qa', 'publishing'
        """
        target_dir = getattr(ctx, f"{category}_dir")
        file_path = target_dir / filename
        
        if is_binary:
            # Assuming content is bytes or we just copy if it's a file path
            if isinstance(content, str) and os.path.exists(content):
                shutil.copy2(content, file_path)
            elif isinstance(content, bytes):
                file_path.write_bytes(content)
        else:
            file_path.write_text(str(content), encoding="utf-8")
            
        emit("MISSION.ARTIFACT_GENERATED", "MissionArtifactPipeline", {
            "mission_id": ctx.mission_id, 
            "category": category, 
            "filename": filename
        })
        
        if category == "qa":
            emit("MISSION.QA_COMPLETED", "MissionArtifactPipeline", {"mission_id": ctx.mission_id})

    def generate_report(self, ctx: MissionContext, stats: Dict[str, Any]):
        """
        stats expected keys:
        - status: "SUCCESS" | "FAILED"
        - duration: str (e.g. "02:14")
        - agents_used: list of str
        - artifact_status: dict (e.g. {"Video": "PASS", "Thumbnail": "PASS"})
        - qa_score: str
        - risk_publishing: str
        - risk_approval: str
        - learning_improvements: list of str
        """
        report_lines = [
            f"Mission: {ctx.brand_id} #{ctx.mission_id}",
            "",
            "Execution:",
            "-------------",
            f"Status: {stats.get('status', 'UNKNOWN')}",
            f"Duration: {stats.get('duration', '00:00')}",
            "",
            "Agents Used:",
            "-------------",
        ]
        
        for agent in stats.get("agents_used", []):
            report_lines.append(agent)
            
        report_lines.extend([
            "",
            "Artifacts:",
            "-------------",
        ])
        
        for art, stat in stats.get("artifact_status", {}).items():
            report_lines.append(f"{art}: {stat}")
            
        report_lines.extend([
            "",
            "Quality:",
            "-------------",
            f"AI QA Score: {stats.get('qa_score', 'N/A')}",
            "Human Review: Pending",
            "",
            "Risk:",
            "-------------",
            f"External publishing: {stats.get('risk_publishing', 'BLOCKED')}",
            f"Approval required: {stats.get('risk_approval', 'YES')}",
            "",
            "Learning:",
            "-------------",
            "Potential improvements:"
        ])
        
        for imp in stats.get("learning_improvements", []):
            report_lines.append(f"- {imp}")
            
        report_path = ctx.active_dir / "mission_report.txt"
        report_path.write_text("\n".join(report_lines))

    def generate_review_template(self, ctx: MissionContext):
        review_data = {
            "mission_id": ctx.mission_id,
            "reviewer": "Pending",
            "decision": "pending",
            "scores": {
                "video_quality": 0,
                "thumbnail_quality": 0,
                "accuracy": 0,
                "creativity": 0,
                "publish_ready": 0
            },
            "issues": [],
            "lessons": []
        }
        review_path = ctx.active_dir / "review.json"
        review_path.write_text(json.dumps(review_data, indent=2))
        
    def generate_artifact_manifest(self, ctx: MissionContext):
        manifest = {
            "mission_id": ctx.mission_id,
            "files": []
        }
        
        for root, _, files in os.walk(ctx.active_dir):
            for file in files:
                # Don't hash the manifest itself if it were to exist
                if file == "artifact_manifest.json": continue
                
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, ctx.active_dir)
                
                with open(filepath, "rb") as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
                    
                manifest["files"].append({
                    "path": rel_path.replace("\\", "/"),
                    "sha256": file_hash
                })
                
        manifest_path = ctx.active_dir / "artifact_manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2))

    def complete_mission(self, ctx: MissionContext):
        """
        Moves the mission from Active to Review/Ready.
        """
        # Ensure reasoning trace is saved one last time
        self._save_reasoning_trace(ctx)
        
        # Generate phase 4 artifacts
        self.generate_review_template(ctx)
        self.generate_artifact_manifest(ctx)
        
        # Update mission.json status
        mission_json_path = ctx.active_dir / "mission.json"
        if mission_json_path.exists():
            data = json.loads(mission_json_path.read_text())
            data["status"] = "REVIEW_READY"
            data["completed_at"] = datetime.datetime.now().isoformat()
            mission_json_path.write_text(json.dumps(data, indent=2))
            
        folder_name = ctx.active_dir.name
        target_dir = self.review_ready_dir / folder_name
        
        # Move the directory
        shutil.move(str(ctx.active_dir), str(target_dir))
        
        # Update the context path just in case
        ctx.active_dir = target_dir
        
        emit("MISSION.REVIEW_REQUIRED", "MissionArtifactPipeline", {"mission_id": ctx.mission_id, "folder": str(target_dir)})
