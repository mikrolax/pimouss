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

try:
  from PySide import QtCore, QtGui,QtWebKit
except:
  raise NameError('Pyside is no installed on your system. Check http://qt-project.org/wiki/PySide for more')

  
class PimoussThread(QtCore.QThread):
    def __init__(self,inputPath,buildPath,generatePath,recursive=None,parent=None):
      super(PimoussThread, self).__init__(parent)
      self.inputPath=inputPath
      self.buildPath=buildPath
      self.generatePath=generatePath
      self.recursive=recursive
      
    def run(self):
      cmd='pimouss.py -b %s -g %s %s' %(self.buildPath,self.generatePath,self.inputPath)
      import subprocess
      message=subprocess.call(cmd,shell=True)
      self.emit(QtCore.SIGNAL("pimoussExecEnd(PyObject)"), str(message))    #should reboot board if timeout exceded...



class PimoussWidget(QtGui.QWidget):
  def __init__(self):
    super(PimoussWidget, self).__init__()
    self.initUI()
    self.pimoussStarted=False
    self.webView=QtWebKit.QWebView() 
    
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
    self.resize(300, 200)

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
    self.newScreenshotButton = self.createButton("Build and Generate",self.process)
    self.buttonsLayout = QtGui.QHBoxLayout()
    self.buttonsLayout.addStretch()
    self.buttonsLayout.addWidget(self.newScreenshotButton)
    #self.buttonsLayout.addWidget(self.saveScreenshotButton)
    #self.buttonsLayout.addWidget(self.quitScreenshotButton)

  def createButton(self, text, member):
    button = QtGui.QPushButton(text)
    button.clicked.connect(member)
    return button


  def updateFolderGroupBox(self):
    self.inputPathText.setText(self.pimoussInput) 
    self.buildPathText.setText(self.pimoussBuild) 
    self.generatePathText.setText(self.pimoussOutput) 
    
  def selectInputPath(self):
    fname = QtGui.QFileDialog.getExistingDirectory(self, 'Select Folder','/home')
    self.pimoussInput=fname
    self.pimoussBuild=fname
    self.pimoussOutput=os.path.join(fname,'_html')
    self.updateFolderGroupBox()
    
  def selectBuildPath(self):
    fname = QtGui.QFileDialog.getExistingDirectory(self, 'Select Folder','/home')
    self.pimoussBuild=fname
    self.updateFolderGroupBox()
    
  def selectGeneratePath(self):
    fname = QtGui.QFileDialog.getExistingDirectory(self, 'Select Folder','/home')
    self.pimoussOutput=fname
    self.updateFolderGroupBox()
      
  def process(self):
    print 'recursive %s' %self.recursive.isChecked()
    if os.path.exists(self.pimoussInput) and not self.pimoussStarted:
      self.thread=PimoussThread(self.pimoussInput,self.pimoussBuild,self.pimoussOutput)
      print 'connect thread'
      self.connect(self.thread, QtCore.SIGNAL("pimoussExecEnd(PyObject)"),self.pimoussEnd)
      print 'try to start thread'
      self.thread.start()
      self.pimoussStarted=True
    else:
      pass

  def wk_preview(self,path):
    pagename=os.path.join(path,'index.html')
    if os.path.exists(pagename):
      print 'try index %s' %pagename
      self.webView.load(pagename)
      self.webView.show()     
    else:
      import glob
      lst=glob.glob(os.path.join(path,'*.html'))
      pagename=lst[0]
      try:
        print 'try  %s' %pagename
        self.webView.load(pagename)
        self.webView.show()    
      except:
        pass
    
  def pimoussEnd(self, msg):
    self.pimoussStarted=False
    if msg=='0':
      message="pimouss successfully finished!\n "
    else:
      message="pimouss error!\n return error code : %s " %msg
    
    #tmp=unicode(string)
    QtGui.QMessageBox.information(self,u"pimouss",message)

    msgBox =QtGui.QMessageBox()
    msgBox.setText(message)
    connectButton = msgBox.addButton(self.tr("Preview"), QtGui.QMessageBox.ActionRole)
    abortButton = msgBox.addButton(QtGui.QMessageBox.Ok)
    msgBox.exec_()
    if msgBox.clickedButton() == connectButton:
      print 'preview %s ' %self.pimoussOutput
      self.wk_preview(self.pimoussOutput)
    elif msgBox.clickedButton() == abortButton:
      print 'abort'

    



class MainWindow(QtGui.QMainWindow):
    def __init__(self):
      super(MainWindow, self).__init__()
      self.initUI()
      
        
    def initUI(self):               
      window=PimoussWidget()
      import pimouss
      self.statusBar().showMessage("using %s" %(pimouss.__version__))
      self.setCentralWidget(window)
      self.setGeometry(300, 300, 350, 250)
      self.setWindowTitle('Pimouss')    
      window.show()
      #self.show()
        

if __name__ == '__main__':
    import sys
    import os
    app = QtGui.QApplication(sys.argv)
    pixmap = QtGui.QPixmap("daria.png")
    splash = QtGui.QSplashScreen(pixmap)
    #splash.setMask(pixmap.mask()) 
    splash.show()
    splash.showMessage("Load pimouss...")
    #app.processEvents()
    import time
    time.sleep(1)
    app.processEvents()
    m=MainWindow()
    m.show()
    splash.finish(m)
    sys.exit(app.exec_())
