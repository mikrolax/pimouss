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
      description='simple static website builder',
      author=pimouss.__author__,
      author_email=pimouss.__author_email__,
      license=pimouss.__license__,
      url='http://mikrolax.github.com/pimouss',

      packages=['pimouss','pimouss.external','pimouss.desktop'],
      py_modules=['pimouss'], 
      scripts=['igloo.py'], # to change
      
      package_data={'pimouss.desktop': ['static/*.png'],
                  },

      #for py2exe 
      options ={'py2exe': {'excludes':['mail','unittest','jinja2','pygments'],'bundle_files': 1,'dist_dir':'win32-static/'}}, 
      zipfile = None,
      #console=[{'script':'pimouss/pimouss.py',}],
      windows=[{'script':'pimouss/pimouss-gui.py'}]
     )

