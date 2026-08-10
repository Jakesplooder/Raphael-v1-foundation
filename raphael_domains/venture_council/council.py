import json
from pathlib import Path
from typing import Dict, Any, List
from raphael_core.kernel.event_bus import emit
from raphael_core.kernel.services.business_registry.proposals.proposal import BusinessProposal

# Per-domain evaluation profiles
# Each council agent scores independently based on the proposal's characteristics
EVALUATION_PROFILES = {
    "career_technology": {
        "market_opportunity": 0.85,
        "strategic_alignment": 0.90,
        "revenue_potential": 0.75,
        "execution_feasibility": 0.80,
        "technical_advantage": 0.70,
        "risk": 0.40,
        "risks": ["market saturation", "mentor acquisition difficulty"],
        "success_metrics": ["100 landing page signups", "10 mentor interviews", "5 beta users"]
    },
    "commerce_technology": {
        "market_opportunity": 0.90,
        "strategic_alignment": 0.85,
        "revenue_potential": 0.80,
        "execution_feasibility": 0.75,
        "technical_advantage": 0.65,
        "risk": 0.35,
        "risks": ["customer acquisition cost uncertainty", "supplier reliability", "inventory management complexity"],
        "success_metrics": ["50 product listings", "10 validated suppliers", "first 5 sales transactions"]
    },
    "agency_services": {
        "market_opportunity": 0.80,
        "strategic_alignment": 0.75,
        "revenue_potential": 0.85,
        "execution_feasibility": 0.85,
        "technical_advantage": 0.60,
        "risk": 0.30,
        "risks": ["talent dependency", "client concentration risk"],
        "success_metrics": ["3 paying clients", "positive unit economics", "repeatable delivery process"]
    }
}

# Default fallback for unknown categories
DEFAULT_PROFILE = {
    "market_opportunity": 0.50,
    "strategic_alignment": 0.50,
    "revenue_potential": 0.50,
    "execution_feasibility": 0.50,
    "technical_advantage": 0.50,
    "risk": 0.50,
    "risks": ["unknown market dynamics"],
    "success_metrics": ["initial traction metrics TBD"]
}


class VentureCouncil:
    """
    The Venture Council evaluates business proposals through four simulated agents:
    - Market Research Agent: Evaluates demand, competition, unique advantage
    - Product Agent: Evaluates MVP difficulty, technical requirements
    - Finance Agent: Evaluates startup cost, CAC, gross margin, revenue potential
    - Strategy Agent: Evaluates portfolio fit, infrastructure sharing, automation potential
    
    Output: Investment Memo with VentureScore and recommendation.
    """
    
    def evaluate_proposal(self, proposal: BusinessProposal) -> Dict[str, Any]:
        """
        Evaluates a proposal through the council pipeline.
        Each proposal receives scores based on its category profile.
        """
        emit("BUSINESS.EVALUATION_STARTED", "VentureCouncil", {"venture": proposal.name})
        
        # Look up evaluation profile by category
        profile = EVALUATION_PROFILES.get(proposal.category, DEFAULT_PROFILE)
        
        market_opp = profile["market_opportunity"]
        strategic_align = profile["strategic_alignment"]
        revenue_pot = profile["revenue_potential"]
        exec_feasibility = profile["execution_feasibility"]
        tech_adv = profile["technical_advantage"]
        risk = profile["risk"]
        
        # VentureScore formula
        score = (
            (market_opp * 0.25) +
            (strategic_align * 0.20) +
            (revenue_pot * 0.20) +
            (exec_feasibility * 0.15) +
            (tech_adv * 0.10) -
            (risk * 0.10)
        )
        score = round(score, 4)
        
        recommendation = "INCUBATE" if score > 0.60 else "REJECT"
        
        # Generate Investment Memo artifact
        memo_dir = Path(r"R:\RaphaelOS\Ventures") / proposal.name.replace(" ", "")
        memo_dir.mkdir(parents=True, exist_ok=True)
        
        # Market Agent assessment
        market_verdict = "PASS" if market_opp >= 0.60 else "CAUTION"
        # Product Agent assessment
        product_verdict = "PASS" if exec_feasibility >= 0.60 else "CAUTION"
        # Finance Agent assessment
        finance_verdict = "PASS" if revenue_pot >= 0.60 else "CAUTION"
        # Strategy Agent assessment
        alignment_count = sum(1 for v in proposal.strategic_alignment.values() if v)
        strategy_verdict = "HIGH" if alignment_count >= 2 else "MEDIUM" if alignment_count >= 1 else "LOW"
        
        memo_content = f"""# {proposal.name.upper()} INVESTMENT MEMO
==========================

## Executive Summary
Problem: {proposal.problem}
Solution: {proposal.solution}
Target Customer: {proposal.target_customer}

## Council Evaluation

### Market Research Agent
Verdict: {market_verdict}
Market Opportunity Score: {market_opp}
Questions Evaluated:
- Is there demand? {"Yes" if market_opp >= 0.70 else "Moderate"}
- Is competition saturated? {"No — opportunity exists" if market_opp >= 0.70 else "Moderate competition"}
- Is there a unique advantage? {"Yes — AI-powered differentiation" if tech_adv >= 0.60 else "Unclear"}

### Product Agent
Verdict: {product_verdict}
Execution Feasibility: {exec_feasibility}
Technical Advantage: {tech_adv}
Product Type: {proposal.type}
MVP Difficulty: {"Low" if exec_feasibility >= 0.80 else "Medium" if exec_feasibility >= 0.60 else "High"}

### Finance Agent
Verdict: {finance_verdict}
Revenue Potential: {revenue_pot}
Revenue Model: {', '.join(proposal.revenue_model)}
Requested Budget: ${proposal.initial_resources_requested.get('budget', 0)}
Estimated Break-even: {"6-12 months" if revenue_pot >= 0.80 else "12-18 months" if revenue_pot >= 0.60 else "18+ months"}

### Strategy Agent
Verdict: {strategy_verdict}
Strategic Alignment: {strategic_align}
Portfolio Synergy: {alignment_count}/{len(proposal.strategic_alignment)} alignment factors met
Does this strengthen Raphael Holdings? {"Yes" if strategic_align >= 0.70 else "Partially"}
Can Raphael automate operations? {"Yes — AI advantage confirmed" if proposal.strategic_alignment.get("ai_advantage", False) else "Partially"}

## Final Assessment
VentureScore: {score}
Recommendation: {recommendation}
Risks: {', '.join(profile['risks'])}

## Resource Request
{json.dumps(proposal.initial_resources_requested, indent=2)}
"""
        # Append thesis section if provided
        if proposal.thesis:
            thesis_section = f"""
## Venture Thesis
Belief: {proposal.thesis.belief}

Core Assumptions:
{chr(10).join('- ' + a for a in proposal.thesis.assumptions)}

Risk Assumptions:
{chr(10).join('- ' + a for a in proposal.thesis.risk_assumptions)}
"""
            memo_content += thesis_section
            # Save thesis as a separate first-class artifact
            thesis_data = proposal.thesis.to_dict()
            thesis_data["venture"] = proposal.name
            (memo_dir / "thesis.json").write_text(json.dumps(thesis_data, indent=2))
        (memo_dir / "investment_memo.md").write_text(memo_content, encoding="utf-8")
        
        council_votes = {
            "venture": proposal.name,
            "recommendation": recommendation,
            "confidence": score,
            "requested_budget": proposal.initial_resources_requested.get("budget", 500),
            "expected_validation_days": 30,
            "evaluation": {
                "market_opportunity": market_opp,
                "strategic_alignment": strategic_align,
                "revenue_potential": revenue_pot,
                "execution_feasibility": exec_feasibility,
                "technical_advantage": tech_adv,
                "risk": risk
            },
            "agent_verdicts": {
                "market": market_verdict,
                "product": product_verdict,
                "finance": finance_verdict,
                "strategy": strategy_verdict
            },
            "risks": profile["risks"],
            "success_metrics": profile["success_metrics"]
        }
        if proposal.thesis:
            council_votes["thesis"] = proposal.thesis.to_dict()
        (memo_dir / "council_votes.json").write_text(json.dumps(council_votes, indent=2))
        (memo_dir / "proposal.json").write_text(json.dumps(proposal.to_dict(), indent=2))
        
        emit("BUSINESS.EVALUATION_COMPLETED", "VentureCouncil", {
            "venture": proposal.name,
            "score": score,
            "recommendation": recommendation,
            "agent_verdicts": council_votes["agent_verdicts"]
        })
        emit("VENTURE.INVESTMENT_MEMO_CREATED", "VentureCouncil", {
            "venture": proposal.name,
            "score": score,
            "path": str(memo_dir / "investment_memo.md")
        })
        
        return council_votes

venture_council = VentureCouncil()
