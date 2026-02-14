#!/usr/local/bin/python3

from wsgiref.handlers import CGIHandler
# index.cgiファイルと同階層にあるapp.pyファイルを呼び出し
from app import app
# Flaskアプリ実行
CGIHandler().run(app)

