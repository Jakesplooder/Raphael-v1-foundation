import sys
import os
import json
from datetime import datetime

if '/app/repo' not in sys.path:
    sys.path.insert(0, '/app/repo')

class BusinessRegistry:
    def get_business(self, id):
        path = f"/app/runtime/businesses/{id}.json"
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}
    
    def get_ceo_brief(self):
        current_hour = datetime.now().hour
        if current_hour < 12:
            greeting = "Good Morning, Aaron"
        elif current_hour < 18:
            greeting = "Good Afternoon, Aaron"
        else:
            greeting = "Good Evening, Aaron"

        biz_data = self.get_business("focus-marketing")
        scorecard = self.get_scorecard("focus-marketing")
        inbox = self.get_inbox()
        opportunities = self.get_opportunities()
        
        business_info = {
            "name": biz_data.get("name", "Focus Marketing"),
            "icon": biz_data.get("icon", "📈"),
            "revenue_today": biz_data.get("revenue_today", 0),
            "revenue_7d": biz_data.get("revenue_7d", 0),
            "affiliate_clicks": biz_data.get("affiliate_clicks", 0),
            "videos_published": biz_data.get("videos_published", 0),
            "experiments_running": biz_data.get("experiments_running", 3),
            "blocked_missions": biz_data.get("blocked_missions", 1),
            "active_missions": biz_data.get("active_missions", 12),
            "health": biz_data.get("health", 72)
        }
        
        recommendations = [
            {"title": "Increase publishing cadence", "detail": "3→5 shorts/day", "expected_impact": "+$40/week"}
        ]
        
        return {
            "greeting": greeting,
            "business": business_info,
            "scorecard": scorecard,
            "inbox": inbox,
            "recommendations": recommendations,
            "opportunities": opportunities
        }
        
    def get_scorecard(self, business_id):
        return [
            {"label": "Traffic", "score": 45, "trend": "flat"},
            {"label": "Content Output", "score": 62, "trend": "up"},
            {"label": "Conversion Rate", "score": 88, "trend": "up"}
        ]
        
    def get_inbox(self):
        inbox = []
        try:
            from raphael_core.operator.initiative_manager import get_active_initiatives
            initiatives = get_active_initiatives()
            for init in initiatives:
                tasks = init.get("tasks", [])
                for task in tasks:
                    status = task.get("status", "").upper()
                    if status == "PENDING" or "approval" in task.get("type", "").lower():
                        inbox.append({
                            "id": task.get("id", str(len(inbox))),
                            "type": "approval",
                            "title": task.get("title", f"Approve task in {init.get('name', 'Initiative')}"),
                            "detail": task.get("detail", "Requires review"),
                            "actions": ["approve", "modify", "reject"]
                        })
        except Exception:
            pass
            
        try:
            from raphael_core.councils.engine import get_recent_decisions
            decisions = get_recent_decisions()
            for dec in decisions:
                rec = dec.get("recommendation", "").upper()
                if rec in ["DEFER", "MODIFY"]:
                    inbox.append({
                        "id": dec.get("id", str(len(inbox))),
                        "type": "decision",
                        "title": dec.get("title", "Council Decision Requires Review"),
                        "detail": dec.get("reason", "Council suggested defer/modify"),
                        "actions": ["approve", "modify", "reject"]
                    })
        except Exception:
            pass
            
        return inbox
        
    def get_opportunities(self):
        path = "/app/runtime/businesses/opportunities.json"
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        
        return [
            {"title": "Pinterest niche: Home office setups", "potential": "$300-$800/month", "confidence": 72},
            {"title": "YouTube Shorts: Coding tutorials", "potential": "$500-$1000/month", "confidence": 85},
            {"title": "TikTok: Tech gadgets reviews", "potential": "$200-$600/month", "confidence": 60}
        ]

business_registry = BusinessRegistry()
