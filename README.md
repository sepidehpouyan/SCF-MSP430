# SCF-MSP430
This repository contains a tool called Side-Channel Finder for MSP, a static analysis tool to automatically verify  binary files compiled for MSP430 microcontroller to detecting information leakage through novel interrupt-latency attacks (a.k.a. Nemesis), timing side-channels, and undesired information flow.

## Pre-requisites
- To run SCF-MSP, **Python 3** is required.<br/>
- For parsing and analyzing ELF files, a Python library, **pyelftools**, is required to install. See https://github.com/eliben/pyelftools for more details.
- The graph library **NetworkX 1.11**.

## Creating input files
SCF-MSP takes an input file in the JSON format. It contains the path to the binary file, the starting function, a list of starting function’s arguments from high-level code and return values.

We assume a function

    int func(int secret, int public)

in a binary file "A". The corresponding json file could be like:
<pre>
	{ <br />
           "file": "A",<br/>
	   "starting_function": "func",<br/>
	   "timing_sensitive": true,<br/>
	   "parameters": [{<br  />
		"size": 1,<br/>
		"confidential": true 
	    }, {
		"size": 1,
		"confidential": false
		}
	    ],
	   "memory": false,
	   "result": {
	        "size": 1,
		"confidential": true,
		"memory": false
		}
	  }
  </pre>

The security level of parameters can be set by **confidential** directive. Setting the confidential directive to true makes the parameter confidential.

## Preparing binary files
The C programs are being compiled once with the off-the-shelf LLVM backend for the MSP430, resulting in a vulnerable binary programme. You can find them as `*.vulnerable` in testcase folder. In addition, a second version of the assembly code is produced ( `*.nemdef` in testcase folder), where instructions in secret-dependent branches are balanced out with respect to the individual instructions’ execution times.

## Running the benchmark
The binary files and the corresponding json files of some vulnerable and beningn C programs is provided in the `testcase` folder. You can run them by executing:

> python main.py testcase/example.json
