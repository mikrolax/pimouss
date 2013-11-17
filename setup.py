#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import pimouss.pimouss as pimouss

try:
  import py2exe
except:
  print 'Can not import py2exe'

data_desk=glob.glob(os.path.join('pimouss','desktop','static','*.png'))
data_img=glob.glob(os.path.join('pimouss','static','img','*.png'))
data_css=glob.glob(os.path.join('pimouss','static','css','*.css'))
data_js=glob.glob(os.path.join('pimouss','static','js','*.js'))
data_desk.extend(glob.glob(os.path.join('pimouss','static','*.html')))

setup(name='pimouss',
      version=pimouss.__version__,
      description='simple static website builder',
      author=pimouss.__author__,
      author_email=pimouss.__author_email__,
      license=pimouss.__license__,
      url='http://mikrolax.github.com/pimouss',

      package_dir={'pimouss': 'pimouss'},
      packages=['pimouss','pimouss.external','pimouss.desktop'],
      #py_modules=['pimouss'], 
      #scripts=['pimouss/pimouss.py'], # change name and add pimouss.py too

      entry_points={
          'console_scripts': [
              'pimouss-gui = pimouss.gui:main',
              'pimouss = pimouss.pimouss:cli',
          ]
      },      
      package_data={'pimouss.desktop': ['static/*.png'],
                    'pimouss': ['static/img/*.png','static/js/*.js','static/css/*.css','static/*.html'],                  
                  },

      #for py2exe 
      data_files=[('static',data_desk),('static/img',data_img),('static/css',data_css),('static/js',data_js)],
      options ={'py2exe': {'includes':'PySide.QtNetwork','excludes':['mail','unittest','jinja2','pygments'],'bundle_files': 1,'dist_dir':'dist/win32-static/'}}, 
      zipfile = None,
      #console=[{'script':'pimouss/pimouss.py',}],
      windows=[{'script':'igloo.py','dest_base': 'pimouss',}] #"icon_resources":[(0,"icon.ico")],
     )

