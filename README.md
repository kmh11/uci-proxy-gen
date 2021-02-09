# UCI Proxy Generator

This is a script to generate wrappers that proxy Universal Chess Interface requests with additional `setoption` commands. [Gooey](https://github.com/chriskiehl/Gooey) is used to generate a GUI for all UCI options supported by an engine, but the generated wrappers have no dependencies outside of the standard library.

This is useful to generate configurations that are portable between engines, or to set options in GUIs that don't have an interface for UCI options.

## Getting Started

Install [Python 3](https://python.org) and [Gooey](https://github.com/chriskiehl/Gooey).

Run `proxygen.py` and select an engine executable. Set the options you want and save it to a `.py` file. In your Chess GUI, add a new UCI engine with either the `.py` file (Linux, MacOS) or the `.bat` file (Windows).

## Troubleshooting

Enable `LOGGING = True` in the generated proxy script and read `proxy.log` for all communication to/from the engine. The UCI protocol is documented [here](http://wbec-ridderkerk.nl/html/UCIProtocol.html). If you choose to [file an issue](https://github.com/kmh11/uci-proxy-gen/issues), please include that log file and the engine and GUI you are using.
