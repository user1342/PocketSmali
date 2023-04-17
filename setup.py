#!/usr/bin/env python

from distutils.core import setup

setup(name='PocketSmali',
      version='0.3',
      description='A modular and extendable Python tool for emulating simple SMALI methods.',
      author='James Stevenson',
      author_email="hi@jamesstevenson.me",
      url='https://github.com/user1342/PocketSmali',
      packages=['PocketSmali','PocketSmali.opcode_handlers'],
     )
