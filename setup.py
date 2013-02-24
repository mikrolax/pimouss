#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
import pimouss.pimouss as pimouss

try:
  import py2exe
except:
  print 'Can not import py2exe'


setup(name='pimouss',
      version=pimouss.__version__,
      description='',
      author='sebastien stang',
      author_email='seb@mikrolax.me',
      url='',
      package_dir = {'': 'pimouss'},
      packages=['external'],
      py_modules=['pimouss'], 
      scripts=['pimouss/pimouss.py','pimouss/pimouss-gui.py'],

      #for py2exe 
      options ={'py2exe': {'excludes':['mail','unittest','jinja2','pygments'],'bundle_files': 1,'dist_dir':'win32-static/'}}, 
      zipfile = None,
      console=[{'script':'pimouss/pimouss.py',}],
      windows=[{'script':'pimouss/pimouss-gui.py'}]
     )

