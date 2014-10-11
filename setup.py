#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from setuptools import setup, find_packages

import mylittlebudget

with open('README.md') as f:
    long_description = f.read()
with open('requirements.txt') as f:
    install_requires = f.read()

setup(name='mylittlebudget',
      version='0.1',
      author='Florian Briand',
      license='GPLv3',
      long_description=long_description,
      #package_dir={'': 'src'},
      packages=find_packages(),
      entry_points = {
        'console_scripts': [
            'mylittlebudget = mylittlebudget.core:main'
        ]
      },
      install_requires=install_requires,
      #scripts=['scripts/mylittlebudget.py']
      )