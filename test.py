#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
import unittest
import subprocess
import sys

def generate_data(folder,datas):
  #if not os.path.exists(folder):
  #  print 'make %s' %folder
  #  os.mkdir(folder)
  for md_filename in datas.keys():
    if md_filename!='static':
      print 'generate %s' %(md_filename)
      try:
        codecs.open(os.path.abspath(os.path.join(folder,md_filename)),'w','utf-8').write(datas[md_filename])
      except:
        print 'cannot create %s' %os.path.abspath(os.path.join(folder,md_filename))
    else:
      for static_file in datas['static']:
        src=os.path.join(folder,md_filename)
        dest=os.path.relpath(src,static_file)
        print '%s -> %s' %(src,dest)
        #os.copy(src,dest)
    
def build(inpath,outpath=None):
  print 'pimoussify (as python module) %s' %(inpath)
  from pimouss.pimouss import Pimouss
  pims=Pimouss()
  pims.process(inpath,outpath=outpath)
  
def build_cli(inpath,outpath=None):
  print 'pimoussify (via cmd line) %s' %(inpath)
  cmd_line='python %s' %os.path.join('pimouss','pimouss.py')
  if outpath!=None:
    cmd_line+=' -g %s' %outpath  
  cmd_line+=' %s' %inpath
  #print 'CLI : %s' %cmd_line  
  result=subprocess.call(cmd_line,shell=True)
  return result
  
  
class PimoussTests(unittest.TestCase):  
  """ Test both pimouss as a module and via command-line interface """

  def tst(self,inpath,datas=None,outpath=None):
    if datas!=None: 
      generate_data(inpath,datas)
    #build(inpath,outpath)
    self.tst_module(inpath,outpath=outpath)
    self.tst_cli(inpath,outpath=outpath)
  
  def tst_module(self,inpath,outpath=None):
    """ test pimouss as a module """
    res=build(inpath,outpath)
    #self.assertEqual(res,0)
  
  def tst_cli(self,inpath,outpath=None):
    """ test pimouss command-line interface """
    res=build_cli(inpath,outpath) 
    self.assertEqual(res,0)
  
  
class Test(PimoussTests):
  def test_example_foto(self):
    """ build example/foto """
    from tests.example_foto  import datas as testdatas
    inpath=os.path.join(os.path.join('example','foto'))
    outpath=os.path.join(os.path.join('example','_www'))
    self.tst(inpath,datas=testdatas,outpath=outpath)
    
  def test_example_website(self):
    """ build example/website """
    from tests.example_website  import datas as testdatas
    inpath=os.path.join(os.path.join('example','website'))
    outpath=os.path.join(os.path.join('example','_www','website'))
    self.tst(inpath,datas=testdatas,outpath=outpath)
      
  def test_setup_sdist(self):
    """ source distribution packing test. Depending on platform, try to build binaries.  """  
    subprocess.call('python setup.py sdist > test.log',shell=True)
    if sys.platform == 'win32':
      self.setup_py2exe()
  
  def setup_py2exe(self):
    subprocess.call('python setup.py py2exe > test.log',shell=True)



def clean():
  import shutil
  build=os.path.join('build')
  example=os.path.join('example','_www')
  if os.path.exists(build):
    print 'remove build folder'
    shutil.rmtree(build)
  if os.path.exists(example):
    print 'remove example folder'
    shutil.rmtree(example)

def suite():
  suite = unittest.TestLoader().loadTestsFromTestCase(Test)
  return suite
  
def run():
  test_suite = unittest.TestSuite()
  tests=suite()
  test_suite.addTest(tests)
  unittest.TextTestRunner(verbosity = 2).run(test_suite)

if __name__ == '__main__':
  clean()
  run()

