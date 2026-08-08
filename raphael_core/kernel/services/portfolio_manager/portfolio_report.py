from typing import List, Dict, Any
from pathlib import Path
import json
from datetime import datetime

class PortfolioReport:
    def __init__(self):
        self.report_dir = Path(r"C:\RaphaelOS\Portfolio")
        self.report_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_report(self, allocations: Dict[str, Dict[str, Any]], businesses: List[Dict[str, Any]]) -> str:
        """
        Generates the RAPHAEL HOLDINGS REPORT with CEO-level strategic recommendations.
        """
        report_lines = [
            "🏢 RAPHAEL HOLDINGS — CEO BRIEF",
            f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            ""
        ]
        
        # Attach allocation data to each business
        for b in businesses:
            bid = b["twin"].identity["business_id"]
            if bid in allocations:
                b["score"] = allocations[bid]["score"]
                b["allocation_pct"] = allocations[bid]["allocation_pct"]
                b["pool"] = allocations[bid].get("pool", "Unknown")
            else:
                b["score"] = 0.0
                b["allocation_pct"] = 0.0
                b["pool"] = "Unknown"
                
        sorted_businesses = sorted(businesses, key=lambda x: x.get("score", 0.0), reverse=True)
        
        # --- Portfolio Overview ---
        report_lines.append("━━━ PORTFOLIO OVERVIEW ━━━")
        medals = ["🥇", "🥈", "🥉", "🏅", "🏅"]
        
        for i, b in enumerate(sorted_businesses):
            medal = medals[i] if i < len(medals) else "🔹"
            twin = b["twin"]
            name = twin.identity["name"]
            domain = twin.identity.get("domain", "unknown").title()
            state = twin.lifecycle.get_state()
            score = b["score"]
            alloc = round(b["allocation_pct"] * 100)
            pool = b.get("pool", "Unknown")
            model = twin.strategy.get("business_model", twin.identity.get("category", "unknown"))
            
            report_lines.append(f"\n{medal} {name} [{domain}]")
            report_lines.append(f"   State: {state} | Model: {model}")
            report_lines.append(f"   Score: {score:.4f} | Allocation: {alloc}% ({pool})")
            
        # --- Strategic Analysis ---
        report_lines.append("\n━━━ STRATEGIC ANALYSIS ━━━")
        
        established = [b for b in sorted_businesses if b["pool"] == "Exploitation"]
        exploring = [b for b in sorted_businesses if b["pool"] == "Exploration"]
        
        if established:
            est_total = sum(b["allocation_pct"] for b in established) * 100
            report_lines.append(f"\nExploitation Pool: {est_total:.0f}%")
            for b in established:
                report_lines.append(f"  └─ {b['twin'].identity['name']}: {round(b['allocation_pct']*100)}%")
                
        if exploring:
            exp_total = sum(b["allocation_pct"] for b in exploring) * 100
            report_lines.append(f"\nExploration Pool: {exp_total:.0f}%")
            for b in exploring:
                share = round(b["allocation_pct"] / (exp_total / 100) * 100) if exp_total > 0 else 0
                report_lines.append(f"  └─ {b['twin'].identity['name']}: {round(b['allocation_pct']*100)}% (pool share: {share}%)")
        
        # --- CEO Recommendations ---
        report_lines.append("\n━━━ CEO RECOMMENDATIONS ━━━")
        
        recommendations = self._generate_strategic_recommendations(sorted_businesses, allocations)
        for i, rec in enumerate(recommendations, 1):
            report_lines.append(f"\n{i}. {rec['action']}")
            report_lines.append(f"   Rationale: {rec['rationale']}")
            report_lines.append(f"   Priority: {rec['priority']}")
        
        report_text = "\n".join(report_lines)
        
        # Save physical artifact
        report_path = self.report_dir / f"holdings_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        report_path.write_text(report_text, encoding="utf-8")
        
        return report_text
    
    def _generate_strategic_recommendations(self, businesses, allocations):
        """
        Generates strategic CEO recommendations based on portfolio composition.
        This is not just 'pick the highest score' — it understands portfolio strategy.
        """
        recommendations = []
        
        # Identify key businesses by their strategic role
        cash_flow_engines = []
        high_upside = []
        slow_validation = []
        revenue_generators = []
        
        for b in businesses:
            twin = b["twin"]
            model = twin.strategy.get("business_model", "")
            state = twin.lifecycle.get_state()
            roi = twin.financials.get("roi", 0)
            risk = twin.risk.get("operational_risk", 0.5)
            confidence = twin.confidence
            
            # Service businesses generate immediate cash flow
            if model == "service_economy" or twin.identity.get("domain") == "agency":
                cash_flow_engines.append(b)
                
            # High ROI established businesses
            if roi > 5.0 and state == "ACTIVE":
                revenue_generators.append(b)
                
            # High strategic upside but uncertain
            if state == "INCUBATING" and confidence >= 0.60:
                high_upside.append(b)
                
            # Slow validators
            if state == "INCUBATING" and confidence < 0.50:
                slow_validation.append(b)
        
        # Recommendation 1: Cash flow engines should be funded aggressively
        for cf in cash_flow_engines:
            name = cf["twin"].identity["name"]
            recommendations.append({
                "action": f"Fund {name} aggressively",
                "rationale": f"Service economy generates fastest revenue. {name} can become the internal cash flow engine that reduces portfolio dependency on a single business.",
                "priority": "HIGH"
            })
        
        # Recommendation 2: Maintain proven revenue generators
        for rg in revenue_generators:
            name = rg["twin"].identity["name"]
            recommendations.append({
                "action": f"Maintain {name} investment — proven performer",
                "rationale": f"ROI of {rg['twin'].financials.get('roi', 0):.1f} validates the business model. Continue exploitation-level funding.",
                "priority": "HIGH"
            })
        
        # Recommendation 3: Keep high-upside ventures alive
        for hu in high_upside:
            name = hu["twin"].identity["name"]
            recommendations.append({
                "action": f"Maintain {name} exploration — high strategic upside",
                "rationale": f"Confidence at {hu['twin'].confidence:.2f}. Strategic value outweighs current risk. Continue validation missions.",
                "priority": "MEDIUM"
            })
        
        # Recommendation 4: Monitor or reduce slow validators
        for sv in slow_validation:
            name = sv["twin"].identity["name"]
            recommendations.append({
                "action": f"Monitor {name} — consider reducing allocation if validation stalls",
                "rationale": f"Confidence at {sv['twin'].confidence:.2f}. Slower validation cycle may indicate structural challenges.",
                "priority": "WATCH"
            })
            
        # Recommendation 5: Portfolio diversity insight
        domains = set(b["twin"].identity.get("domain", "") for b in businesses)
        if len(domains) >= 4:
            recommendations.append({
                "action": "Portfolio diversification achieved — maintain economic model balance",
                "rationale": f"Raphael Holdings now spans {len(domains)} economic models. No single model failure can collapse the portfolio.",
                "priority": "STRATEGIC"
            })
        
        return recommendations
    
    def generate_holdings_strategy(self, allocations: Dict[str, Dict[str, Any]], businesses: List[Dict[str, Any]]) -> str:
        """
        Generates the CEO-level holdings_strategy.md document.
        'Why does Raphael Holdings own these companies, and how should capital flow between them?'
        """
        # Attach scores
        for b in businesses:
            bid = b["twin"].identity["business_id"]
            if bid in allocations:
                b["score"] = allocations[bid]["score"]
                b["allocation_pct"] = allocations[bid]["allocation_pct"]
                b["pool"] = allocations[bid].get("pool", "Unknown")
                
        sorted_biz = sorted(businesses, key=lambda x: x.get("score", 0.0), reverse=True)
        
        lines = [
            "# RAPHAEL HOLDINGS — PORTFOLIO STRATEGY",
            "",
            f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
            "",
            "## Why Does Raphael Holdings Own These Companies?",
            "",
            "Raphael Holdings exists to build, operate, and optimize a diversified portfolio",
            "of AI-powered businesses. Each company serves a distinct economic function within",
            "the holding company, creating resilience through diversification and shared",
            "infrastructure through the Raphael OS kernel.",
            ""
        ]
        
        # Portfolio composition
        lines.append("## Portfolio Composition")
        lines.append("")
        lines.append("| Company | Division | Economic Model | Stage | Score | Capital Pool |")
        lines.append("|---------|----------|---------------|-------|-------|-------------|")
        
        for b in sorted_biz:
            twin = b["twin"]
            name = twin.identity["name"]
            domain = twin.identity.get("domain", "unknown").title()
            model = twin.strategy.get("business_model", twin.identity.get("category", "unknown"))
            state = twin.lifecycle.get_state()
            score = b.get("score", 0)
            pool = b.get("pool", "Unknown")
            lines.append(f"| {name} | {domain} | {model} | {state} | {score:.4f} | {pool} |")
            
        lines.append("")
        
        # Capital flow logic
        lines.append("## Capital Flow Strategy")
        lines.append("")
        lines.append("### Exploitation Pool (80%)")
        lines.append("Reserved for proven businesses with validated unit economics.")
        lines.append("Capital flows to businesses that have demonstrated positive ROI and")
        lines.append("reached ACTIVE lifecycle state.")
        lines.append("")
        lines.append("### Exploration Pool (20%)")
        lines.append("Reserved for incubating ventures competing on VentureScore.")
        lines.append("Capital is allocated proportionally based on evidence, not favoritism.")
        lines.append("The highest-scoring venture receives the largest share of exploration capital.")
        lines.append("")
        
        # Inter-venture synergies
        lines.append("## Inter-Venture Capital Flow")
        lines.append("")
        lines.append("The portfolio is designed so ventures can fund each other:")
        lines.append("")
        
        # Build the flow map dynamically
        for b in sorted_biz:
            twin = b["twin"]
            name = twin.identity["name"]
            domain = twin.identity.get("domain", "")
            model = twin.strategy.get("business_model", "")
            
            if domain == "creator":
                lines.append(f"- **{name}** (Attention Economy) → Generates audience and brand awareness")
                lines.append(f"  - Feeds leads to Agency and Commerce ventures")
            elif domain == "agency":
                lines.append(f"- **{name}** (Service Economy) → Generates immediate cash flow")
                lines.append(f"  - Can fund other ventures through internal revenue")
                lines.append(f"  - Lowest risk, fastest path to revenue")
            elif domain == "career":
                lines.append(f"- **{name}** (Network Effects) → Builds long-term platform value")
                lines.append(f"  - Network effects compound over time")
                lines.append(f"  - Strategic upside outweighs current uncertainty")
            elif domain == "commerce":
                lines.append(f"- **{name}** (Transaction Economy) → Generates direct product revenue")
                lines.append(f"  - Leverages AI curation for differentiation")
                lines.append(f"  - Requires longer validation for product-market fit")
        
        lines.append("")
        
        # Strategic thesis
        lines.append("## Strategic Thesis")
        lines.append("")
        lines.append("Raphael Holdings operates on three principles:")
        lines.append("")
        lines.append("1. **No single point of failure.** Four economic models ensure that if one")
        lines.append("   sector contracts, the portfolio survives.")
        lines.append("")
        lines.append("2. **Evidence-based capital allocation.** The Portfolio Manager allocates")
        lines.append("   resources based on VentureScore, not preference. Every venture competes")
        lines.append("   on merit within its pool.")
        lines.append("")
        lines.append("3. **AI-powered operations.** Every venture leverages AI agents for execution,")
        lines.append("   reducing operational cost and enabling scale without proportional headcount.")
        lines.append("")
        
        # Decision framework
        lines.append("## Capital Decision Framework")
        lines.append("")
        lines.append("| Signal | Action |")
        lines.append("|--------|--------|")
        lines.append("| VentureScore > 0.70 + ACTIVE state | Increase exploitation allocation |")
        lines.append("| VentureScore > 0.50 + INCUBATING | Continue exploration funding |")
        lines.append("| VentureScore < 0.30 after 30 days | Escalate to CEO for pivot/kill decision |")
        lines.append("| Service venture generating MRR | Redirect surplus to exploration pool |")
        lines.append("| Two ventures share infrastructure | Explore merger or shared services |")
        lines.append("")
        
        strategy_text = "\n".join(lines)
        
        strategy_path = self.report_dir / "holdings_strategy.md"
        strategy_path.write_text(strategy_text, encoding="utf-8")
        
        return strategy_text
