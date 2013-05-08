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

import os
import logging
from ConfigParser import SafeConfigParser

try:
  from PySide import QtCore,QtGui,QtWebKit
except:
  raise NameError('Pyside is no installed on your system. Check http://qt-project.org/wiki/PySide for more')

class MyProcess(QtCore.QThread):    # or just an object?
  def __init__(self,parent=None):
    super(MyProcess, self).__init__(parent)  
    self.params={}
    
  def set(self,params):
    logging.debug('config.MyProcess::set: %s' %params)
    self.params=params
    
  def run(self):
    logging.debug('config.MyProcess::emit: %s' %self.params)
    self.emit(QtCore.SIGNAL('processStart(PyObject)'), self.params)


class AutoConfigWidget(QtGui.QWidget):
  def __init__(self,parent=None,filepath=None):
    super(AutoConfigWidget, self).__init__(parent)  
    self.config=Config(parent,filepath)
    self.parent=parent          
    if parent !=None:
      self.title=parent.title
      self.icon=parent.icon
    else:
      self.title=None
      self.icon=None
    self.section_name=None
    self.params={}
    self.line_edit=[]
    self.line_edit_dict={} 
    self.check_box_dict={}
    self.currentWorkspace=None
    self.processThread=MyProcess(parent=self)
    self.option_type={}
    self.connect(self.processThread,QtCore.SIGNAL('processStart(PyObject)'),self.onProcessStart)
    self.connect(self.processThread,QtCore.SIGNAL('processEnd(PyObject)'),self.onProcessStop)
    self.init_ui()
        
  #createTab should add tab and a thread worker in a pool
  '''def create_tab(self,section_name):
    #use self.tabs
    try: 
      options=self.config.get_options(section_name)
    except:
      print 'AutoConfigWidget :: create_tab(%s) : section name error' %section_name
      return
    layout=QtGui.QGridLayout() 
    idx=0
    line_edit=[]
    for option in options.keys():
      value=options[option]
      #self.params[option]=value
      layout.addWidget(QtGui.QLabel(option),idx,0)
      widget=QtGui.QLineEdit(value)
      line_edit.append( (option,widget) )
      layout.addWidget(widget,idx,1)
      idx+=1        
    pb_ping=QtGui.QPushButton('Ping')
    pb_save=QtGui.QPushButton('Save')
    pb_process=QtGui.QPushButton('Process')
    import functools
    pb_save.clicked.connect(functools.partial(self.save, section_name))
    pb_process.clicked.connect(functools.partial(self.process, section_name))
    pb_ping.clicked.connect(functools.partial(self.ping, section_name))
    layout.addWidget(pb_ping)
    layout.addWidget(pb_save)
    layout.addWidget(pb_process)
    frame=QtGui.QFrame()
    frame.setLayout(layout)  
    self.line_edit_dict[section_name]=line_edit  
    self.tabs.addTab(frame,unicode(section_name))'''
      
  def init_ui(self):
    layout=QtGui.QGridLayout()
    self.layout=QtGui.QVBoxLayout() 
    #get option step if any?
    options=self.config.get_options('OPTIONS')
    idx=0
    
    for option in options.keys():
      if 'type_' in option:
        print 'option type ________________________________'
        print option
        self.option_type[option]=options[option]
                   
    for option in options.keys():
      #if option=='step':
      #  self.tabs=QtGui.QTabWidget()
      #  print '________________________________'
      #  print option
      #  steps_tmp=options[option]
      #  steps=[ step.strip() for step in steps_tmp[1:-1].split(',')] #
      #  print steps
      #  for step in steps:
      #    print step
      #    self.create_tab(step)
      if option=='args':
        args_tmp=options[option]
        args=[ x.strip() for x in args_tmp[1:-1].split(',')]
        print '________________________________'
        print args  
      elif option=='options':
        option_tmp=options[option]
        opt=[ x.strip() for x in option_tmp[1:-1].split(',')]
        print '________________________________'
        print opt         
      else:
        #add to general groupbox
        #self.add_general(options[option]) #type,idx,label,value -> (bool,0,'some option',False) / (path,0,'some path','')
        print '________________________________'
        if not 'type_' in option:
          value=options[option]          
          self.params[option]=value
          if 'path' in self.option_type['type_%s' %option]:
            layout.addWidget(QtGui.QLabel(option),idx,0)
            widget=QtGui.QLineEdit(value)
            self.line_edit.append( (option,widget) )
            layout.addWidget(widget,idx,1) 
            change_pb=QtGui.QPushButton('Change')
            layout.addWidget(change_pb,idx,2) 
            #change_pb.connect.clicked(self.change)
            #self.line_edit_dict[section_name]=
            self.line_edit_dict[option]=widget
            import functools
            change_pb.clicked.connect( functools.partial(self.change, widget) )
            
          elif 'bool' in  self.option_type['type_%s' %option]:
            layout.addWidget(QtGui.QLabel(option),idx,0)
            widget=QtGui.QCheckBox() #add name?
            self.line_edit.append( (option,widget) )
            layout.addWidget(widget,idx,1) 
            self.check_box_dict[option]=widget
          else:
            layout.addWidget(QtGui.QLabel(option),idx,0)
            widget=QtGui.QLineEdit(value)
            self.line_edit.append( (option,widget) )
            self.line_edit_dict[option]=widget
            layout.addWidget(widget,idx,1)           
                 
          idx+=1     
    print self.params

    pb_save=QtGui.QPushButton('Save')
    self.pb_process=QtGui.QPushButton('Process')
    #import functools
    pb_save.clicked.connect(self.save)
    #self.pb_process.clicked.connect(functools.partial(self.process, self.params)) #self.params
    self.pb_process.clicked.connect(self.process)
    layout.addWidget(pb_save,idx,1)
    layout.addWidget(self.pb_process,idx,2)
        
    frame=QtGui.QFrame()       
    frame.setLayout(layout)
    self.layout.addWidget(frame)      
    #self.layout.addWidget(self.tabs) 
    self.setLayout(layout)
    #self.setWindowTitle(self.title)
    self.setWindowIcon(QtGui.QIcon(self.icon))

  def addWorkspace(self,_name,path):
    logging.debug('AutoConfigWidget:: addWorkspace %s' %path)
    self.config.create(_name, path)
    for key in self.params:
      self.config.config.set(_name,key,self.params[key])
    #self.set_params(_name)

  def setWorkspace(self, _name, path):
    logging.debug('AutoConfigWidget:: setWorkspace %s' %path)
    self.currentWorkspace=path
    self.section_name=_name
    #self.set_params(_name)
    self.update_params()
    #self.init_ui()
  
  def update_params(self):
    #read config and update widget accordingly
    for key in self.config.config.options(self.section_name) :
      print '%s config key %s' %(self.section_name,key)
      value=self.config.config.get(self.section_name,key)
      print '%s config value %s' %(self.section_name,value)
      self.params[key]=value
      if 'True' in value:
        self.check_box_dict[key].setCheckState(QtCore.Qt.CheckState(QtCore.Qt.Checked))
      elif 'False' in value:
        self.check_box_dict[key].setCheckState(QtCore.Qt.CheckState(QtCore.Qt.Unchecked))
      else:
        self.line_edit_dict[key].setText(value)
      #else:
      #  pass

    
  def set_params(self,section_name):
    logging.debug('AutoConfigWidget:: set_params %s' %section_name)
    #self.section_name=section_name
    print 'AutoConfigWidget: set_params'
    print self.params
    #print self.line_edit   
    for key in self.params.keys():
      #self.params[key]=self.params
      self.config.config.set(section_name,key,self.params[key])
      
      #self.line_edit[key].setText(self.params[key])
    #self.init_ui()
    
  def save(self,section_name=None): #save options only?
    if section_name != None:
      for item in self.line_edit_dict[section_name]:
        option,value=item
        print 'AutoConfigWidget save ',
        print value.text()
        self.config.config.set(section_name,option,value.text())
      for item in self.check_box_dict.keys():
        self.config.config.set(section_name,item,str(self.check_box_dict[item].isChecked()) )
    else:    
      for item in self.line_edit:
        print item
        option,value=item
        print 'AutoConfigWidget save ',
        print value.text()
        self.config.config.set(self.section_name,option,value.text())
      
      for item in self.check_box_dict.keys():
        self.config.config.set(self.section_name,item,str(self.check_box_dict[item].isChecked()) )
    self.config.write()

  def change(self,line_edit):
    print 'AutoConfigWidget change'
    dialog = QtGui.QFileDialog(self)
    dialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)
    dirname = dialog.getExistingDirectory(self, 'Select folder!', os.path.abspath(self.currentWorkspace))    
    line_edit.setText(dirname)
    self.save()
    self.update_params()
    #self.config.section_name
    
    
  def process(self):
    print 'AutoConfigWidget::process %s %s' %(self.currentWorkspace,self.params)
    if os.path.exists(self.currentWorkspace):
      self.processThread.set(self.params)
      self.processThread.start()
      #p.join()
      
  def onProcessStart(self,msg):
    print 'AutoConfigWidget::onProcessStart: %s' %msg
      
  def onProcessStop(self,ret):
    msg='AutoConfigWidget::onProcessStop : %s' %ret  
    if ret!=0:
      logging.error(msg)
      QtGui.QMessageBox.warning(self, u'Error', unicode(msg))  



class Config(object):
  """ Simple config holder """
  def __init__(self,parent=None,filepath=None):
    logging.debug('Config :: __init__')
    #parent
    #self.parent=parent
    self.config = SafeConfigParser()
    self.workspace = []
    if filepath==None:
      self.filepath='config.ini'
    else:
      self.filepath=filepath
    self.read()
      
  def create(self, name, path):
    logging.info('Config :: create %s / %s' %(name,path))
    self.config.set('WORKSPACE', name, path) #??    
    self.workspace.append((name, path))
    self.config.add_section(name)
    self.write()

  def read(self):
    self.workspace=[]
    logging.info('Config :: read %s '%self.filepath)
    try:
      self.config.read(self.filepath)
    except:
      return -1
    try:
      for option in self.config.options('WORKSPACE'):
        self.workspace.append((option, self.config.get('WORKSPACE', option)))
        logging.debug('Config :: option : %s / %s ' %(option, self.config.get('WORKSPACE', option)) )
    except:
      self.config.add_section('WORKSPACE')
      self.write()
      self.read()
    try:
      for option in self.config.options('OPTIONS'):
        #self.workspace.append((option, self.config.get('OPTIONS', option)))
        logging.debug('Config :: option : %s / %s ' %(option, self.config.get('OPTIONS', option)) )
    except:
       self.config.add_section('OPTIONS')
       self.write()
       self.read()   
    #self.read_projects()   
    return self.workspace


  def set_section(self,section_name,options_dict):
    for key in options_dict.keys():
      self.config.set(section_name,key,options_dict[key])
  
  #def remove_section(self,section_name)
  #
  #def delete_workspace(self,name)#or index?
  
  def get_options(self,section_name):
    self.current_option_dict={}
    for option in self.config.options(section_name):
      self.current_option_dict[option]=self.config.get(section_name,option)  
    return self.current_option_dict
  
  def write(self):
    logging.info('Config :: write config.ini' )
    logging.debug( self.workspace )
    
    self.config.remove_section('WORKSPACE')
    self.config.add_section('WORKSPACE')
    for name, path in self.workspace:
      self.config.set('WORKSPACE', name, path)
    self.config.write(open(self.filepath, 'w'))
    self.read()
    
