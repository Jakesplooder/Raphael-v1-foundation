import sys
sys.path.insert(0, r"R:\RaphaelOS")
from command_bus import RaphaelCommandBus

bus = RaphaelCommandBus()

result1 = bus.route("how do i run this build BUILD-123")
print("1. Intent:", result1.get("intent"), "Command:", result1.get("command_type"), result1.get("matched_command"))

result2 = bus.route("status build-999")
print("2. Intent:", result2.get("intent"), "Command:", result2.get("command_type"), result2.get("matched_command"))

result3 = bus.route("open build-xyz")
print("3. Intent:", result3.get("intent"), "Command:", result3.get("command_type"), result3.get("matched_command"))
