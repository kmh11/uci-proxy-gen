#!/usr/bin/env python3

from gooey import Gooey, GooeyParser
from pathlib import Path
import json
import stat
import sys
import os

@Gooey
def main():
	widgets = {"spin": "IntegerField", "combo": "Dropdown"}
	actions = {"check": "store_true", "string": "store"}
	parser = GooeyParser()
	parser.add_argument("Proxy file", help="Where to store the generated proxy", widget="FileSaver")
	options = json.loads(os.environ["OPTIONS"])
	for option in options:
		if option["type"] in actions:
			parser.add_argument("--"+option["name"], action=actions[option["type"]], gooey_options={"initial_value": option.get("default")})
		else:
			parser.add_argument("--"+option["name"], widget=widgets[option["type"]], help=("Min: {}, Max: {}".format(option.get("min"), option.get("max")) if "min" in option or "max" in option else None), gooey_options={"min": option.get("min"), "max": option.get("max"), "initial_value": option.get("default")}, **({"choices": option["choices"]} if "choices" in option else {}))
	options = vars(parser.parse_args())
	out = options["Proxy file"]
	del options["Proxy file"]
	with open(out, "w") as f:
		f.write(open(str(Path(__file__).parent / "uciproxy.py")).read() % (repr(os.environ["ENGINE"]), repr(options)))
	os.chmod(out, os.stat(out).st_mode | stat.S_IEXEC)
	with open(out.rpartition(".")[0]+".bat", "w") as f:
		f.write(sys.executable+" "+out)

main()
