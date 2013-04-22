#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import glob
import logging

try:
  from PySide import QtCore,QtGui
except:
  raise NameError('Pyside is no installed on your system. Check http://qt-project.org/wiki/PySide for more')


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


group_box_name='Projects'
window_title='Project Widget'
parent_icon=os.path.join(_module_path(),'static','icon.png')
#top_lvl_icon=QtGui.QIcon(parent_icon)
#child_icon=QtGui.QIcon(parent_icon)

#parent_icon=AppMainWindow.icon

# options
parent_type ='folder'  #in 'folder' or file
ext         =None      #
child_ext   =['*.*']   #

class TreeWidget(QtGui.QWidget):
  def __init__(self):
    super(TreeWidget, self).__init__()    
    self.parent_type=parent_type
    self.ext=ext
    self.child_ext=child_ext
    self.items=[]
    self.init_ui()
  
  def init_ui(self): 
    logging.debug('TreeWidget::init_ui')   
    self.projectNavGroupBox=QtGui.QGroupBox(group_box_name)
    self.treeWidget = QtGui.QTreeWidget()
    self.treeWidget.setColumnCount(1)
    self.treeWidget.setHeaderLabel('Name')
    groupBoxLayout=QtGui.QGridLayout()
    groupBoxLayout.addWidget(self.treeWidget)
    self.projectNavGroupBox.setLayout(groupBoxLayout)
 
    #self.setContextMenuPolicy(Qt.ActionsContextMenu)
    self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    #self.connect(self.treeWidget, QtCore.SIGNAL("customContextMenuRequested(const QPoint &)"), self.menuContextTree) OVERRIDE IT IN MAIN WINDOW

    self.layout = QtGui.QHBoxLayout()
    self.layout.addWidget(self.projectNavGroupBox)    
    self.setLayout(self.layout)
    self.setWindowTitle(window_title)
    #self.show()

  #should add action!
  
  def menuContextTree(self, point):#TreeContextMenuHandler
    item = self.treeWidget.itemAt(point)
    logging.debug(self.treeWidget.currentIndex())
    menu = QtGui.QMenu()
    addAction=menu.addAction('Add')
    deleteAction=menu.addAction('Delete')
    menu.exec_(QtGui.QCursor.pos())
    #self.connnect(self.treeWidget, ,addAction)
    
  def set_config(self,parent_type=None,ext=None,child_ext=None):
    if parent_type != None and parent_type in ['folder','file']:
      self.parent_type=parent_type
    if ext !=None:            #check if list
      self.ext=ext    
    if child_ext!=None:       #check if list
      self.child_ext=child_ext
    
  def add_item(self,path,name=None):
    logging.debug('TreeWidget::add_item %s' %path)
    if name!=None:
      current_name=name
    else:
      current_name=os.path.basename(path)
    logging.debug('current_name : %s' %current_name) 
    child_lst=[]
    if self.parent_type =='file':
      logging.debug('+ add item:%s' %current_name)
      parentItem=QtGui.QTreeWidgetItem(self.treeWidget, [str(current_name)])
      try:
        parentItem.setIcon(0, QtGui.QIcon(parent_icon))
      except:
        pass
      for ext in self.ext:
        child_lst=glob.glob(os.path.join(path,ext))
        for child in child_lst:
          logging.debug('+ add child:%s' %child)
          childItem=QtGui.QTreeWidgetItem(parentItem, [str(child)])
          parentItem.addChild(childItem)
      self.items.append(parentItem)  
    elif self.parent_type=='folder':
      for item in os.listdir(path):
        if os.path.isdir(os.path.join(path,item)):          
          logging.debug('add item:%s' %os.path.basename(item) )
          parentItem=QtGui.QTreeWidgetItem(self.treeWidget, [os.path.basename(item)])
          try:
            parentItem.setIcon(0, QtGui.QIcon(parent_icon))
          except:
            pass
          for ext in self.child_ext:
            child_lst=glob.glob(os.path.join(path,item,ext)) 
            for child in child_lst:
              logging.debug('+ add child:%s' %os.path.basename(child) )
              childItem=QtGui.QTreeWidgetItem(parentItem, [str(os.path.basename(child))])
              parentItem.addChild(childItem)
          self.items.append(parentItem)  
    else:
      pass  
    self.treeWidget.insertTopLevelItems(0, self.items)
         

    
    
    
    
    
    
