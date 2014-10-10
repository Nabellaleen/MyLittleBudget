# -*- coding: UTF-8 -*-
from distutils.core import setup
from setuptools import find_packages

with open('README.md') as f:
    long_description = f.read()
with open('requirements.txt') as f:
    install_requires = f.read()

setup(name='MyLittleBudget',
      version='0.1',
      author='Florian Briand',
      license='GPLv3',
      long_description=long_description,
      #package_dir={'': 'src'},
      packages=find_packages(),
      install_requires=install_requires,
      scripts=['src/mylittlebudget.py'])