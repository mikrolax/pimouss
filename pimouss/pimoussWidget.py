#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Simple Pyside Widget """

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
from PySide import QtCore, QtGui,QtWebKit
from ConfigParser import SafeConfigParser

import pimouss
__version__=pimouss.__version__

def _we_are_frozen():
    """Returns whether we are frozen via py2exe.  This will affect how we find out where we are located."""
    return hasattr(sys, "frozen")
def _module_path():
    """ This will get us the program's directory, even if we are frozen using py2exe"""
    if _we_are_frozen():
        return os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding( )))
    return os.path.dirname(unicode(__file__, sys.getfilesystemencoding( )))  

    
class PimoussThread(QtCore.QThread):
    def __init__(self,parent=None):
      super(PimoussThread, self).__init__(parent)
      self.inputPath=None
      self.buildPath=None
      self.generatePath=None
      self.recursive=None
    
    def setParams(self,inputPath,buildPath,generatePath,recursive=None):
      self.inputPath=inputPath
      self.buildPath=buildPath
      self.generatePath=generatePath
      self.recursive=recursive

    def run(self):
      #if self.buildPath == None:
      message='processing...'
      self.emit(QtCore.SIGNAL("pimoussProcessStart(PyObject)"), str(message))
      self.buildPath=self.inputPath
      #if self.generatePath == None:
      #  self.generatePath=os.path.join(self.inputPath,'_html')
      p=pimouss.Pimouss()
      res=p.process(self.inputPath,buildpath=self.buildPath,outpath=self.generatePath) 
      message='return %s ' %res
      self.emit(QtCore.SIGNAL("pimoussProcessEnd(PyObject)"), str(message))


class PimoussConfigWidget(QtGui.QWidget):
  def __init__(self):
    super(PimoussConfigWidget, self).__init__()
    self.__version__=pimouss.__version__
    self.pimoussInput=None
    self.pimoussBuild=None
    self.pimoussOutput=None
    self.initUI()
    self.config_file='config.ini' #!Warning
    self.config = SafeConfigParser()
    

  def initUI(self):
    self.createFilepathGroupBox()
    self.createOptionsGroupBox()
    self.createButtonsLayout()
    mainLayout = QtGui.QVBoxLayout()    
    mainLayout.addWidget(self.filepathGroupBox)
    mainLayout.addWidget(self.optionsGroupBox)    
    mainLayout.addLayout(self.buttonsLayout)        
    self.setLayout(mainLayout)
    self.setWindowTitle("Pimouss")    

  def createFilepathGroupBox(self):
    self.filepathGroupBox=QtGui.QGroupBox("File/Folder")
    self.inputPathLabel =QtGui.QLabel('Content Folder:')    
    self.inputPathText  =QtGui.QLineEdit()
    self.inputPathButton=self.createButton("Select",self.selectInputPath)
    self.buildPathLabel=QtGui.QLabel('Build path:')    
    self.buildPathText =QtGui.QLineEdit()
    self.buildPathButton  =self.createButton("Change",self.selectBuildPath)
    self.generatePathLabel=QtGui.QLabel('Output Folder:')    
    self.generatePathText =QtGui.QLineEdit()
    self.generatePathButton  =self.createButton("Change",self.selectGeneratePath)
    filepathGroupBoxLayout=QtGui.QGridLayout()
    filepathGroupBoxLayout.addWidget(self.inputPathLabel,0,0)
    filepathGroupBoxLayout.addWidget(self.inputPathText,0,1)    
    filepathGroupBoxLayout.addWidget(self.inputPathButton,0,2)
    filepathGroupBoxLayout.addWidget(self.buildPathLabel,1,0)
    filepathGroupBoxLayout.addWidget(self.buildPathText,1,1)    
    filepathGroupBoxLayout.addWidget(self.buildPathButton,1,2)
    filepathGroupBoxLayout.addWidget(self.generatePathLabel,2,0)
    filepathGroupBoxLayout.addWidget(self.generatePathText,2,1)    
    filepathGroupBoxLayout.addWidget(self.generatePathButton,2,2)
    self.filepathGroupBox.setLayout(filepathGroupBoxLayout)

  def createOptionsGroupBox(self):
    self.optionsGroupBox = QtGui.QGroupBox("Options")
    self.recursive = QtGui.QCheckBox("Recursive")
    optionsGroupBoxLayout = QtGui.QGridLayout()
    optionsGroupBoxLayout.addWidget(self.recursive, 1, 0, 1, 2)
    self.optionsGroupBox.setLayout(optionsGroupBoxLayout)

  def createButtonsLayout(self):
    self.saveButton = self.createButton("Save",self.save)
    self.saveButton.setToolTip('Save this config')  
    self.saveButton.setIcon(QtGui.QIcon(os.path.join(_module_path(),'static','img','glyphicons_206_ok_2.png')))     
    self.closeButton = self.createButton("Close",self.hide)  
    self.closeButton.setToolTip('Close config window')  
    self.closeButton.setIcon(QtGui.QIcon(os.path.join(_module_path(),'static','img','glyphicons_207_remove_2.png')))         
    self.buttonsLayout = QtGui.QHBoxLayout()
    self.buttonsLayout.addStretch()
    self.buttonsLayout.addWidget(self.saveButton)
    self.buttonsLayout.addWidget(self.closeButton)
    
  def createButton(self, text, member):
    button = QtGui.QPushButton(text)
    button.clicked.connect(member)
    return button
  
  def updateFolderGroupBox(self):
    logging.debug('PimoussConfigWidget::updateFolderGroupBox: input: %s,build: %s,out:%s' %(self.pimoussInput,self.pimoussBuild,self.pimoussOutput))
    self.inputPathText.setText(self.pimoussInput) 
    self.buildPathText.setText(self.pimoussBuild) 
    self.generatePathText.setText(self.pimoussOutput) 
    
  def selectInputPath(self):
    fname = QtGui.QFileDialog.getExistingDirectory(self, 'Select Folder','/home')
    self.pimoussInput=fname
    #self.pimoussBuild=fname
    #self.pimoussOutput=os.path.join(fname,'_www')
    self.updateFolderGroupBox()
    
  def selectBuildPath(self):
    fname = QtGui.QFileDialog.getExistingDirectory(self, 'Select Folder','/home')
    self.pimoussBuild=fname
    self.updateFolderGroupBox()
    
  def selectGeneratePath(self):
    fname = QtGui.QFileDialog.getExistingDirectory(self, 'Select Folder','/home')
    self.pimoussOutput=fname
    self.updateFolderGroupBox()
  
  def read(self,section_name,base_path):
    self.config.read(self.config_file)
    self.section_name=section_name
    self.pimoussInput=os.path.abspath(base_path)
    self.pimoussBuild=os.path.abspath(base_path)
    self.pimoussOutput=os.path.join(os.path.abspath(base_path),'_www')
    try:
      self.pimoussInput=self.config.get(section_name,'inpath',)
      self.pimoussBuild=self.config.get(section_name,'buildpath',)
      self.pimoussOutput=self.config.get(section_name,'outpath',)
      self.config.get(section_name,'recursive',False)
    except:
      pass
    self.save()
          
  def update(self,section_name,base_path):
    self.read(section_name,base_path)
    self.updateFolderGroupBox()
    return self.pimoussOutput
      
  def save(self):
    if not self.config.has_section(self.section_name):
      self.config.add_section(self.section_name)
    self.config.set(self.section_name,'inpath',self.pimoussInput)
    self.config.set(self.section_name,'buildpath',self.pimoussBuild)
    self.config.set(self.section_name,'outpath',self.pimoussOutput)
    if self.recursive.isChecked():
      self.config.set(self.section_name,'recursive','True')        
    else:  
      self.config.set(self.section_name,'recursive','False')  
    self.config.write(open(self.config_file, 'w'))
    self.hide()
  #def hide(self):  
    
    
    
class PimoussWidget(QtGui.QWidget):
  def __init__(self):
    super(PimoussWidget, self).__init__()
    self.__version__=pimouss.__version__
    self.__project__='pimouss'
    self.initUI()
    self.pimoussStarted=False
    self.webView=QtWebKit.QWebView() 
    self.thread=PimoussThread()
    self.connect(self.thread, QtCore.SIGNAL("pimoussProcessEnd(PyObject)"),self.pimoussEnd) 
    self.wConf=PimoussConfigWidget()
    
    import ftptool
    self.wFTP=ftptool.FtpWindow()
            
  def initUI(self):
    self.createButtonsLayout()
    mainLayout = QtGui.QVBoxLayout()    
    url='welcome.html'        # !! use os.path.abspath(_module_path(),'static',welcome.html)
    self.mWebView = QtWebKit.QWebView()
    self.mWebView.load(url)
    self.mWebView.settings().setAttribute(QtWebKit.QWebSettings.LocalContentCanAccessRemoteUrls, True)
    self.mWebView.settings().setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
    self.mWebView.settings().setAttribute(QtWebKit.QWebSettings.JavascriptEnabled, True)
    self.mWebView.settings().setAttribute(QtWebKit.QWebSettings.LocalContentCanAccessFileUrls, True)  
    configLayout = QtGui.QHBoxLayout()    
    configLayout.addLayout(self.buttonsLayout)    
    mainLayout.addLayout(configLayout)
    mainLayout.addWidget(self.mWebView)
            
    self.setLayout(mainLayout)
    self.setWindowTitle("Pimouss")
    #self.setHTMLView(os.path.join('desktop','static','welcome.html'))  # !! use os.path.abspath(_module_path(),'static',welcome.html)


  def createButtonsLayout(self):
    self.configButton = self.createButton("Config",self.showConfig)
    self.configButton.setToolTip('Click here to see this pimouss config!')
    self.configButton.setIcon(QtGui.QIcon(os.path.join(_module_path(),'static','img','glyphicons_137_cogwheels.png'))) 
    self.configButton.setEnabled(False)

    self.buildButton = self.createButton("HTML-ize",self.process)
    self.buildButton.setToolTip('Click here to launch this pimouss!')
    self.buildButton.setIcon(QtGui.QIcon(os.path.join(_module_path(),'static','img','glyphicons_081_refresh.png')))     
    self.buildButton.setEnabled(False)
 
    self.helpButton = self.createButton("",self.help)
    self.helpButton.setToolTip('Click here to view Help')
    self.helpButton.setIcon(QtGui.QIcon(os.path.join(_module_path(),'static','img','glyphicons_194_circle_question_mark.png')))     

    self.ftpButton = self.createButton("FTP",self.showFTP)
    self.ftpButton.setToolTip('Upload generated website via FTP')
    self.ftpButton.setIcon(QtGui.QIcon(os.path.join(_module_path(),'static','img','glyphicons_363_cloud_upload.png')))     
    self.ftpButton.setEnabled(False)
       
    self.buttonsLayout = QtGui.QHBoxLayout()
    self.buttonsLayout.addStretch()
    self.buttonsLayout.addWidget(self.configButton)
    self.buttonsLayout.addWidget(self.buildButton)
    self.buttonsLayout.addWidget(self.ftpButton)   
    self.buttonsLayout.addWidget(self.helpButton) 
    
  def createButton(self, text, member):
    button = QtGui.QPushButton(text)
    button.clicked.connect(member)
    return button

  def setHTMLView(self,url): 
    print 'loading %s' %url
    #self.mWebView.load(QtCore.QUrl(url))
    self.mWebView.load(QtCore.QUrl.fromLocalFile(url))
  
  def showConfig(self):
    self.wConf.show()
  
  def showFTP(self):
    self.wFTP.show()
    
  def help(self):
    self.setHTMLView(os.path.join(_module_path(),'static','welcome.html'))
    
  def update(self,name,inpath):
    self.configButton.setEnabled(True)
    self.buildButton.setEnabled(True)
    self.ftpButton.setEnabled(True)
    self.wConf.update(name,inpath)
    self.wFTP.setConfig('config.ini',name,src_dir=self.wConf.pimoussOutput) 
    if self.wConf.pimoussOutput != None:
      if os.path.exists(os.path.join(self.wConf.pimoussOutput,'index.html')):
        self.setHTMLView(os.path.join(self.wConf.pimoussOutput,'index.html'))
    return self.wConf.pimoussOutput

  def process(self):
    #print 'recursive %s' %self.wConf.recursive.isChecked()
    if os.path.exists(self.wConf.pimoussInput) and not self.pimoussStarted:
      self.thread.setParams(self.wConf.pimoussInput,self.wConf.pimoussBuild,self.wConf.pimoussOutput)
      self.thread.start()
      self.pimoussStarted=True
    else:
      pass  
       
  def pimoussEnd(self, msg):
    self.pimoussStarted=False
    if msg=='0':
      message="pimouss successfully finished!\n "
    else:
      message="pimouss error!\n return error code : %s " %msg
    #tmp=unicode(string)
    QtGui.QMessageBox.information(self,u"Pimouss",message)
    msgBox =QtGui.QMessageBox()
    msgBox.setText(message)
    connectButton = msgBox.addButton(self.tr("Preview"), QtGui.QMessageBox.ActionRole)
    abortButton = msgBox.addButton(QtGui.QMessageBox.Ok)
    msgBox.exec_()
    if msgBox.clickedButton() == connectButton:
      print 'preview %s ' %self.wConf.pimoussOutput
      self.wk_preview(self.wConf.pimoussOutput)
    elif msgBox.clickedButton() == abortButton:
      print 'abort'
      
  def wk_preview(self,path):
    pagename=os.path.join(path,'index.html')
    if os.path.exists(pagename):
      print 'try index %s' %pagename
      self.webView.load(pagename)
      self.webView.show()     
    else:
      import glob
      lst=glob.glob(os.path.join(path,'*.html'))
      if len(lst)>0:
        pagename=lst[0]
        try:
          print 'try  %s' %pagename          
          print 'wk_preview %s ' %pagename
          self.webView.load(pagename)
          self.webView.show()    
        except:
          pass
      else:
        pass



    
