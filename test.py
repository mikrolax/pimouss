#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
import unittest
import subprocess
import sys
import shlex
try:
    import cStringIO
    StringIO = cStringIO
except ImportError:
    import StringIO

#command line generator
cmdlines    =[('cmd.md','python pimouss/pimouss.py -h','')]
cmd_init    =[('cmd.init.md','python pimouss/pimouss.py init -h',''),
              ('cmd.init.md','python pimouss/pimouss.py -d init doc','init doc folder')]
cmd_build   =[('cmd.build.md','python pimouss/pimouss.py build -h',''),
              ('cmd.build.md','python pimouss/pimouss.py -d build -of _www doc','get all markdown file. build doc folder')]
cmd_generate=[('cmd.generate.md','python pimouss/pimouss.py generate -h',''),
              ('cmd.generate.md','python pimouss/pimouss.py -d generate -of doc/_www doc','generate html for doc folder')]
cmd_make    =[('cmd.make.md','python pimouss/pimouss.py make -h',''),
              ('cmd.make.md','python pimouss/pimouss.py -d make -of doc/_www doc ','build & generate doc folder'),
              ('cmd.make.md','python pimouss/pimouss.py -d make -tstyle pills -of doc/_www2 doc ','build & generate doc folder,change tabs style/position')]

def generator_cmdlines():    
  cmd_lines=cmdlines+cmd_init+cmd_build+cmd_generate+cmd_make  
  for cmd in cmd_lines:
    yield cmd
  
class CliTests(unittest.TestCase):  #CmdDocBuilder
  """ Test pimouss command line interface """
  def setUp(self):
    pass
    
  def test_doc(self):
    docpath='doc'
    if not os.path.exists(docpath):
      os.makedirs(docpath)  
    for filename,cmd,description in generator_cmdlines():
      with open(os.path.join(docpath,filename),'a') as log: #as option?
        print 'exec: %s' %cmd
        log.write('## Command\n')
        log.write('- - -\n\n')
        log.write('        %s\n' %cmd)
        log.write('\n')
        if description !='':
          log.write('### Description\n\n')
          log.write('        %s\n' %description)
          log.write('\n')
        log.write('### Output\n\n')
        args=shlex.split(cmd)
        output,error = subprocess.Popen(args,stdout = subprocess.PIPE, stderr= subprocess.PIPE).communicate()
        for line in StringIO.StringIO(error).readlines():
          log.write('        %s  \n' %line.rstrip())
        for line in StringIO.StringIO(output).readlines():
          log.write('        %s  \n' %line.rstrip())
        log.write('\n\n')  
    
  def tearDown(self):
    error=subprocess.call('python pimouss/pimouss.py make -of doc/_html/ doc',shell=True)
    self.assertEqual(error,0)
  
def generate_data(folder,datas):
  if not os.path.exists(folder):
    try:
      print 'mkdir %s' %folder
      os.makedirs(folder)
    except:
      print 'failed to create %s' %folder
      pass  
  for md_filename in datas.keys():
    if md_filename!='static':
      print 'generate %s' %(md_filename)
      f=codecs.open(os.path.abspath(os.path.join(folder,md_filename)),'w','utf-8')
      f.write(datas[md_filename])
      f.close()
    else:
      for static_file in datas['static']:
        src=os.path.join(folder,md_filename)
        dest=os.path.relpath(src,static_file)
        print '%s -> %s' %(src,dest)
        #os.copy(src,dest)

def build(inpath,outpath=None): #class test
  print 'pimoussify (as python module) %s' %(inpath)
  from pimouss.pimouss import Pimouss
  pims=Pimouss()
  pims.process(inpath,outpath=outpath)

class ModuleTests(unittest.TestCase):  
  """ Test both pimouss as a module/class """
  def setUp(self):
    #generate data
    self.inpath=[]
    self.path_foto=os.path.join('example','foto')
    self.inpath.append(self.path_foto)
    from tests.example_foto  import datas as fotos
    generate_data(self.path_foto,fotos)
    
    self.path_website=os.path.join('example','website')
    self.inpath.append(self.path_website)
    from tests.example_website  import datas as webs
    generate_data(self.path_website,webs)
    
  def test_example(self):
    for path in self.inpath:
      build(path,os.path.join(path,'_www'))
    build(self.path_foto,os.path.join('doc','_html','example_foto'))
    build(self.path_website,os.path.join('doc','_html','example_website'))
    
  def tearDown(self):
    """ write doc """
    doc=open(os.path.join('doc','example.md'),'w')
    doc.write('Example  \n')
    doc.close()
    doc=open(os.path.join('doc','example.foto.md'),'w')
    doc.write('### markdown file list  \n- - -  \n')
    for f in os.listdir(self.path_foto):
      if os.path.isfile(os.path.join(self.path_foto,f)):
        if os.path.splitext(f)[1]=='.md':
          doc.write('* file:%s  \n\n' %os.path.join(self.path_foto,f))
          lines=open(os.path.join(self.path_foto,f),'r').readlines()
          for line in lines:
            doc.write('        %s  \n' %line.rstrip())
          doc.write('\n')  
    doc.close()
    doc=open(os.path.join('doc','example.website.md'),'w')
    doc.write('### markdown file list  \n- - -  \n')
    #path=self.path_website
    #self._writedoc(path)
    for f in os.listdir(self.path_website):
      if os.path.isfile(os.path.join(self.path_website,f)):
        if os.path.splitext(f)[1]=='.md':
          doc.write('* file:%s  \n\n' %os.path.join(self.path_website,f))
          lines=open(os.path.join(self.path_website,f),'r').readlines()
          for line in lines:
            doc.write('        %s  \n' %line.rstrip())
          doc.write('\n')
    doc.close()
    
class InstallTests(unittest.TestCase):  
  """ install tests """
  def test_build(self):
    """ install tests  """  
    #must be run as sudo...
    error=subprocess.call('python setup.py install',shell=True)
    self.assertEqual(error,0)
     
class BuildTests(unittest.TestCase):  
  """ build tests """
  def test_install(self):
    """ build tests  """
    cmd=['python setup.py sdist']
        #'python setup.py check',
        #'python setup.py clean']    
    error=0
    for item in cmd:    
      error+=subprocess.call(shlex.split(item))
    #self.assertEqual(error,0)
    if sys.platform == 'win32':
      self.build_win()
  
  def build_win(self):
    errors=subprocess.call(shlex.split('python setup.py py2exe'))
    #errors+=subprocess.call('python setup.py bdist win32',shell=True)
    self.assertEqual(errors,0)

def suite():
  suite = unittest.TestLoader().loadTestsFromTestCase(BuildTests)
  #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(InstallTests))
  suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ModuleTests))
  suite.addTest(unittest.TestLoader().loadTestsFromTestCase(CliTests))
  return suite
  
def clean():
  import shutil
  build=os.path.join('build')
  if os.path.exists(build):
    print 'remove build folder...'
    shutil.rmtree(build)
  example=os.path.join('example')
  if os.path.exists(example):
    print 'remove example folder...'
    shutil.rmtree(example)
  #doc=os.path.join('doc')
  #if os.path.exists(doc):
  #  print 'remove doc folder...'
  #  shutil.rmtree(doc)

def run():
  tests=suite()
  res=unittest.TextTestRunner(verbosity = 2).run(tests)
  return res
  
if __name__ == '__main__':
  old=os.getcwd()
  os.chdir(os.path.dirname(os.path.abspath(__file__))) 
  clean()
  res=run()
  os.chdir(old)
  sys.exit(len(res.errors)+len(res.failures))
  
  
