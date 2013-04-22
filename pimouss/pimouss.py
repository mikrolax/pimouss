#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" mini file based static website/html pages generator """
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

import os
import glob
import string
import shutil
import errno
import sys

import logging
#logging.basicConfig(level=logging.INFO)
#__debug_level__=DEBUG
#logging.basicConfig(level=logging.getattr(__debug_level__))

import threading
from external import markdown2

#very basic one file approch template
tpl_page='''
  <html>
    <head>
      <title>  </title>
      <link href="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.2.1/css/bootstrap-combined.min.css" rel="stylesheet">
    </head>    
    <body>
     <div class="container"> 
      $content

      <!-- 
      <hr>
      <p>&copy; sebastien stang - 2013</p> 
      -->
            
     </div>
      <script src="http://code.jquery.com/jquery-1.8.2.min.js"></script>
      <script src="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.2.1/js/bootstrap.min.js"></script>
    </body>
  </html>
'''

tpl_article='''
  $content
'''

def make_tabs(snippet,names): #list of HTML snippet... Should add options...
  tpl='''<div class="tabbable tabs-left"> 
            <ul class="nav nav-tabs"> 
            $links
            </ul>
          
            <div class="tab-content">
            $tabs
            </div>
          </div>
  '''
  links=''' '''
  tabs=''' '''
  i=0
  for item in snippet:
    if i==0:
      links+='''<li class="active"><a href="#tab%s" data-toggle="tab">%s</a></li>''' %(str(i),names[i].capitalize())  #add title... 
      tabs+='''<div class="tab-pane active" id="tab%s"> %s </div>''' %(str(i),item.encode('utf-8'))
    else:
      links+='''<li><a href="#tab%s" data-toggle="tab">%s</a></li>''' %(str(i),names[i].capitalize())  #add title...
      tabs+='''<div class="tab-pane" id="tab%s"> %s </div>''' %(str(i),item.encode('utf-8'))
    i+=1
  template=string.Template(tpl)  
  html=template.substitute(links=links,tabs=tabs)
  return html
  
def _we_are_frozen():
  return hasattr(sys, "frozen")

def _module_path():
  if _we_are_frozen():
    return os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding( )))
  else:
    return os.path.dirname(os.path.abspath(__file__))
    

def generate_page(template,articles,pagename='',title=None,style=None): # don't use title now...
  if title == None:
    title='Pimouss'
  html=''' '''
  tabs=[]
  tabsnames=[]
  idx=0
  for article in articles: #for article_name,
    res=string.split(os.path.basename(article),'.')
    html_article=''' '''
    if os.path.exists(article+'.tpl'):
      logging.info('generate_page() :: using user defined article template : %s' %(res[0]+'.tpl'))
      article_tpl=open(os.path.basename(article)+'.tpl','r').read()
    else:
      logging.debug('generate_page():: No template for article, using default')
      article_tpl=tpl_article
    logging.debug('generate_page():: markdown process on article: %s',os.path.basename(article))        
    html_article=md2html(article_tpl,article)

    if len(articles)>1:  
      if len(res)==2 and res[0] == pagename:
        logging.info('generate_page() :: adding common html for page : %s' %(os.path.basename(article)))      
        html+=html_article
      else:
        tabs.append(html_article)
        tabsnames.append(res[1])
    idx+=1  

  if len(articles)>1:
    if style=='raw':
      logging.info('generate_page using raw style')      
      for article in tabs:
        html+=article  
    else:
      if style!=None:
        logging.warning('Unknown style : %s. Processing default tabbed style' %style)
      logging.debug('generate_page() :: making tabs : %s' %(tabsnames))   
      tmp=make_tabs(tabs,tabsnames)
      html+=tmp.decode('utf-8')
  else:    
    html+=html_article #.encode('utf-8') 

  page=string.Template(template) 
  #html_page=page.substitute(title=title,content=html.encode('utf-8'))
  html_page=page.substitute(content=html.encode('utf-8'))
  return html_page
  
  
  
def md2html(template,filepath):
  """  write html snippet based on template and file """
  #look if filepath is a list or not?
  s = string.Template(template)  
  #try:
  content=markdown2.markdown_path(filepath)#safe_mode=True
  #except:
  #  print 'error processing markdown. Read raw file...'  
  #  content=open(filepath,'r').read()
  try:
    html=s.substitute(content=content)
  except:
    logging.warning('string.Template substitute failed... Trying safe mode ')
    html=s.safe_substitute(content=content)    
  return html

'''
def plugin_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod
'''

class Pimouss(object):
  def __init__(self,plugin=None):
    #logging.basicConfig(level=logging.INFO)
    self.builder=None
    self.generator=None
    default_template=os.path.join(_module_path(),'layout.tpl')
    if not os.path.exists(default_template):
      #logging.warning('Pimouss :: No default template exist, will use internal one.')
      self.layout=None
    else:  
      self.layout=default_template   
    self.pages={}
    
    if plugin==None:
      self.builder=Builder()
      self.generator=Generator()      
    else:
      #modulename='pimouss.plugin_'+plugin
      modulename='plugin_'+plugin

      module = __import__(modulename,fromlist=['Builder','Generator'])
      class_ = getattr(module, 'Builder')
      self.builder=class_()
      class_ = getattr(module, 'Generator')
      self.generator=class_()
      
      self.builder.layout=self.layout
      self.generator.layout=self.layout
      print  self.builder
      print  self.generator         
  
  def scan_plugin(self):
    """ return a list of available plugin  """
    pluginpath=_module_path()
    plugins=[]
    for f in os.listdir(pluginpath):
      if os.path.isfile(os.path.join(pluginpath,f)) and os.path.splitext(os.path.join(pluginpath,f))[-1]=='.py' :
        if 'plugin_' in os.path.basename(f):
          logging.debug("Pimouss :: found plugin : %s",f)
          plugins.append(f)
    return plugins    
    
  def build(self,srcpath,buildpath=None):
    logging.info('Pimouss :: build %s' %srcpath)                  
    self.pages=self.builder.scan(srcpath)
    if buildpath==None:
      buildpath=srcpath 
    self.builder.write(srcpath,buildpath)
    #if buildpath!=None:
    #  self.builder.write(srcpath,buildpath)
    #else:
    #  pass
    #self.write_config()
    #return self.pages['pagelist']

  def generate(self,buildpath,outpath=None):
    logging.info('Pimouss :: generate %s ' %outpath)
    if outpath==None:
      buildpath=outpath
    self.generator.process(buildpath,outpath)
    
  def process(self,inpath,buildpath=None,outpath=None):
    logging.info('Pimouss :: process %s' %inpath)
    if buildpath==None:
      buildpath=inpath
    if outpath==None:
      outpath=inpath                  
    self.build(inpath,buildpath)      
    self.generate(buildpath,outpath)
    self.cp_static_files(inpath,outpath)
    
      
  def cp_static_files(self,inpath,outpath): #inpath not needed... use copyfiles !
    """ search for a 'static' folder and copy tree to output """ 
    logging.debug('Pimouss :: cpStaticFiles')
    for folder in os.listdir(inpath):
      if folder == 'static':
        logging.info('Pimouss :: cpStaticFiles :: found static folder, copy all...')
        copyfiles(os.path.join(inpath,folder),os.path.join(outpath,folder))

    
    
def copyfiles(src,dst):
    logging.debug('Pimouss :: copyfiles')
    try:
      shutil.copytree(src, dst)
    except OSError as exc:
      if exc.errno == errno.ENOTDIR:
        print("Folder %s already exists. Skipping..." % src)
        shutil.copy(src, dst)
        #copyfiles(src, dst)
      elif exc.errno == errno.EEXIST:
        print("File %s already exists. Skipping..." % src)
        pass
      else: raise


class Builder(object): 
  """  File based generic mardown/txt/HTML content parser. Only One level deep   """
  def __init__(self):
    self.path=None     # add template?
    self.ext_lst=['txt','md','html']
    self.excludes=['static','js','img','css']
    self.outfolder=None   #we will use a '_build' folder
    self.layout=None
    #init to be sure it's well-formatted
    self.pages={}
    self.pages['pagelist']=[]
    #self.cfg=Config()
    
    
  def parseByNames(self,path):
    files=[]
    print glob.glob(os.path.join(path,'*.*'))
    for item in glob.glob(os.path.join(path,'*.*')):
      if string.split(os.path.basename(item),'.')[-1] in self.ext_lst:
        files.append(item)
    logging.debug('Pimouss :: Builder :: parseByNames:: files for %s : %s' %(path,files))
    res = None
    pagelist=[]
    articledict={}
    for item in files:
      res=os.path.basename(item).split()
      res=string.split(os.path.basename(item),'.')
      #print 'Builder :: parseByNames:: res : %s' %res      
      if res[0] not in pagelist:
        logging.info('Pimouss :: Builder :: parseByNames :: add page : %s' %res[0])      
        pagelist.append(res[0])
        articledict[res[0]]=[] #or add itself?
      articledict[res[0]].append(item)    
    if len(pagelist)>0:
      self.pages['pagelist'] = pagelist
      for page in pagelist:      
        logging.debug('Pimouss :: Builder :: parseByNames :: pages= %s ' %page)
        logging.debug('Pimouss :: Builder :: parseByNames :: articles= %s ' %articledict[page])      
        self.pages[page]=articledict[page] 
    #look for templates/layout... To ENHANCE...
    self.pages['template']=glob.glob(os.path.join(path,'*.tpl'))              
    global_tpl=None
    if os.path.isfile(os.path.join(path,'layout.tpl')):
      logging.info('Builder :: parseByNames :: Find general layout file : %s' %'layout.tpl')
      self.pages['layout']=os.path.join(path,'layout.tpl')
      self.layout=os.path.join(path,'layout.tpl')
    else:
      # it will write default template...
      self.pages['layout']=global_tpl
    
  #def parseFolder(self,path):
  #  logging.info('Builder :: parseFolder :: %s' %path)
  #  self.parseByNames(path)
  
  #def process(self,scan_path,output_path)
        
  def scan(self,path): #should have a build path...
    """ Scan directory and output a dict   """
    #_build
    #if 
    if os.path.exists(path):
      self.path=path
      logging.info('Builder :: scan :: %s' %self.path)
      self.parseByNames(path)    
      #for item in os.listdir(self.path):
      #  if os.path.isdir(os.path.join(self.path,item)):
      #    logging.info('Builder :: scan :: found folder : %s' %item)
      #    self.parseFolder(os.path.join(self.path,item))
        #else: 
          #print 'found file : %s' %os.path.basename(path)      
          #pass
    else:
      logging.error('Builder :: scan :: path does not exist : %s' %path)
    return self.pages
  
  
  
  def write(self,srcpath,buildpath):
    self.outfolder=buildpath
    if not os.path.exists(self.outfolder):
      os.makedirs(self.outfolder)  
    if buildpath != srcpath:  
      logging.info('Builder :: write content files into :: %s' %self.outfolder)
      for page in self.pages['pagelist']:
        for item in self.pages[page]:
          try:
            shutil.copy(item,os.path.join(self.outfolder,os.path.basename(item))) 
          except:
            logging.warning('cannot copy %s to %s' %(item,os.path.join(self.outfolder,os.path.basename(item))))    
          if self.layout == None:
            open(os.path.join(self.outfolder,'layout.tpl'),'w').write(tpl_page)  
          else:
            if not os.path.exists(os.path.join(self.outfolder,'layout.tpl')):
              shutil.copy(self.layout,os.path.join(self.outfolder,'layout.tpl'))   #use basename? 
      cfg=os.path.basename(self.path)+'.pimouss'
    else:
      cfg='.pimouss'
    logging.info('Builder :: write content files into :: %s' %self.outfolder)
    open(cfg,'w').write(str(self.pages))    #self.cfg.write()
      
    '''  
    if len(self.pages['template'])== 0:
      logging.debug('Builder :: write :: no template found use default one...')
    elif len(self.pages['template'])== 1:
      logging.debug('Builder :: write :: single template found : %s' %self.pages['template'][0])
    else:
      logging.debug('Builder :: write :: more than one tamplate found : %s' %self.pages['template'])'''




  
class Generator(object):
  """ generate HTML """
  def __init__(self): # or scan?
    self.outpath=None
    self.pages={}
    self.layout=None
    self.style=None #or blog
    #self.cfg=Config()            # add file!!
    
  def scan(self,path): #read_config(self,config_filepath)
    self.pages=Builder().scan(path) #no!
    print self.pages
    self.layout=self.pages['layout']

  def chckpages(self):
    """ Check minimal keys... """
    #defindedPagesKeys=Pages().keys() #TBD
    result=False
    minimalPagesKeys=['pagelist']
    for key in self.pages.keys():
      if key in minimalPagesKeys:
        result=True
      if key not in minimalPagesKeys:
        logging.warning('Pimouss :: chckpages :: undefined keys: %s' %key)
    return result
    
  def process(self,path,outpath=None,pagelist=None): #outname...
    # read md/html, and process it!
    if pagelist==None:
      self.scan(path) #get config...
    if outpath == None:
      logging.info('Pimouss :: Generator :: no output folder specified, using "_www" folder')          
      self.outpath=os.path.join(path,'_www')
    else:
      self.outpath=outpath
    if not os.path.exists(self.outpath):
      logging.info('Pimouss :: Generator :: creating : %s' %(self.outpath))      
      os.makedirs(self.outpath)
    if self.chckpages()== False:
      logging.error('Pimouss :: process :: chckpages error')
      return
    if self.pages['pagelist']==None:
      logging.error('Pimouss :: process :: self.pages[%s]==None' %('pagelist'))
      return 2
    for page in self.pages['pagelist']:
      logging.info('Pimouss ::  Generator ::  writing %s' %(page+'.html') )
      if self.layout != None:
        page_tpl=open(self.layout).read()
      else:
        #else if 
        page_tpl=tpl_page
      #html_page=generate_page(page_tpl,self.pages[page],pagename=page,title=page,style=self.style) 
      html_page=generate_page(page_tpl,self.pages[page],pagename=page,title=None,style=self.style)
      with open(os.path.join(self.outpath,page+'.html'),'w') as f:
        f.write(html_page)
    copyfiles(path,self.outpath)

'''
class PimouShell(cmd.Cmd):
  """Simple command processor"""  
  def __init__(self):
    cmd.Cmd.__init__(self)
    self.prompt = 'pimouss > '
    self.intro = 'Simple command processor for pimouss!\n
                    Type help to see available command\n'
                      
  def emptyline(self):    
    """Do nothing on empty input line"""
    pass        
  
  def do_exit(self, args):
    """Exits from the console"""
    return -1

  def do_build(self,args):      
    pass

  def do_generate(self,args):      
    pass
'''

'''
def pimoussProcess():
  try:
    import multiprocessing
  except:
    raise  
'''


class PimoussThread(threading.Thread): 
  """ launch Pimouss for a folder in a thread """  
  def __init__(self,folder_path): #add optons
    threading.Thread.__init__(self)
    self.folder_path=folder_path
    
  def run(self):
    Pimouss()
    
    
    
def pimoussCli():
  try:
    import argparse
  except:
    import external.argparse  as argparse  
  parser = argparse.ArgumentParser(description='pimouss v.%s:  static website generator' %__version__,epilog='Copyright Sebastien Stang') #add version? 
  #parser.add_argument("-v", "--version",action='store_true',default=False,help="display current version")
  parser.add_argument("-i", "--interactive",type=bool,default=False,help="Simulate an interactive shell")
  parser.add_argument("-p", "--plugin",type=str,default=None,help="use plugin name")
  parser.add_argument("-r", "--recursive", action="store_true",help="recursively look for markdown file")
  parser.add_argument("-b", "--build_path",type=str,default=None,help="build path. Where it write config")
  parser.add_argument("-g", "--generate_path",type=str,default=None,help="generate path. Default to folder '_www' of input folder")
  parser.add_argument("input_path",type=str,default='',help="input folder (content).")
  args = parser.parse_args()
  
  if not os.path.exists(args.input_path):
    print 'input path does not exist... Aborting.'
    return 1
  
  if not os.path.isdir(args.input_path):  
    print 'input path is not a folder... Aborting.'
    return 1
  
    
  pimouss=Pimouss()
  print ''
  print '    Pimouss v.%s' %__version__
  print ''
  print '  Available plugin : '
  for plugin in pimouss.scan_plugin():
    print '    - %s  ' %plugin 
  print ''
  print '  Processing folder : %s' %args.input_path
  print '   - build_path : %s' %args.build_path  
  print '   - generate_path : %s' %args.generate_path
  #print '*   - plugin : %s' %args.plugin
  print ''
  if args.build_path!=None:
    build_path=args.build_path
  else:
    build_path=args.input_path
  if args.generate_path!=None:
    generate_path=args.generate_path
  else:
    generate_path=os.path.join(args.input_path,'_html')
  if args.plugin!=None:
    plugin=args.plugin
  else:
    plugin=None

  pimouss=Pimouss(plugin=plugin)    
  if args.recursive == True:
    tmp_build_path=os.path.join(build_path,'_tmp')
    for dirpath, dirnames, filenames in os.walk(args.input_path):
      pimouss.build(dirpath,buildpath=tmp_build_path)
    pimouss.generate(tmp_build_path,outpath=generate_path) #remove tmp file?
  else:
    pimouss.process(args.input_path,buildpath=build_path,outpath=generate_path) 
  
  
'''  
def test():    
  import shlex
  for item in os.listdir():
    args='python pimouss item'
    subprocess.call(shlex(args))
'''

#to avoid create new plugin from scratch ??
default_plugin='''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pimouss
import os

#overide Builder class if needed
class Builder(iglou.Builder):
  def __init__(self):
    iglou.Builder.__init__(self)

#overide Generator class if needed
class Generator(iglou.Generator):
  def __init__(self):
    iglou.Generator.__init__(self)   
'''

'''
def createPlugin(plugin_name):
  with open() as fp: #use module path
    fp.write()
'''

if __name__ == '__main__':
  pimoussCli()  
    

    
