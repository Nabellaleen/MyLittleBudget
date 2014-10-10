#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from bottle import run

import web.index

def main():
    run(host='localhost', port=8080)

if __name__ == '__main__':
    main()