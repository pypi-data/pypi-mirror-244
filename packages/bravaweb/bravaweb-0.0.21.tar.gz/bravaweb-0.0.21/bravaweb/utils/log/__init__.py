#!/usr/bin/env python

# LIBS
from datetime import datetime
import traceback as trace

# LOGGING
import logging

# CREATE TOP LOG LEVEL
log = logging.getLogger("uvicorn.error")

def Info(message):
    log.info(message)

def Debug(message):
    log.debug(message)

def Warning(message):
    log.warning(message)

def Error(sector, e, traceback=True):
    _trace = None
    message = ""
    if traceback:
        _trace = trace.format_exc()
        message = f"\n {sector if sector else ''}: {_trace if _trace else ''} \n"
    log.error(f"\n{message} Message: {e if e else ''}\n")

def Critical(sector, e, traceback=True):
    _trace = None
    message = ""
    if traceback:
        _trace = trace.format_exc()
        message = f"\n {sector if sector else ''}: {_trace if _trace else ''} \n"
    log.critical(f"\n{message} Message: {e if e else ''}\n")
