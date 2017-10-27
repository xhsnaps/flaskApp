#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xhsnaps'

'''
flask App的启动文件
'''


from flask import Flask
import time


app = Flask(__name__)


@app.route('/')
def index():
    return "Index Page"


@app.route('/delay')
def delay_reply():
    time.sleep(1)
    return "response return delay 1 seconds"


if __name__ == '__main__':
    app.run()
