# SCF-MSP430
This repository contains a tool called Side-Channel Finder for MSP, a static analysis tool to automatically verify  binary files compiled for MSP430 microcontroller to detecting information leakage through novel interrupt-latency attacks (a.k.a. Nemesis), timing side-channels, and undesired information flow.

## Pre-requisites
1- To run SCF-MSP, **Python 3** is required.<br/>
2- For parsing and analyzing ELF files, a Python library, **pyelftools**, is required to install. See https://github.com/eliben/pyelftools for more details.\
3- The graph library **NetworkX 1.11**.
