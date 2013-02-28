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

import os
from PySide import QtCore, QtGui,QtWebKit
from pimoussWidget import PimoussWidget as PimoussWidget

class PimoussTabbedWidget(QtGui.QWidget):
  def __init__(self):
    super(PimoussTabbedWidget, self).__init__()
    self.initUI()
    self.pimoussStarted=False
    self.webView=QtWebKit.QWebView() 
    
  def initUI(self):
    self.tabs=QtGui.QTabWidget()  
    default=PimoussWidget()
    default.pimoussInput=os.getcwd()
    default.pimoussBuild=default.pimoussInput
    default.pimoussOutput=os.path.join(default.pimoussInput,'_html')    
    self.tabs.addTab(default,os.path.basename(default.pimoussInput))  

    layout = QtGui.QVBoxLayout()
    layout.addWidget(self.tabs)
    self.setLayout(layout)
    self.setWindowTitle("Pimouss")
    self.resize(300, 200)  


  def add(self,path):
    tab=PimoussWidget()
    tab.pimoussInput=path
    tab.pimoussBuild=path
    tab.pimoussOutput=os.path.join(path,'_html')
    tab.updateFolderGroupBox()
    self.tabs.addTab(tab,os.path.basename(path))  
  
  def dialog_add(self):
    options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
    directory = QtGui.QFileDialog.getExistingDirectory(self,"Select Content Directory",'/home', options)
    tab=PimoussWidget()
    tab.pimoussInput=directory
    tab.pimoussBuild=directory
    tab.pimoussOutput=os.path.join(directory,'_html')
    #tab.pimoussBuild=directory
    tab.updateFolderGroupBox()
    self.tabs.addTab(tab,os.path.basename(directory))  
  
  
  def open_(self):
    pass

  def remove(self):
    pass
    
  def save(self):
    print 'save'
    for idx in range(self.tabs.count()):
      print self.tabs.widget(idx)

  def build(self):
    for idx in range(self.tabs.count()):
      print self.tabs.widget(idx)
      self.tabs.widget(idx).process()  

       
