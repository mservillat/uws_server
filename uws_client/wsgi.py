#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright (c) 2016 by Mathieu Servillat
# Licensed under MIT (https://github.com/mservillat/uws-server/blob/master/LICENSE)
"""
WSGI script for UWS server
"""

import os
import sys

curdir = os.path.dirname(__file__)
sys.path.append(curdir)

# Change working directory so relative paths (and template lookup) work again
os.chdir(curdir)

import bottle
from uws_client import uws_client

# Do NOT use bottle.run() with mod_wsgi
application = uws_client.app
