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
from pimoussTabbedWidget import PimoussTabbedWidget as PimoussTabbedWidget

class PimoussProjectWidget(QtGui.QWidget): #this is an Iglou!
  def __init__(self):
    super(PimoussProjectWidget, self).__init__()
    self.initUI()
    self.project=[]
    
  def initUI(self):
    self.createProjectNav()
    self.createTabbedWidget()
    self.createFileListWidget()
    #self.create
    mainLayout = QtGui.QHBoxLayout()
    self.setLayout(mainLayout)
    self.setWindowTitle("Iglou - a home for pimousses")
    self.resize(300, 200)
    splitter = QtGui.QSplitter()

    splitter.addWidget(self.projectNavGroupBox)
    splitter.addWidget(self.filesGroupBox)    
    splitter.addWidget(self.pimoussTabGroupBox)
    mainLayout.addWidget(splitter)

  def createFileListWidget(self):
    self.filesGroupBox=QtGui.QGroupBox("Files")
    self.listview=QtGui.QListView()
    groupBoxLayout=QtGui.QGridLayout()
    groupBoxLayout.addWidget(self.listview)
    self.filesGroupBox.setLayout(groupBoxLayout)

  def createProjectNav(self):
    self.projectNavGroupBox=QtGui.QGroupBox("Projects")
    self.treeWidget = QtGui.QTreeWidget()
    self.treeWidget.setColumnCount(1)
    #self.treeWidget.insertTopLevelItems(0, self.project)
    groupBoxLayout=QtGui.QGridLayout()
    groupBoxLayout.addWidget(self.treeWidget)
    self.projectNavGroupBox.setLayout(groupBoxLayout)
 
    self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu) 
    self.connect(self.treeWidget, QtCore.SIGNAL("customContextMenuRequested(const QPoint &)"), self.menuContextTree)

  def menuContextTree(self, point):
    item = self.treeWidget.itemAt(point) 
    print item
    
  def createTabbedWidget(self):
    self.pimoussTabGroupBox=QtGui.QGroupBox("Pimousses")
    self.tabwidget=PimoussTabbedWidget()
    groupBoxLayout=QtGui.QGridLayout()
    groupBoxLayout.addWidget(self.tabwidget)
    self.pimoussTabGroupBox.setLayout(groupBoxLayout)

  def addProject(self,name,path):
    #self.tabwidget.add()
    item=QtGui.QTreeWidgetItem()
    item.setText(0,name)
    self.treeWidget.addTopLevelItem(item)
    self.tabwidget.add(path)
    #self.tabwidget
    #tab=PimoussTabbedWidget()
    #tab.pimoussInput=path
    #tab.updateFolderGroupBox()
    #self.tabwidget.addTab(tab,os.path.dirname(path))



