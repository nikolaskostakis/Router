# Router
This project is a routing tool, based on Lee's Maze Algorithm & is part of my thesis.

> The project is still under development!

## Requirements
Python 3.10 and beyond
### Required packages
- tkinter
- pyreadline
- numpy
- mathplotlib

## Project structure
    Router/
    ├── benchmarks/
    ├── data/
    ├── src/
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