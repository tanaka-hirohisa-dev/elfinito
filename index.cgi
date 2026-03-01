#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from wsgiref.handlers import CGIHandler
from app import create_app

application = create_app()  # Flaskインスタンス生成
CGIHandler().run(application)

