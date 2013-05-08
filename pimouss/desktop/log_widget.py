#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Simple threaded logfile viewer using pyside """

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

import os
import time
import logging

try:
  from PySide import QtCore,QtGui
except:
  raise NameError('Pyside is no installed on your system. Check http://qt-project.org/wiki/PySide for more')

group_box_name=''
window_title='Log'
welcome_msg='Welcome!'

#window_title=AppMainWindow.title
#=AppMainWindow.icon

class LogThread(QtCore.QThread):
  def __init__(self,parent=None):
    super(LogThread, self).__init__(parent)
    self.logfile=None
    self.state='initialized'
    self.tmp_content=''
    
  def run(self):
    logging.debug('LogThread::run')
    while(1):
      while(self.state=='started'):
        if self.logfile!=None and os.path.isfile(self.logfile):
          s=open(self.logfile,'r').read()
          if s != self.tmp_content:
            self.tmp_content=s
            self.emit(QtCore.SIGNAL('updateLog(PyObject)'), s) 
        else:
          s='logfile path error: %s' %self.logfile
          self.emit(QtCore.SIGNAL('updateLog(PyObject)'), s) 
          self.state='stopped'
        time.sleep(1)
                
  def stop(self):
    logging.debug('LogThread::stop')
    self.state='stopped'
      
  def set_filepath(self,filepath):
    logging.debug('LogThread::set_filepath : %s' %os.path.abspath(filepath) )
    self.logfile=filepath  
    self.state='started'



class LogWidget(QtGui.QWidget):
  def __init__(self):
    super(LogWidget, self).__init__()    
    self.init_ui()
    self.thread=LogThread() #add path
    #self.logfilelst=logfiles
    
  def init_ui(self):
    logging.debug('LogWidget::init_ui')
    self.logGroupBox=QtGui.QGroupBox(group_box_name)
    self.log=QtGui.QTextEdit()
    groupBoxLayout=QtGui.QGridLayout()
    groupBoxLayout.addWidget(self.log)
    self.logGroupBox.setLayout(groupBoxLayout)

    self.layout = QtGui.QHBoxLayout()
    self.layout.addWidget(self.logGroupBox)    
    self.setLayout(self.layout)
    self.setWindowTitle(window_title) 
    self.log.setText(welcome_msg)
    #self.show()

  def clearLog(self):
    open(self.logfile,'w').close()
    
  def updateLog(self, msg):
    #self.log.setText(msg)
    self.log.clear()
    self.log.append(msg)
      
  def set_path(self,filepath):
    logging.debug('LogWidget::set_path %s' %filepath)  
    self.thread.stop()
    self.thread.set_filepath(filepath)
    self.connect(self.thread, QtCore.SIGNAL('updateLog(PyObject)'), self.updateLog)
    self.thread.start()
    
  def process(self):
    logging.debug('LogWidget::process')  
    self.connect(self.thread, QtCore.SIGNAL('updateLog(PyObject)'), self.updateLog)
    self.thread.start()
      
