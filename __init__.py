#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask

app = Flask(__name__)
from FileUploadApp import views

app.config.update(
    DEBUG=True,
    SECRET_KEY='d66HR8dç"f_-àgjYYic*dh',
)

from FileUploadApp import app



