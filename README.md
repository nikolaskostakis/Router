# Router
- This tool is created as my thesis
- It is based on Lee's Maze Routing Algorithm
- Written in Python

# Required Packages
- tkinter
- pyreadline
- numpy
- mathplotlib

# Project structure
    Router/
    ├── benchmarks/
    ├── data/
    ├── router/
    │   ├── file_io/
    │   │   ├── __init__.py
    │   │   ├── parsers.py
    │   │   └── writers.py
    │   ├── place_and_route/
    │   │   ├── __init__.py
    │   │   ├── placement.py
    │   │   └── routing.py
    │   ├── structures/
    │   │   ├── __init__.py
    │   │   ├── design_components.py
    │   │   └── trees.py
    │   ├── ui/
    │   │   ├── __init__.py
    │   │   ├── gui.py
    │   │   └── tcl_interpreter.py
    │   ├── __init__.py
    │   ├── config.py
    │   └── router.py      
    ├── test/
    ├── .gitignore
    ├── Makefile
    └── README.md