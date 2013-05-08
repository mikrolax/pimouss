#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Simple HTML viewer widget using pyside webkit & treeView """

__author__ = 'Sebastien Stang'
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

import logging
try:
  from PySide import QtCore,QtGui,QtWebKit
except:
  raise NameError('Pyside is no installed on your system. Check http://qt-project.org/wiki/PySide for more')

group_box_name=''
window_title  ='HTML viewer'
parent_icon   ='icon.png'

#=AppMainWindow.icon

#options
ext           =['*.html']

class FilesWidget(QtGui.QWidget):
  """ Simple HTML viewer widget using QTreeView & QWebKit"""
  def __init__(self):
    super(FilesWidget, self).__init__()  
    self.mWebView = QtWebKit.QWebView()
    try:
      self.mWebView.setWindowIcon((QtGui.QIcon(parent_icon)))
    except:
      pass
    self.mWebView.setWindowTitle('%s :: Webkit Preview' %window_title)    
    self.init_ui()
    self.folderpath=None
    self.ext=ext     
    
  def init_ui(self):     
    logging.debug( 'FilesWidget::init_ui')
    self.filesGroupBox=QtGui.QGroupBox(group_box_name)
    self.model = QtGui.QFileSystemModel()
    self.model.setRootPath(QtCore.QDir.currentPath())
    self.tree =  QtGui.QTreeView()
    self.tree.setSortingEnabled(True)
    self.tree.setModel(self.model)
    #self.tree.clicked[QtCore.QModelIndex].connect(self.preview)
    groupBoxLayout=QtGui.QGridLayout()
    groupBoxLayout.addWidget(self.tree)
    self.filesGroupBox.setLayout(groupBoxLayout)
    self.layout = QtGui.QHBoxLayout()
    self.layout.addWidget(self.filesGroupBox)    
    self.setLayout(self.layout)
    self.setWindowTitle(window_title)    
    self.tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    self.connect(self.tree, QtCore.SIGNAL("customContextMenuRequested(const QPoint &)"), self.showContextMenu)
    self.previewAct=QtGui.QAction('&Preview', self) #delete selected if any
    self.previewAct.triggered.connect(self.preview)
  
  def set_path(self,path):
    logging.debug('FilesWidget::set_path %s' %path)  
    self.folderpath=path
    self.model.setRootPath(self.folderpath)
    self.model.setNameFilters(self.ext)
    self.tree.setModel(self.model)
    self.tree.setRootIndex(self.model.index(self.folderpath))    #QtCore.QDir(

  def showContextMenu(self,point):    
    logging.debug('FilesWidget::showContextMenu')
    menu = QtGui.QMenu()
    viewAction=menu.addAction(self.previewAct)    
    menu.exec_(QtGui.QCursor.pos())
    
  def preview(self,url=None):
    index = self.tree.currentIndex()
    url = self.model.filePath(index)
    #logging.info('preview %s' %url)
    self.mWebView.load(url)
    self.mWebView.show()    
    
    
