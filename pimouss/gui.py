#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Simple Graphical User Interface using pyside (Qt python binding) """

__author__='sebastien stang'
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

title='pimouss'
class MainWindow(AppMainWindow):
  def __init__(self,parent=None):
    logging.debug('gui.MainWindow:: init %s' %parent)
    self.appWidget=PimoussWidget()
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
    #self.connect(self.appWidget.thread, QtCore.SIGNAL('onStartProcess(PyObject)'), self.onStartProcess)    
    #self.connect(self.appWidget.thread, QtCore.SIGNAL('onStopProcess(PyObject)'), self.onEndProcess)    
 

  def setProject(self, _name, path):
    logging.info('gui.MainWindow::setProject %s : %s' %(_name,path))
    self.setFileView(os.path.join(path))
    #setLog() # if on a per project config
    #specific widget things here
    self.appWidget.pimoussInput=path
    self.appWidget.pimoussOutput=os.path.join(path,'_html')
    self.appWidget.updateFolderGroupBox()
    if os.path.exist(os.path.join(path,'_html','index.html')):
      self.appWidget.setHTMLView(os.path.join(path,'_html','index.html'))            

  def onStartProcess(self,msg):
    logging.debug('gui.MainWindow::onStartProcess: %s' %msg)
    self.startProcessTimer()
    self.statusBar().showMessage(msg)
    
  def onEndProcess(self,msg):
    logging.debug('gui.MainWindow::onEndProcess: %s' %msg)
    self.stopProcessTimer()
    self.statusBar().showMessage(msg)


def main(): 
  formatter='%(asctime)s::%(levelname)s::%(message)s'
  print logfile
  logging.basicConfig(filename=os.path.abspath(logfile), filemode='w',format=formatter, level=logging.DEBUG)
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

