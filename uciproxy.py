#!/usr/bin/env python3

import asyncio
import sys

if sys.platform == "win32":
	loop = asyncio.ProactorEventLoop()
	asyncio.set_event_loop(loop)
else:
	loop = asyncio.get_event_loop()

async def proxy_out():
	async for line in process.stdout:
		sys.stdout.buffer.write(line)
		sys.stdout.flush()
		if process.returncode is not None: break

async def proxy_in(options):
	while process.returncode is None:
		line = await loop.run_in_executor(None, sys.stdin.buffer.readline)
		if line.strip() == b"isready":
			for name in options:
				if options[name] is None: continue
				process.stdin.write(f"setoption name {{}} value {options[name]}\n".format(name.replace("__", " ")).encode("utf-8"))
		process.stdin.write(line)

process = loop.run_until_complete(asyncio.create_subprocess_exec(%s, stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE))
loop.run_until_complete(asyncio.gather(proxy_in(%s), proxy_out()))
