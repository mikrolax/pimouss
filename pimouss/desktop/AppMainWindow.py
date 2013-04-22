#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

import sys
import os
import logging

try:
  from PySide import QtCore,QtGui
except:
  raise NameError('Pyside is no installed on your system. Check http://qt-project.org/wiki/PySide for more')

from log_widget import LogWidget
from tree_widget import TreeWidget
from files_widget import FilesWidget

from config import Config

#configfilename='appMainWindow.cfg'
title='App'
#icon=QtGui.QIcon(os.path.join(_module_path(),'icon.png'))
project_dock_name='Project'     
log_dock_name='Log'     
files_dock_name='Report'     


def _we_are_frozen():
    """Returns whether we are frozen via py2exe.
    This will affect how we find out where we are located."""
    return hasattr(sys, "frozen")
def _module_path():
    """ This will get us the program's directory,
    even if we are frozen using py2exe"""
    if _we_are_frozen():
        return os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding( )))
    return os.path.dirname(unicode(__file__, sys.getfilesystemencoding( )))  


class MainWindow(QtGui.QMainWindow):
  def __init__(self,app_widget,parent=None):
    super(MainWindow, self).__init__()   
    self.wapp=app_widget
    #self.wproject.parent_type='file'      #configure the treeViewItem scan
    self.project_ext=['*.*']             #configure the treeView scan extension
    #self.init_ui()
    self.config=Config()
    self.parent=parent

  def init_ui(self): 
    logging.debug('MainWindow::init_ui')
    self.setCentralWidget(self.wapp)
    #self.setWindowTitle(title)

    dockWidget = QtGui.QDockWidget(project_dock_name, self)
    #dockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
    self.wproject=TreeWidget()
    self.wproject.parent_type='file'      #configure the treeViewItem scan
    self.wproject.ext=self.project_ext   #configure the treeView scan extension
    
    dockWidget.setWidget(self.wproject)
    self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dockWidget)

    dockWidget = QtGui.QDockWidget(log_dock_name, self)
    #dockWidget.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
    self.wlog=LogWidget()
    dockWidget.setWidget(self.wlog)
    self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, dockWidget)

    dockWidget = QtGui.QDockWidget(files_dock_name, self)
    #dockWidget.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
    self.wfiles=FilesWidget()
    dockWidget.setWidget(self.wfiles)
    #self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dockWidget)
    self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, dockWidget)
    
    logging.debug('MainWindow::create actions')
    self.create_actions()
    logging.debug('MainWindow::create menu')
    self.create_menu()
    self.statusBar().showMessage('Ready')
    
    try:
      version='%s v.%s' %(self.wapp.__project__,self.wapp.__version__)
      self.statusBar().addPermanentWidget(QtGui.QLabel(version))
    except:
      pass

    try:
      self.setWindowIcon((QtGui.QIcon(os.path.join(_module_path(),'static','icon.png'))))
      self.led_red_pixmap = QtGui.QPixmap(os.path.join(_module_path(),'static','led-red.png'))
      self.led_green_pixmap = QtGui.QPixmap(os.path.join(_module_path(),'static','led-green.png'))
      self.led_grey_pixmap = QtGui.QPixmap(os.path.join(_module_path(),'static','led-grey.png'))
      self.led_blue_pixmap = QtGui.QPixmap(os.path.join(_module_path(),'static','led-blue.png'))
      
      self.processWidget=QtGui.QLabel()    
      self.processWidget.setPixmap(self.led_grey_pixmap)
      self.statusBar().addPermanentWidget(self.processWidget)
      #use_LCD
      self.statusbar_timer=QtGui.QLCDNumber()
      self.statusBar().addPermanentWidget(self.statusbar_timer)
      #use_ToolLED
      #self.toolLED=QtGui.QLabel()    
      #self.toolLED.setPixmap(self.led_grey_pixmap)
      #self.statusBar().addPermanentWidget(self.toolLED)      
    except:
      pass #should do something
    #self.show()
    
  def create_actions(self):
    self.addProjectAct=QtGui.QAction(QtGui.QIcon('add.png'), '&Add', self)
    self.addProjectAct.triggered.connect(self.addProject)
    self.deleteProjectAct=QtGui.QAction(QtGui.QIcon('delete.png'), '&Delete', self) #delete selected if any
    self.deleteProjectAct.triggered.connect(self.deleteProject)
   
    #self.addProjectAct.triggered.connect(self.wproject.add_item) 
    self.connect(self.wproject.treeWidget, QtCore.SIGNAL("customContextMenuRequested(const QPoint &)"), self.menuContextTree)
    self.connect(self.wproject.treeWidget, QtCore.SIGNAL("itemSelectionChanged()"),self.setProjectFromTreeView)
    
    
  def create_menu(self):
    #self.projectMenu = self.menuBar().addMenu("&Project")
    #self.projectMenu.addAction(self.addProjectAct)   
    #self.projectMenu.addAction(self.deleteProjectAct)
    self.viewMenu=self.menuBar().addMenu("&About")
    workspaceGroup = QtGui.QActionGroup(self)
    import functools
    for item in self.config.workspace:
      name, value = item
      act = QtGui.QAction(name, self, checkable=True)
      act.triggered.connect(functools.partial(self.setProject, name, value)) #not!
      self.wproject.add_item(value,name=name)
      #workspaceGroup.addAction(act)
      #self.projectMenu.addAction(act)
  '''
  def update_ui(self):
    for item in range(self.wproject.treeWidget.topLevelItemCount()):
      #print self.wproject.treeWidget.topLevelItemCount()
      logging.info('remove item %s' %item)
      self.wproject.treeWidget.takeTopLevelItem(item)
    #self.wproject=TreeWidget()
    #self.wproject.parent_type='file'      #configure the treeViewItem scan
    #self.wproject.ext=['*.*']   
    workspaceGroup = QtGui.QActionGroup(self)
    import functools
    for item in self.wapp.config.workspace:
      name, value = item
      act = QtGui.QAction(name, self, checkable=True)
      act.triggered.connect(functools.partial(self.setProject, name, value)) #not!
      self.wproject.add_item(value,name=name)
      workspaceGroup.addAction(act)
    self.setCentralWidget(self.wapp)

  def setAppWidget(self,widget):
    logging.debug('MainWindow::setAppWidget %s' %repr(widget))
    self.wapp=widget
    self.update_ui()
  '''

  def setLog(self,logfilepath):
    logging.debug('AppMainWindow::setLog %s' %logfilepath)
    self.wlog.set_path(logfilepath)
    
  def setFileView(self,path):
    logging.debug('AppMainWindow::setFileView %s' %path)
    self.wfiles.set_path(path)



#--------  Project Management    
  def addProject(self):
    logging.debug( 'MainWindow::addProject' )
    dialog = QtGui.QFileDialog(self)
    dialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)
    dirname = dialog.getExistingDirectory(self, 'Select project folder!', os.path.abspath(os.getcwd()))
    #if not os.path.isfile(os.path.join(dirname, configfilename)):
    #  QtGui.QMessageBox.information(self, title, unicode('%s not found. Create one.' %configfilename))
      #self.wapp.createNewAppConf(dirname)
    _name, _bool = QtGui.QInputDialog.getText(self, 'New Workspace', 'label/name')

    #update widget    
    if _bool == True:
      self.wproject.add_item(dirname,name=_name)
      self.config.create(_name,dirname) #addWorkspace
  
  def setProjectFromTreeView(self):
    #print self.wproject.treeWidget.currentIndex()
    i=self.wproject.treeWidget.currentIndex().row()
    logging.debug('MainWindow::setProjectFromTreeView index %s' %str(i))
    _name,path=self.config.workspace[i]
    self.setProject(_name,path)
    
    
  def setProject(self,name,path):
    logging.debug('MainWindow::setProject : %s' %name)
    if self.parent!=None:
      print self.parent
      if hasattr(self.parent,setProject): # exposed method!
        print 'call parent'
        self.parent.setProject(name,path)
      
    #self.wapp.setWorkspace(name,path) 
    #self.setWorkspace(name,path)  #WARNING
    
    #if on per-project based
    #logfiles=os.path.join(path,logfilename)
    #self.wlog.set_path(logfiles)
    #report_path=os.path.join(self.currentWorkspace,report_path)
    #self.wfiles.set_path(report_path)

  def deleteProject(self):
    logging.debug('MainWindow::delete TreeWidgetItem %s' %self.wproject.treeWidget.currentIndex().row() )
    i=self.wproject.treeWidget.currentIndex().row()
    logging.debug( 'delete item  %s' %i)
    self.wproject.treeWidget.takeTopLevelItem(i)  
    del self.wproject.items[i]

    print type(self.config.workspace) 
    logging.info('MainWindow:: delete from list %s' %repr(self.config.workspace[i]) )
    del self.config.workspace[i]
    self.config.write()
    

  def menuContextTree(self, point):   #projectContextMenuHandler
    item = self.wproject.treeWidget.itemAt(point)
    logging.debug('%s ' %item)
    logging.debug(self.wproject.treeWidget.currentIndex() )
    menu = QtGui.QMenu()
    addAction=menu.addAction(self.addProjectAct)
    deleteAction=menu.addAction(self.deleteProjectAct)
    menu.exec_(QtGui.QCursor.pos())
    #self.connnect(self.treeWidget, ,addAction)


#--------  TOOL LED   
  def startToolProcess(self):
    try:
      self.toolLED.setPixmap(self.led_blue_pixmap)
    except:
      pass

  def endToolProcess(self):
    try:
      self.toolLED.setPixmap(self.led_grey_pixmap)
    except:
      pass
  
#-------- process Timer & LED   
  def startProcessTimer(self):
    self.timer=QtCore.QTimer(self)
    self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.updateProcessTimer)
    self.ptime=0
    self.timer.start(1000)
    try:
      self.processWidget.setPixmap(self.led_green_pixmap)
    except:
      pass
    #if hasattr(self.parent,onStartProcess):
    # parent.onStartProcess()  
      
  def stopProcessTimer(self):
    self.timer.stop()
    try:
      self.processWidget.setPixmap(self.led_grey_pixmap)
    except:
      pass
    
  def updateProcessTimer(self):
    self.ptime+=1
    self.statusbar_timer.display(self.ptime)
    
    
