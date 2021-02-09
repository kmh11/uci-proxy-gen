#!/usr/bin/env python3

from gooey import Gooey, GooeyParser
from pathlib import Path
import subprocess
import json
import sys
import os

@Gooey
def main():
	parser = GooeyParser()
	parser.add_argument("Engine", help="Location of the chess engine to proxy", widget="FileChooser")
	args = parser.parse_args()
	p = subprocess.Popen([args.Engine], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	p.stdin.write(b"uci\n")
	p.stdin.flush()
	output = ""
	for line in p.stdout:
		output += line.decode("utf-8")
		if b"uciok" == line.strip(): break
	p.kill()
	options = []
	for line in output.split("\r\n" if "\r" in output else "\n"):
		tokens = line.split(" ")
		if tokens[0] == "option":
			option = {}
			option["name"] = tokens[2].replace(" ", "__")
			tokens = tokens[2:]
			while (tokens := tokens[1:])[0] != "type":
				option["name"] += "__" + tokens[0]
			option["type"] = tokens[1]
			tokens = tokens[2:]
			if option["type"] == "button": continue
			elif option["type"] == "string":
				if len(tokens) > 1:
					assert tokens[0] == "default"
					option["default"] = " ".join(tokens[1:])
			elif option["type"] == "spin":
				while tokens:
					option[tokens[0]] = int(tokens[1])
					tokens = tokens[2:]
			elif option["type"] == "combo":
				option["choices"] = []
				while len(tokens) > 1:
					default = tokens[0] == "default"
					assert default or tokens[0] == "var"
					choice = tokens[1]
					tokens = tokens[1:]
					while len(tokens) > 1 and (tokens := tokens[1:])[0] not in ("var", "default"):
						choice += " " + tokens[0]
					if choice not in option["choices"]: option["choices"].append(choice)
					if default: option["default"] = choice
			elif option["type"] == "check":
				if len(tokens) > 1:
					assert tokens[0] == "default"
					assert tokens[1] in ("true", "false")
					option["default"] = tokens[1] == "true"
			options.append(option)
	subprocess.run([sys.executable, str(Path(__file__).parent / "configure.py")], env=dict(os.environ, ENGINE=args.Engine, OPTIONS=json.dumps(options)))

main()
