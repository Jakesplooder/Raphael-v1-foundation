import glob
import os
import re

files = []
for f in glob.glob(r'C:\Users\cyber\Downloads\RalphaelOS\raphael_core\**\*.py', recursive=True):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    if r'C:\RaphaelOS' in content:
        files.append(f)

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # If it's a raw string r"C:\RaphaelOS..."
    # Replace r"C:\RaphaelOS\foo" with os.environ.get("RAPHAEL_DATA_DIR", r"C:\RaphaelOS") + r"\foo"
    # Actually simpler: os.path.join(os.environ.get("RAPHAEL_DATA_DIR", r"C:\RaphaelOS"), r"foo")
    
    # Let's just do text replace:
    new_content = content.replace(r'r"C:\RaphaelOS', 'os.path.join(os.environ.get("RAPHAEL_DATA_DIR", r"C:\\RaphaelOS"), r"')
    # This turns: r"C:\RaphaelOS\world_model\predictions"
    # Into: os.path.join(os.environ.get("RAPHAEL_DATA_DIR", r"C:\RaphaelOS"), r"\world_model\predictions"
    # Oh wait! We need to add the closing parenthesis.
    # It's safer to just replace 'r"C:\RaphaelOS' with '(os.environ.get("RAPHAEL_DATA_DIR", r"C:\\RaphaelOS") + r"'
    # So r"C:\RaphaelOS\foo" becomes (os.environ.get("RAPHAEL_DATA_DIR", r"C:\RaphaelOS") + r"\foo")
    
    new_content = new_content.replace(r'r"C:\RaphaelOS', '(os.environ.get("RAPHAEL_DATA_DIR", r"C:\\RaphaelOS") + r"')
    # We must add a closing paren after the string literal ends.
    # Actually, regex is better:
    # Match r"C:\RaphaelOS..." where ... doesn't have quotes.
    # Pattern: r"C:\\RaphaelOS([^"]*)"
    new_content = re.sub(r'r"C:\\RaphaelOS([^"]*)"', r'os.path.join(os.environ.get("RAPHAEL_DATA_DIR", r"C:\\RaphaelOS"), r"\1")', content)
    
    # Also handle the cases where they did:
    # os.path.join(r"C:\RaphaelOS\world_model", "training_records.json")
    # This regex will turn that into:
    # os.path.join(os.path.join(os.environ.get("RAPHAEL_DATA_DIR", r"C:\RaphaelOS"), r"\world_model"), "training_records.json")
    # which is completely fine!

    if "import os" not in new_content:
        new_content = "import os\n" + new_content

    with open(f, 'w', encoding='utf-8') as file:
        file.write(new_content)

print(f"Updated {len(files)} files.")
