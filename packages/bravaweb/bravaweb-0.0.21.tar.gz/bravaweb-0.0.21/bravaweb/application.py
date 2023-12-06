# -*- coding: utf-8 -*-

import os

# Third Part Imports

# Basics Imports
import configuration

# Utils
from bravaweb.utils import GetHeader

# Security
import bravaweb.security as Security

# Enviroment
from bravaweb.enviroment import Enviroment

# Error Tratament
import traceback

# App Boot Time
from datetime import datetime

# App Log
from bravaweb.utils.log import *

boot_time = datetime.now()


async def App(scope, receive, send, hanndler_error=None):
    try:
        Debug(f"Request '{scope['method']} {scope['path']}'")
        headers = GetHeader(scope)
        Debug("Catching Header")
    except Exception as e:
        if not hanndler_error is None:
            hanndler_error(e, scope, None, 'Global Error: Get Header')
        raise e

    try:

        if scope["method"] == "OPTIONS":
            await Security.origin.Options(headers, send)

        elif Security.origin.Static(scope):
            await Security.origin.NotFound(send)

        elif Security.origin.Permitted(headers, scope):

            try:
                Debug("Load Enviroment")
                envirom = Enviroment(headers, scope, receive, send)

                Debug("Receiving Body")
                await envirom.ReceiveBody()

                Debug("Start Response")
                await envirom.Response()

            except Exception as e:
                if not hanndler_error is None:
                    hanndler_error(e, scope, headers, 'Global Error: Enviroment, Body Response')
                Error("App Response Content", e)
        else:
            Error("", "Request Origin Not Authorized", False)
            await Security.origin.Forbidden(send)

    except Exception as e:
        if not hanndler_error is None:
            hanndler_error(e, scope, headers, 'Global Error: Unexpected')
        raise e
