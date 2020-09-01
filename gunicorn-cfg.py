# -*- encoding: utf-8 -*-
"""
License: Commercial
Copyright (c) 2019 - present AppSeed.us
"""

bind = "0.0.0.0:5005"
# bind = "unix://run/gunicorn.socket"
workers = 4
pythonpath = "."
accesslog = "./logs/gunicorn_access.log"
errorlog = "./logs/gunicorn_error.log"
workers = 1
loglevel = "debug"
capture_output = True
enable_stdio_inheritance = True
