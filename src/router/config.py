"""
Config module used for global variables
"""

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