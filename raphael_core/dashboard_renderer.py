from typing import Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.table import Table
from rich.align import Align

def _format_staleness(st: str) -> str:
    if st == "stale":
        return "[yellow]! Data stale[/yellow]"
    if st in ("missing", "error"):
        return "[red]! Unavailable[/red]"
    return ""

def render_dashboard(data: Dict[str, Any]):
    console = Console()
    
    # Create the root layout
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main"),
        Layout(name="footer", size=5)
    )
    
    layout["main"].split_row(
        Layout(name="left_panel", ratio=1),
        Layout(name="right_panel", ratio=1)
    )
    
    layout["right_panel"].split_column(
        Layout(name="metrics", ratio=1),
        Layout(name="portfolio", ratio=1)
    )

    # Header
    health_score = data["health"]["overall"]
    health_color = "green" if health_score >= 90 else "yellow" if health_score >= 70 else "red"
    header_text = f"RAPHAEL OS — Executive Dashboard\n[dim]{data['timestamp']}[/dim]    Health: [{health_color}]{health_score}%[/{health_color}]    v1.5"
    layout["header"].update(Panel(header_text, style="bold cyan"))
    
    # Left Panel: Executive Status
    init_text = Text()
    init_text.append("TODAY'S FOCUS\n", style="bold")
    if not data["initiatives"]:
        init_text.append("  No initiatives currently queued.\n", style="dim")
    else:
        for i, init in enumerate(data["initiatives"], 1):
            init_text.append(f"  {i}. {init.get('title', 'Unknown')}\n")
            
    init_text.append("\nALERTS\n", style="bold")
    # Determine if any critical risks exist (in real app, we scan initiatives for type=risk and high priority)
    risks = [r for r in data["initiatives"] if r.get("type") == "risk"]
    if risks:
        init_text.append(f"  ! {len(risks)} critical risk(s) detected\n", style="red")
    else:
        init_text.append("  OK No critical risks\n", style="green")
        
    const_score = data["health"]["components"]["constitutional"]["score"]
    if const_score == 100:
        init_text.append("  OK No constitutional violations\n", style="green")
    else:
        init_text.append("  ! Constitutional violation recorded\n", style="red")
        
    layout["left_panel"].update(Panel(init_text, title="Executive Status", border_style="blue"))
    
    # Right Panel 1: Operational Metrics
    metrics_table = Table.grid(padding=(0, 2))
    metrics_table.add_column(style="bold")
    metrics_table.add_column()
    metrics_table.add_column()
    
    wm = data["world_model"]
    metrics_table.add_row("WORLD MODEL", f"Nodes: {wm['nodes']}  Rels: {wm['rels']}", _format_staleness(wm['staleness']))
    
    lr = data["learning"]
    metrics_table.add_row("LEARNING", f"Accuracy: {lr['accuracy']}% {lr['trend']}", _format_staleness(lr['staleness']))
    
    llm = data["llm_spend"]
    metrics_table.add_row("LLM SPEND", f"Week: ${llm['spend']:.2f}  Avoidable: {llm['avoidable_pct']:.0f}%", _format_staleness(llm['staleness']))
    
    wf = data["workforce"]
    metrics_table.add_row("AGENTS", f"Active: {wf['active']}  Overloaded: {wf['overloaded']}", _format_staleness(wf['staleness']))
    
    work = data["workflows"]
    metrics_table.add_row("WORKFLOWS", f"Queue: {work['queue']}  Blocked: {work['blocked']}", _format_staleness(work['staleness']))
    
    layout["metrics"].update(Panel(metrics_table, title="Operational Metrics", border_style="magenta"))
    
    # Right Panel 2: Portfolio View
    port_text = Text()
    port_text.append("ACTIVE PROJECTS\n", style="bold")
    for proj in data["portfolio"]["projects"]:
        port_text.append(f"  {proj['name']:<15} {proj['status']}\n")
    
    port_text.append("\nCRITICAL PATH BLOCKERS\n", style="bold")
    for block in data["portfolio"]["blockers"]:
        port_text.append(f"  {block}\n")
        
    layout["portfolio"].update(Panel(port_text, title="Portfolio View", border_style="yellow"))
    
    # Footer: Drill-down instructions
    footer_text = (
        "[dim][Press 1 for initiative detail: python raphael.py initiative-status]\n"
        "[Press W for weekly summary: python raphael.py generate-weekly-summary]\n"
        "[Press F for forecast: python raphael.py capacity-forecast PROJECT-ID][/dim]"
    )
    layout["footer"].update(Align.center(footer_text))
    
    console.print(layout)
