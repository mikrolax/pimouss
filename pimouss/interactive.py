#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" simple interactive command line interface for pimouss """

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

import cmd
import os
import sys
import glob

try:
  import pimouss
  import desktop.config
  __version__=pimouss.__version__
except:
  sys.exit(-1)
  
  
  
def _we_are_frozen():
  return hasattr(sys, "frozen")
def _module_path():
  if _we_are_frozen():
    return os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding( )))
  else:
    return os.path.dirname(os.path.abspath(__file__))
 
 
 
class Tools(cmd.Cmd): 
  pimouss_list=[]
  project_config_list=glob.glob(os.path.join(_module_path(),'*.cfg'))

  def __init__(self):
    cmd.Cmd.__init__(self)
    self.prompt = 'pimouss.tools> '
    self.intro  =  ' \n pimouss v.%s tools utilities \n\n \tType help to list available commands\n' %__version__
    
    self.cfg=desktop.config.Config() #add filepah=iglou.cfg
    self.do_load('config.ini') #!!
    
    self.pimousses=None
    self.pimouss=pimouss.Pimouss()
    
  def do_clean(self,line):
    " remove lib and build folder "    
    #folder_lis=['build','dist']
    pass
  
  # Config management
  def do_load(self,line):
    " load project configuration " 
    print line
    filepath=os.path.join(_module_path(),line)
    print filepath
    self.cfg.filepath=filepath
    self.pimousses=self.cfg.read()
    
    if self.pimousses==-1:
      sys.stderr.write('Error reading configuration file %s' %filepath)
    else:  
      self.pimouss_list=[]
      for name,path in self.pimousses:
        self.pimouss_list.append(name)

  def do_save(self,line):
    " save config into [filename] file "   
    #if empty, use config.ini
    self.cfg.write()   

  def do_save_as(self,line):
    " save config into [filename] file "   
    self.cfg.filepath=os.path.join(_module_path(),line)
    self.cfg.write()


  # Pimousses management
  def do_add(self,line):
    " add a pimouss to the project "
    if line=='':
      line=raw_input('Name:')

    path=raw_input('Project %s input path :' %line)
    if not os.path.exists(os.path.abspath(path)):
      print 'not valid path: %s Try again!' %os.path.abspath(path)
      self.do_add(line)
      
    self.cfg.create(line,path)
    self.pimousses=self.cfg.read()
    self.pimouss_list=[]
    for name,path in self.pimousses:
      self.pimouss_list.append(name)

  def do_delete(self,line):
    " delete a pimouss from the project "
    print "not implemented!"
    pass
  
  def do_list(self,line):
    " display defined pimouss's "
    sys.stdout.write('Input file :\n \t%s \nDefined pimousses:\n' %self.cfg.filepath)
    for item in self.pimouss_list:
      sys.stdout.write('\t %s\n' %item)
      
  def do_run(self,line):
    " process a pimouss defined in config"
    print 'run pimouss %s' %line
    for name,path in self.pimousses: #or pimouss_list?
      if name==line:
        self.pimouss.process(inpath=path,outpath=os.path.join(path,'_www'))

  # iterate over defined pimoussees
  def do_run_all(self,line):
    " process a pimouss defined in config"
    for name,path in self.pimousses: #or pimouss_list?
      self.do_run(name)

  #def sendftp(self,line):
        
      
  # completion management
  def complete_load(self, text, line, begidx, endidx):
    if not text:
      completions = self.project_config_list[:]
    else:
      completions = [ f for f in self.project_config_list if f.startswith(text) ]
    return completions 

  def complete_run(self, text, line, begidx, endidx):
    if not text:
      completions = self.pimouss_list[:]
    else:
      completions = [ f for f in self.pimouss_list if f.startswith(text) ]
    return completions 
  
  def complete_delete(self, text, line, begidx, endidx):
    if not text:
      completions = self.pimouss_list[:]
    else:
      completions = [ f for f in self.pimouss_list if f.startswith(text) ]
    return completions
    
    
    
  def do_EOF(self, line):
    return True
  def emptyline(self):
    pass   
  def do_shell(self, line):
    "Run a shell command. Or use ! before command."
    self.stdout.write( 'running shell command: %s \n' %line)
    output = os.popen(line).read()
    print output
    self.last_output = output    
  def do_quit(self, arg):
    " Exit program"
    sys.exit(1)
        
  # shortcuts
  do_q = do_quit
  
  
  
def main():
  import logging
  formatter='%(asctime)s::%(levelname)s::%(message)s'
  logging.basicConfig(filename='pimouss.log',format=formatter,level=logging.DEBUG)
  import sys
  if len(sys.argv) > 1: # i.e. python test.py start/run 
      Tools().onecmd(' '.join(sys.argv[1:]))
  else:
      Tools().cmdloop()

if __name__ == '__main__':
  main()
    
