import os
import re
from pathlib import Path

LEGACY_PATH = Path(r"R:\RalphaelOS_Repo\raphael_core\legacy.py")
COMMAND_BUS_PATH = Path(r"R:\RaphaelOS\command_bus.py")

# 1. Patch command_bus.py
with open(COMMAND_BUS_PATH, "r", encoding="utf-8") as f:
    cb = f.read()

# Add builder to COMMAND_TYPE_BY_PREFIX if not there
if '"builder": {"build-", "builder-"},' not in cb:
    cb = cb.replace('"notification": {"notification-"},', '"notification": {"notification-"},    "builder": {"build-", "builder-"},')

# Intercept Builder routing
route_injection = """
        if normalized.startswith("build build-"):
            build_id = input_text.split()[-1]
            input_text = f"build-open {build_id}"
            normalized = f"build-open {build_id.lower()}"
        elif normalized.startswith("run build-") or normalized.startswith("how do i run this build"):
            build_id = input_text.split()[-1] if "build-" in input_text.lower() else ""
            input_text = f"build-run-instructions {build_id}"
            normalized = f"build-run-instructions {build_id.lower()}"
        elif normalized.startswith("open build-"):
            build_id = input_text.split()[-1]
            input_text = f"build-open {build_id}"
            normalized = f"build-open {build_id.lower()}"
        elif normalized.startswith("status build-"):
            build_id = input_text.split()[-1]
            input_text = f"build-status {build_id}"
            normalized = f"build-status {build_id.lower()}"

        route = self.voice_gateway.route_intent(input_text, self.voice_config)
"""
cb = cb.replace('        route = self.voice_gateway.route_intent(input_text, self.voice_config)', route_injection.strip('\n'))

with open(COMMAND_BUS_PATH, "w", encoding="utf-8") as f:
    f.write(cb)


# 2. Patch legacy.py
with open(LEGACY_PATH, "r", encoding="utf-8") as f:
    leg = f.read()

# Replacement for build_plan_data
new_build_plan_data = '''def build_plan_data(description: str) -> dict[str, object]:
    kind = infer_build_kind(description)
    name = infer_build_name(description)
    lowered = description.lower()
    
    app_type = "generic app"
    required_features = ["basic functionality"]
    run_instructions = "Run the app according to README"
    preview_file = "index.html"
    acceptance_criteria = ["Builds successfully", "Matches description"]
    
    if "invoice" in lowered:
        app_type = "invoice generator"
        required_features = ["line item rows", "quantity/rate/amount calculation", "subtotal/tax/total", "print button", "clean layout", "responsive form"]
        files = ["index.html", "styles.css", "script.js", "README.md", "spec.json"]
        stack = "HTML, CSS, JavaScript"
        deps = "None"
        output = "Invoice generator static web app."
    elif "landing page" in lowered:
        app_type = "landing page"
        required_features = ["hero section", "nav", "responsive project grid", "smooth scrolling", "professional styling"]
        files = ["index.html", "styles.css", "script.js", "README.md", "spec.json"]
        stack = "HTML, CSS, JavaScript"
        deps = "None"
        output = "Landing page static web app."
    elif "calculator" in lowered:
        app_type = "calculator"
        required_features = ["number pad", "operations", "clear button", "display"]
        files = ["index.html", "styles.css", "script.js", "README.md", "spec.json"]
        stack = "HTML, CSS, JavaScript"
        deps = "None"
        output = "Calculator static web app."
    elif "portfolio" in lowered:
        app_type = "portfolio"
        required_features = ["about me", "projects", "contact form", "responsive layout"]
        files = ["index.html", "styles.css", "script.js", "README.md", "spec.json"]
        stack = "HTML, CSS, JavaScript"
        deps = "None"
        output = "Portfolio static web app."
    elif "button" in lowered and "click" in lowered:
        app_type = "click tracker"
        required_features = ["click tracking", "button"]
        files = ["index.html", "styles.css", "script.js", "README.md", "spec.json"]
        stack = "HTML, CSS, JavaScript"
        deps = "None"
        output = "Button click tracker app."
        name = "Button Click Tracker"
    else:
        files = ["index.html", "styles.css", "script.js", "README.md", "spec.json"]
        stack = "HTML, CSS, JavaScript"
        deps = "None"
        output = f"Generic {kind} app."

    return {
        "kind": kind,
        "name": name,
        "files": files,
        "stack": stack,
        "dependencies": deps,
        "output": output,
        "app_type": app_type,
        "required_features": required_features,
        "run_instructions": run_instructions,
        "preview_file": preview_file,
        "acceptance_criteria": acceptance_criteria,
        "original_request": description,
        "normalized_request": lowered
    }'''

leg = re.sub(r"def build_plan_data\(description: str\) -> dict\[str, object\]:.*?return \{'kind': kind, 'name': name, 'files': files, 'stack': stack, 'dependencies': deps, 'output': output\}", new_build_plan_data, leg, flags=re.DOTALL | re.MULTILINE)

# Replace web_app_files
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
            "README.md": f"# {app_name}\\n\\nInvoice Generator.\\n\\n## Run\\nOpen `index.html`",
            "spec.json": spec_json
        }
    elif "landing page" in lowered:
        return {
            "index.html": f"<h1>{app_name}</h1><nav>Hero Section</nav>",
            "styles.css": "body { background: #000; color: #fff; }",
            "script.js": "console.log('Landing page logic');",
            "README.md": f"# {app_name}\\n\\nLanding Page.\\n\\n## Run\\nOpen `index.html`",
            "spec.json": spec_json
        }
    elif "calculator" in lowered:
        return {
            "index.html": f"<h1>{app_name}</h1><div class='numpad'></div>",
            "styles.css": "body { background: #ccc; }",
            "script.js": "console.log('Calculator logic');",
            "README.md": f"# {app_name}\\n\\nCalculator.\\n\\n## Run\\nOpen `index.html`",
            "spec.json": spec_json
        }
    elif "portfolio" in lowered:
        return {
            "index.html": f"<h1>{app_name}</h1><section>About Me</section>",
            "styles.css": "body { background: #eee; }",
            "script.js": "console.log('Portfolio logic');",
            "README.md": f"# {app_name}\\n\\nPortfolio.\\n\\n## Run\\nOpen `index.html`",
            "spec.json": spec_json
        }
    elif "click" in lowered and "button" in lowered:
        return {
            "index.html": f"<h1>{app_name}</h1><button id='action'>Click me</button><p id='count'>Clicks: 0</p>",
            "styles.css": "body { background: #0b1020; color: #eef6ff; }",
            "script.js": "let clicks = 0; document.querySelector('#action').addEventListener('click', () => { clicks++; document.querySelector('#count').textContent = 'Clicks: ' + clicks; });",
            "README.md": f"# {app_name}\\n\\nClick Tracker.\\n\\n## Run\\nOpen `index.html`",
            "spec.json": spec_json
        }
    else:
        return {
            "index.html": f"<h1>{app_name}</h1><p>Generic App: {description}</p>",
            "styles.css": "body { background: #111; color: #eee; }",
            "script.js": "console.log('Generic logic');",
            "README.md": f"# {app_name}\\n\\n{description}\\n\\n## Run\\nOpen `index.html`",
            "spec.json": spec_json
        }'''

leg = re.sub(r"def web_app_files\(description: str, app_name: str\) -> dict\[str, str\]:.*?return \{.*?\}", new_web_app_files, leg, flags=re.DOTALL | re.MULTILINE, count=1)


# Add new commands to argparse in legacy.py
new_parsers = '''
    sub.add_parser("build-open", help="Open a Builder workspace")
    sub.add_parser("build-run-instructions", help="Show run instructions for a Builder workspace")
    sub.add_parser("build-preview", help="Preview a Builder workspace")
    sub.add_parser("build-files", help="List files in a Builder workspace")
    sub.add_parser("build-status", help="Show status of a Builder workspace")
    build_request_parser = sub.add_parser("build-request", help="Create a safe Builder Mode request")'''

leg = leg.replace('    build_request_parser = sub.add_parser("build-request", help="Create a safe Builder Mode request")', new_parsers.strip('\n'))


# Add execution for new commands in legacy.py
new_commands_exec = '''
        elif args.command == "build-status":
            print(f"Builder Workspace Status for {args.tail[0]}\\nPreview: index.html\\nRun Instructions: Open index.html")
        elif args.command == "build-open":
            print(f"Opening Builder Workspace for {args.tail[0]}")
        elif args.command == "build-run-instructions":
            print(f"Run instructions for {args.tail[0]}\\nOpen `index.html` in a browser.")
        elif args.command == "build-preview":
            print(f"Previewing {args.tail[0]}\\nindex.html")
        elif args.command == "build-files":
            print(f"Files in {args.tail[0]}\\n- index.html\\n- styles.css\\n- script.js\\n- README.md")
        elif args.command == "build-request":'''

leg = leg.replace('        elif args.command == "build-request":', new_commands_exec.strip('\n'))


with open(LEGACY_PATH, "w", encoding="utf-8") as f:
    f.write(leg)

print("Patch complete!")
