#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Simple Graphical User Interface using pyside (Qt python binding) """

__author__='Sebastien Stang'
__author_email__='seb@mikrolax.me'
__license__="""Copyright (C) 2013 Sebastien Stang

Permission is hereby granted, free of charge, to any person obtaining a copy of 
this software and associated documentation files (the "Software"), to deal in 
the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
of the Software, and to permit persons to whom the Software is furnished to do so,
 subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE 
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


import sys
import os
import logging
logfile='pimouss.log'

try:
  from PySide import QtCore, QtGui,QtWebKit
except:
  raise NameError('Pyside is no installed on your system. Check http://qt-project.org/wiki/PySide for more')

from pimoussWidget import PimoussWidget
from desktop.AppMainWindow import MainWindow as AppMainWindow 

def _we_are_frozen():
  return hasattr(sys, "frozen")

def _module_path():
  if _we_are_frozen():
    return os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding( )))
  else:
    return os.path.dirname(os.path.abspath(__file__))
    
title='Pimouss'
class MainWindow(AppMainWindow):
  def __init__(self,parent=None):
    logging.debug('gui.MainWindow:: init %s' %parent)
    self.appWidget=PimoussWidget() # contains self.appWidget.thread
    super(MainWindow, self).__init__(self.appWidget,self)
    self.parent=parent
    self.init()
  
  def init(self):  
    logging.debug('gui.MainWindow::init')  
    self.project_ext=['*.md']
    self.title=title
    self.init_ui()
    self.setLog(logfile)
    self.setWindowTitle(title)   
    self.appWidget.setHTMLView(os.path.join(_module_path(),'static','welcome.html'))   
    
    self.connect(self.appWidget.thread, QtCore.SIGNAL("pimoussProcessStart(PyObject)"), self.onStartProcess)
    self.connect(self.appWidget.thread, QtCore.SIGNAL("pimoussProcessEnd(PyObject)"), self.onEndProcess)
 
  def setProject(self, _name, path):
    logging.debug('gui.MainWindow::setProject %s : %s' %(_name,path))
    #specific widget things here
    self._name=_name
    self.path=path
    out_path=self.appWidget.update(_name,path) #return output folder
    self.setFileView(os.path.join(out_path))
    
  def onStartProcess(self,msg):
    logging.debug('gui.MainWindow::onStartProcess: %s' %msg)
    self.startProcessTimer()
    self.statusBar().showMessage(msg)
    
  def onEndProcess(self,msg):
    logging.debug('gui.MainWindow::onEndProcess: %s' %msg)
    self.stopProcessTimer()
    self.statusBar().showMessage('Ready')
    self.setProject(self._name,self.path)


def main(): 
  formatter='%(asctime)s::%(levelname)s::%(message)s'
  print logfile
  logging.basicConfig(filename=os.path.abspath(logfile), filemode='w',format=formatter, level=logging.INFO)
  app = QtGui.QApplication(sys.argv)
  pixmap = QtGui.QPixmap("logo.png")
  splash = QtGui.QSplashScreen(pixmap)
  splash.show()
  splash.showMessage("Load pimouss...")
  app.processEvents()
  win=MainWindow()
  win.show()
  splash.finish(win)  
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()

