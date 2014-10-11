#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from bottle import route, template, view

@route('/hello/<name>')
def hello(name):
    return template('<b>Hello {{name}}</b> !', name=name)

@route('/')
@view('mylittlebudget/web/templates/index.tpl')
def index():
	context = {'title': 'My Little Budget'}
	return context
