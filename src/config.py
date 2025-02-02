# -*- coding: utf-8 -*-

"""
Config module used for global variables
"""

__author__ = "Nikolaos Kostakis"
__copyright__ = "Copyright (c) 2024 Nikolaos Kostakis"
__license__ = "MIT License"
__version__ = "1.0"

import logging
import sys

loggingLevel = logging.INFO
"""
Logging level to be used by loggers in each module

Default value is logging.INFO & can be changed to logging.DEBUG, given command
line arguments '-d' or '--debug' 
"""

simpleFormatter = logging.Formatter("%(levelname)s: %(message)s")
"""Simple formatter used for logging messagees"""
detailedFormatter = logging.Formatter(
    "%(asctime)s from %(name)s: %(levelname)s: %(message)s"
)
"""A detailed formatter used for logging messagees"""

consoleHandler = logging.StreamHandler(sys.stdout)
"""Console handler for logging messages shown in the stdout"""
consoleHandler.setLevel(loggingLevel)
consoleHandler.setFormatter(simpleFormatter)

logfileHandler = logging.FileHandler(filename="data\\router.log")
"""File handler for logging messages in a log file"""
logfileHandler.setLevel(loggingLevel)
logfileHandler.setFormatter(detailedFormatter)