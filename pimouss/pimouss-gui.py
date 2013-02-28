#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Simple Graphical User Interface using pyside (Qt python binding) """
__version__='alpha'
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

try:
  from PySide import QtCore, QtGui,QtWebKit
except:
  raise NameError('Pyside is no installed on your system. Check http://qt-project.org/wiki/PySide for more')

import pimouss
from desktop.pimoussWidget import PimoussWidget as PimoussWidget 
from desktop.PimoussTabbedWidget import PimoussTabbedWidget as PimoussTabbedWidget

          
class MainWindow(QtGui.QMainWindow):
  def __init__(self):
    super(MainWindow, self).__init__()
    self.initUI()

  def initUI(self):   
    self.mainWidget=PimoussTabbedWidget()
    self.statusBar().showMessage("using pimouss v. %s" %(pimouss.__version__))
    self.setCentralWidget(self.mainWidget)
    self.setGeometry(300, 300, 350, 250)
    self.setWindowTitle('Pimouss')    
    self.show()
    
    fileMenu = self.menuBar().addMenu("&Pimouss")
    self.addAct=QtGui.QAction("&Add pimouss", self,shortcut=QtGui.QKeySequence.New,statusTip="Add a new folder to process", 
                triggered=self.add)
    self.saveAct=QtGui.QAction("&Save This Project", self,shortcut=QtGui.QKeySequence.New,statusTip="Save config in file", 
                triggered=self.save)
    self.buildAct=QtGui.QAction("&Build all", self,shortcut=QtGui.QKeySequence.New,statusTip="build project", 
                triggered=self.build)    
    fileMenu.addAction(self.addAct)
    fileMenu.addAction(self.saveAct)
    fileMenu.addAction(self.buildAct)
        
  def add(self):
    self.mainWidget.dialog_add()

  def open_(self):
    self.mainWidget.open_()

  def save(self):
    self.mainWidget.save()

  def build(self):
    self.mainWidget.build()     

      
def main():
  app = QtGui.QApplication(sys.argv)
  pixmap = QtGui.QPixmap("splash.png")
  splash = QtGui.QSplashScreen(pixmap)
  splash.show()
  splash.showMessage("Load pimouss...")
  app.processEvents()
  m=MainWindow()
  m.show()
  splash.finish(m)
  sys.exit(app.exec_())
    
if __name__ == '__main__':
  main()

