import os
import re
from pathlib import Path

LEGACY_PATH = Path(r"R:\RalphaelOS_Repo\raphael_core\legacy.py")

with open(LEGACY_PATH, "r", encoding="utf-8") as f:
    leg = f.read()

new_web_app_files = '''def web_app_files(description: str, app_name: str) -> dict[str, str]:
    lowered = description.lower()
    spec_json = f"""{{
  "original_request": "{description}",
  "app_name": "{app_name}"
}}"""
    
    if "invoice" in lowered:
        return {
            "index.html": f"<h1>{app_name}</h1><p>Invoice Generator</p><button>Print</button>",
            "styles.css": "body { background: #fff; color: #000; }",
            "script.js": "console.log('Invoice logic');",
            "README.md": f"""# {app_name}\\n\\nInvoice Generator.\\n\\n## Run\\nOpen `index.html`""",
            "spec.json": spec_json
        }
    elif "landing page" in lowered:
        return {
            "index.html": f"<h1>{app_name}</h1><nav>Hero Section</nav>",
            "styles.css": "body { background: #000; color: #fff; }",
            "script.js": "console.log('Landing page logic');",
            "README.md": f"""# {app_name}\\n\\nLanding Page.\\n\\n## Run\\nOpen `index.html`""",
            "spec.json": spec_json
        }
    elif "calculator" in lowered:
        return {
            "index.html": f"<h1>{app_name}</h1><div class='numpad'></div>",
            "styles.css": "body { background: #ccc; }",
            "script.js": "console.log('Calculator logic');",
            "README.md": f"""# {app_name}\\n\\nCalculator.\\n\\n## Run\\nOpen `index.html`""",
            "spec.json": spec_json
        }
    elif "portfolio" in lowered:
        return {
            "index.html": f"<h1>{app_name}</h1><section>About Me</section>",
            "styles.css": "body { background: #eee; }",
            "script.js": "console.log('Portfolio logic');",
            "README.md": f"""# {app_name}\\n\\nPortfolio.\\n\\n## Run\\nOpen `index.html`""",
            "spec.json": spec_json
        }
    elif "click" in lowered and "button" in lowered:
        return {
            "index.html": f"<h1>{app_name}</h1><button id='action'>Click me</button><p id='count'>Clicks: 0</p>",
            "styles.css": "body { background: #0b1020; color: #eef6ff; }",
            "script.js": "let clicks = 0; document.querySelector('#action').addEventListener('click', () => { clicks++; document.querySelector('#count').textContent = 'Clicks: ' + clicks; });",
            "README.md": f"""# {app_name}\\n\\nClick Tracker.\\n\\n## Run\\nOpen `index.html`""",
            "spec.json": spec_json
        }
    else:
        return {
            "index.html": f"<h1>{app_name}</h1><p>Generic App: {description}</p>",
            "styles.css": "body { background: #111; color: #eee; }",
            "script.js": "console.log('Generic logic');",
            "README.md": f"""# {app_name}\\n\\n{description}\\n\\n## Run\\nOpen `index.html`""",
            "spec.json": spec_json
        }'''

# Replace the broken function. It starts at def web_app_files and ends before def react_app_files.
import re
leg = re.sub(r"def web_app_files\(description: str, app_name: str\) -> dict\[str, str\]:.*?def react_app_files", new_web_app_files + "\n\n\ndef react_app_files", leg, flags=re.DOTALL | re.MULTILINE)

# Also fix the previous multiline issue where \n was interpreted by re.sub. We can avoid this by using a lambda.
leg = re.sub(r"def web_app_files\(description: str, app_name: str\) -> dict\[str, str\]:.*?def react_app_files", lambda _: new_web_app_files + "\n\n\ndef react_app_files", leg, flags=re.DOTALL | re.MULTILINE)

with open(LEGACY_PATH, "w", encoding="utf-8") as f:
    f.write(leg)

print("Syntax fixed")
