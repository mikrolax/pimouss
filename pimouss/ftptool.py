#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Simple FTP tools: somme function to connect and upload, and a Widget (based on PySide) """

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
import ftplib
import logging
import base64
from ConfigParser import SafeConfigParser
try:
  from PySide import QtCore, QtGui, QtNetwork
except:
  pass

default_conf={'ftp_server':'',
              'ftp_login':'',
              'ftp_password':'',
              'ftp_src':'',
              'ftp_dest':'www',
              }

def ftp_connect(host,user,password):
  try:
    ftp=ftplib.FTP(host,user,password)
  except ftplib.all_errors, e:
    logging.error('Error %s' %e)
    return None
  try:
    ftp.login(host,user,password)    
  except ftplib.all_errors, e:
    logging.error('Error %s' %e) 
  return ftp
  
  
def ftp_rec_copy(ftp,src,dest):
    logging.info('FTP Upload begin...') 
    try:
      ftp.cwd(dest)
    except ftplib.all_errors, e:
      try:          #should test if exist before...
        ftp.mkd(dest)
        ftp.cwd(dest)
      except ftplib.all_errors, e:
        return 0
    #recursive copy  
    nb_files=0 
    for root, dirs, files in os.walk(src):
      relpath=os.path.relpath(root,src)
      try:
        ftp.cwd(relpath)
      except ftplib.all_errors, e: 
        logging.error('Error %s' %e)    
      
      for d in dirs:
        try:
          ftp.mkd(os.path.join(relpath,d))
        except ftplib.all_errors, e:       
          logging.error('Error %s' %e) 
      
      for f in files:
        try: 
          fobj = open(os.path.join(root,f),"rb")
          a = "STOR " + f
          ftp.storbinary (a, fobj)
          nb_files+=1
        except ftplib.all_errors, e:        
          logging.error('Error %s' %e) 
          
    logging.info('FTP: Uploded %d files' %nb_files)  
    return nb_files

def _get_default_conf(src_dir):
  conf=default_conf
  conf['ftp_src']=src_dir
  return conf
    
def ftp_read_cfg(filepath,section,src_dir=None): 
  config = SafeConfigParser()
  config.read(filepath)
  if src_dir!=None:
    conf=_get_default_conf(src_dir)
  else:
    conf=default_conf  
  try:
    conf['ftp_server']=config.get(section,'ftp_server')
    conf['ftp_login']=config.get(section,'ftp_login')
    conf['ftp_password']=base64.b64decode(config.get(section,'ftp_password'))
    conf['ftp_src']=config.get(section,'ftp_src')
    conf['ftp_dest']=config.get(section,'ftp_dest')
  except:
    pass
  return conf  
          
def ftp_save_cfg(filepath,section,host,user,password,src,dest): 
  config = SafeConfigParser()
  config.read(filepath)
  #! create section if not existing...
  config.set(section,'ftp_server',host)
  config.set(section,'ftp_login',user)
  config.set(section,'ftp_password',base64.b64encode(password))
  config.set(section,'ftp_src',src)
  config.set(section,'ftp_dest',dest)
  config.write(open(filepath, 'w'))
  
  
  
class FtpWindow(QtGui.QDialog):
  def __init__(self, parent=None):
    QtGui.QDialog.__init__(self, parent)
        
    self.ftpServerLabel = QtGui.QLabel(self.tr("FTP Server:"))
    self.ftpServerLineEdit = QtGui.QLineEdit("")

    self.ftpLoginLabel = QtGui.QLabel(self.tr("Login:"))
    self.ftpLoginLineEdit = QtGui.QLineEdit("")
    self.ftpPasswordLabel = QtGui.QLabel(self.tr("Password:"))
    self.ftpPasswordLineEdit = QtGui.QLineEdit("")
    self.ftpPasswordLineEdit.setEchoMode(QtGui.QLineEdit.Password) #QLineEdit.PasswordEchoOnEdit
    
    self.ftpUploadFromLabel = QtGui.QLabel(self.tr("From:"))
    self.ftpUploadFromLineEdit = QtGui.QLineEdit("")
    self.ftpUploadToLabel = QtGui.QLabel(self.tr("To:"))
    self.ftpUploadToLineEdit = QtGui.QLineEdit("")    

    self.statusLabel = QtGui.QLabel(self.tr("Please enter the name of an FTP server."))    
    #self.statusLabel = QtGui.QTextEdit("") 
    
    self.connectButton = QtGui.QPushButton(self.tr("Connect"))
    self.connectButton.setDefault(True)

    self.saveButton = QtGui.QPushButton(self.tr("Save"))
    self.saveButton.setEnabled(False)
    self.downloadButton = QtGui.QPushButton(self.tr("Upload"))
    self.downloadButton.setEnabled(False)
    self.quitButton = QtGui.QPushButton(self.tr("Quit"))   
    
    topLayout = QtGui.QHBoxLayout()
    topLayout.addWidget(self.ftpServerLabel)
    topLayout.addWidget(self.ftpServerLineEdit)
    
    topLayout2 = QtGui.QGridLayout()
    topLayout2.addWidget(self.ftpLoginLabel,0,0)
    topLayout2.addWidget(self.ftpLoginLineEdit,0,1)
    topLayout2.addWidget(self.ftpPasswordLabel,1,0)
    topLayout2.addWidget(self.ftpPasswordLineEdit,1,1)    
    topLayout2.addWidget(self.ftpUploadFromLabel,2,0)
    topLayout2.addWidget(self.ftpUploadFromLineEdit,2,1)    
    topLayout2.addWidget(self.ftpUploadToLabel,3,0)
    topLayout2.addWidget(self.ftpUploadToLineEdit,3,1)          
    topLayout2.addWidget(self.ftpServerLabel,4,0)
    topLayout2.addWidget(self.ftpServerLineEdit,4,1)
    
    buttonLayout = QtGui.QHBoxLayout()
    buttonLayout.addStretch(1)
    buttonLayout.addWidget(self.saveButton)    
    buttonLayout.addWidget(self.downloadButton)
    buttonLayout.addWidget(self.connectButton)
    buttonLayout.addWidget(self.quitButton)

    mainLayout = QtGui.QVBoxLayout()
    mainLayout.addLayout(topLayout)
    mainLayout.addLayout(topLayout2)          
    mainLayout.addWidget(self.statusLabel)
    mainLayout.addLayout(buttonLayout)
    self.setLayout(mainLayout)
    
    self.setWindowTitle(self.tr("FTP"))  
    self.connect(self.saveButton, QtCore.SIGNAL("clicked()"), self.save)           
    self.connect(self.connectButton, QtCore.SIGNAL("clicked()"), self.connectToFtpServer)    
    self.connect(self.quitButton, QtCore.SIGNAL("clicked()"), self.quit)    
    self.connect(self.downloadButton, QtCore.SIGNAL("clicked()"), self.uploadToFtpServer)  
    self.cfg_filepath='config.ini' # !!!!
    
  def save(self):
    if self.cfg_filepath!=None and self.cfg_section!=None:
      ftp_save_cfg(self.cfg_filepath,
                   self.cfg_section,
                   self.ftpServerLineEdit.text(),
                   self.ftpLoginLineEdit.text(),
                   self.ftpPasswordLineEdit.text(),
                   self.ftpUploadFromLineEdit.text(),
                   self.ftpUploadToLineEdit.text())    
      
  def read(self):
    if self.cfg_filepath!=None and self.cfg_section!=None:  
      values_dict=ftp_read_cfg(self.cfg_filepath,self.cfg_section,self.src_dir)
      self.ftpServerLineEdit.setText(values_dict['ftp_server'])
      self.ftpLoginLineEdit.setText(values_dict['ftp_login'])
      self.ftpPasswordLineEdit.setText(values_dict['ftp_password'])      
      self.ftpUploadFromLineEdit.setText(values_dict['ftp_src'])
      self.ftpUploadToLineEdit.setText(values_dict['ftp_dest'])
      return 0
    else:
      return 1  
   
  def setConfig(self,filepath,section,src_dir=None):
    if os.path.exists(filepath):
      self.cfg_filepath=filepath
      self.cfg_section=section
      if src_dir!=None:
        self.src_dir=src_dir
      if self.read()==0:
        self.saveButton.setEnabled(True)    
      
  def connectToFtpServer(self):
    self.statusLabel.setText('Connecting...') 
    self.ftp=ftp_connect(self.ftpServerLineEdit.text(),self.ftpLoginLineEdit.text(),self.ftpPasswordLineEdit.text())
    if self.ftp!=None:
      self.downloadButton.setEnabled(True) 
      self.statusLabel.setText('Upload files!')  
    else:
      self.statusLabel.setText('Error connecting FTP')
      
  def uploadToFtpServer(self):
    self.statusLabel.setText('Uploading...') 
    nb_files=ftp_rec_copy(self.ftp,self.ftpUploadFromLineEdit.text(),self.ftpUploadToLineEdit.text())
    self.statusLabel.setText('Uploded %d files' %nb_files)
             
  def quit(self):
    try:
      self.ftp.quit()
    except:
      pass
    self.hide()
    
      
if __name__ == '__main__':
  app = QtGui.QApplication(sys.argv)
  ftpWin = FtpWindow()
  sys.exit(ftpWin.exec_())    
