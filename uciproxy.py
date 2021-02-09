#!/usr/bin/env python3

import asyncio
import sys

LOGGING = False

if sys.platform == "win32":
	loop = asyncio.ProactorEventLoop()
	asyncio.set_event_loop(loop)
else:
	loop = asyncio.get_event_loop()

def log(m, out):
	if not LOGGING: return
	from pathlib import Path
	with open(Path(__file__).parent / "proxy.log", "ab") as f:
		if out: f.write(b"< ")
		else: f.write(b"> ")
		f.write(m)

configured = False

async def proxy_out():
	async for line in process.stdout:
		log(line, True)
		sys.stdout.buffer.write(line)
		sys.stdout.flush()
		if process.returncode is not None: break

async def proxy_in(options):
	global configured
	while process.returncode is None:
		line = await loop.run_in_executor(None, sys.stdin.buffer.readline)
		if not configured and line.strip().split(b" ")[0] in (b"isready", b"position", b"go"):
			configured = True
			for name in options:
				if options[name] is None: continue
				if options[name] is True: options[name] = "true"
				elif options[name] is False: options[name] = "false"
				command = f"setoption name {{}} value {options[name]}\n".format(name.replace("__", " ")).encode("utf-8")
				log(command, False)
				process.stdin.write(command)
		log(line, False)
		process.stdin.write(line)

process = loop.run_until_complete(asyncio.create_subprocess_exec(%s, stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE))
loop.run_until_complete(asyncio.gather(proxy_in(%s), proxy_out()))
