#!/usr/bin/env python
# -*- coding: utf-8 -*-

__description__=""" mini file-based static website/html pages generator """

__version__='0.1.0-beta'

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
logging.basicConfig(level=logging.WARNING,format='%(asctime)s::%(levelname)s::%(name)s::%(message)s')
logger=logger=logging.getLogger('pimouss')


import external.markdown2 as markdown2

#very basic one file approch template
tpl_page='''.
<!DOCTYPE html>
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
      logger.debug('generate_page()::using user defined article template : %s' %(res[0]+'.tpl'))
      article_tpl=open(os.path.basename(article)+'.tpl','r').read()
    else:
      logger.debug('generate_page()::No template for article, using default')
      article_tpl=tpl_article
    logger.debug('generate_page()::markdown process on article: %s',os.path.basename(article))        
    html_article=md2html(article_tpl,article)
    if len(articles)>1:  
      if len(res)==2 and res[0] == pagename:
        logger.debug('generate_page()::adding html for %s' %(os.path.basename(article)))      
        html+=html_article
      else:
        tabs.append(html_article)
        tabsnames.append(res[1])
    idx+=1  
  if len(articles)>1:
    if style=='raw':
      logger.debug('generate_page using raw style')      
      for article in tabs:
        html+=article  
    else:
      if style!=None:
        logger.warning('Unknown style : %s. Processing default tabbed style' %style)
      logger.debug('generate_page() :: making tabs : %s' %(tabsnames))   
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
  content=''
  s = string.Template(template)  
  try:
    content=markdown2.markdown_path(filepath)
  except:
    logger.warning('md2html()::markdown convertion failed... Trying safe mode ')
    try:
      content=markdown2.markdown_path(filepath,safe_mode=True)
    except:
      logger.error('md2html()::markdown convertion failed for %s. Use raw text.' %filepath)
      import codecs
      try:
        content=codecs.open(filepath,'r','utf-8').read()
      except:
        logger.error('invalid file %s ' %filepath)
  #  print 'error processing markdown. Read raw file...'  
  html=''
  try:
    html=s.substitute(content=content)
  except:
    logger.warning('md2html()::string.Template substitute failed... Trying safe mode ')
    try:
      html=s.safe_substitute(content=content)    
    except:
      logger.error('md2html()::string.Template conversion failed for : %s ' %filepath)
      
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
      #print  self.builder
      #print  self.generator         
  
  def scan_plugin(self):
    """ return a list of available plugin  """
    pluginpath=_module_path()
    plugins=[]
    for f in os.listdir(pluginpath):
      if os.path.isfile(os.path.join(pluginpath,f)) and os.path.splitext(os.path.join(pluginpath,f))[-1]=='.py' :
        if 'plugin_' in os.path.basename(f):
          logger.debug("Pimouss :: found plugin : %s",f)
          plugins.append(f)
    return plugins    
    
  def build(self,srcpath,buildpath=None):
    logger.info('Pimouss :: build %s' %srcpath)                  
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
    logger.info('Pimouss :: generate %s ' %outpath)
    if outpath==None:
      buildpath=outpath
    self.generator.process(buildpath,outpath)
    
  def process(self,inpath,buildpath=None,outpath=None):
    logger.info('Pimouss :: process %s' %inpath)
    if buildpath==None:
      buildpath=inpath
    if outpath==None:
      outpath=inpath                  
    self.build(inpath,buildpath)      
    self.generate(buildpath,outpath)
    self.cp_static_files(inpath,outpath)
    
      
  def cp_static_files(self,inpath,outpath): #inpath not needed... use copyfiles !
    """ search for a 'static' folder and copy tree to output """ 
    logger.debug('Pimouss :: cpStaticFiles')
    for folder in os.listdir(inpath):
      if folder == 'static':
        logger.info('Pimouss :: cpStaticFiles :: found static folder, copy all...')
        if os.path.exists(os.path.join(outpath,folder)):
          logger.warning('Remove old static folder')
          shutil.rmtree(os.path.join(outpath,folder)) #not efficient. Should do it incrementaly...
        copyfiles(os.path.join(inpath,folder),os.path.join(outpath,folder))

    
    
def copyfiles(src,dst):
    logger.warning('Pimouss :: copyfiles from %s to %s' %(src,dst))
    try:
      shutil.copytree(src, dst)
    except:
      logger.warning("Error copying files...")

    '''try:
      shutil.copytree(src, dst)
    except OSError as exc:
      if exc.errno == errno.ENOTDIR:
        logger.warning("Folder %s already exists. Skipping..." % src)
        shutil.copy(src, dst)
        #copyfiles(src, dst)
        pass        
      elif exc.errno == errno.EEXIST:
        logger.warning("File %s already exists. Skipping..." % src)
        pass
      else: raise'''


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
    #print glob.glob(os.path.join(path,'*.*'))
    for item in glob.glob(os.path.join(path,'*.*')):
      if string.split(os.path.basename(item),'.')[-1] in self.ext_lst:
        files.append(item)
    logger.debug('Pimouss :: Builder :: parseByNames:: files for %s : %s' %(path,files))
    res = None
    pagelist=[]
    articledict={}
    for item in files:
      res=os.path.basename(item).split()
      res=string.split(os.path.basename(item),'.')
      #print 'Builder :: parseByNames:: res : %s' %res      
      if res[0] not in pagelist:
        logger.debug('Pimouss :: Builder :: parseByNames :: add page : %s' %res[0])      
        pagelist.append(res[0])
        articledict[res[0]]=[] #or add itself?
      articledict[res[0]].append(item)    
    if len(pagelist)>0:
      self.pages['pagelist'] = pagelist
      for page in pagelist:      
        logger.debug('Pimouss :: Builder :: parseByNames :: pages= %s ' %page)
        logger.debug('Pimouss :: Builder :: parseByNames :: articles= %s ' %articledict[page])      
        self.pages[page]=articledict[page] 
    #look for templates/layout... To ENHANCE...
    self.pages['template']=glob.glob(os.path.join(path,'*.tpl'))              
    global_tpl=None
    if os.path.isfile(os.path.join(path,'layout.tpl')):
      logger.debug('Builder :: parseByNames :: Find general layout file : %s' %'layout.tpl')
      self.pages['layout']=os.path.join(path,'layout.tpl')
      self.layout=os.path.join(path,'layout.tpl')
    else:
      # it will write default template...
      self.pages['layout']=global_tpl
    
  #def parseFolder(self,path):
  #  logger.debug('Builder :: parseFolder :: %s' %path)
  #  self.parseByNames(path)
  
  #def process(self,scan_path,output_path)
        
  def scan(self,path): #should have a build path...
    """ Scan directory and output a dict   """
    #_build
    #if 
    if os.path.exists(path):
      self.path=path
      logger.debug('Builder :: scan :: %s' %self.path)
      self.parseByNames(path)    
      #for item in os.listdir(self.path):
      #  if os.path.isdir(os.path.join(self.path,item)):
      #    logger.info('Builder :: scan :: found folder : %s' %item)
      #    self.parseFolder(os.path.join(self.path,item))
        #else: 
          #print 'found file : %s' %os.path.basename(path)      
          #pass
    else:
      logger.error('Builder :: scan :: path does not exist : %s' %path)
    return self.pages  
  
  def write(self,srcpath,buildpath):
    self.outfolder=buildpath
    if not os.path.exists(self.outfolder):
      os.makedirs(self.outfolder)  
    if buildpath != srcpath:  
      logger.debug('Builder :: write content files into :: %s' %self.outfolder)
      for page in self.pages['pagelist']:
        for item in self.pages[page]:
          try:
            shutil.copy(item,os.path.join(self.outfolder,os.path.basename(item))) 
          except:
            logger.warning('cannot copy %s to %s' %(item,os.path.join(self.outfolder,os.path.basename(item))))    
          if self.layout == None:
            open(os.path.join(self.outfolder,'layout.tpl'),'w').write(tpl_page)  
          else:
            if not os.path.exists(os.path.join(self.outfolder,'layout.tpl')):
              shutil.copy(self.layout,os.path.join(self.outfolder,'layout.tpl'))   #use basename? 
      cfg=os.path.basename(self.path)+'.pims'
    else:
      cfg='.pims'
    logger.debug('Builder :: write content files into :: %s' %self.outfolder)
    open(cfg,'w').write(str(self.pages))    #self.cfg.write()
      
    '''  
    if len(self.pages['template'])== 0:
      logger.debug('Builder :: write :: no template found use default one...')
    elif len(self.pages['template'])== 1:
      logger.debug('Builder :: write :: single template found : %s' %self.pages['template'][0])
    else:
      logger.debug('Builder :: write :: more than one tamplate found : %s' %self.pages['template'])'''

  
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
    #print self.pages
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
        logger.debug('Pimouss :: chckpages :: undefined keys: %s' %key)
    return result
    
  def process(self,path,outpath=None,pagelist=None): #outname...
    # read md/html, and process it!
    if pagelist==None:
      self.scan(path) #get config...
    if outpath == None:
      logger.warning('Pimouss :: Generator :: no output folder specified, using "_www" folder')          
      self.outpath=os.path.join(path,'_www')
    else:
      self.outpath=outpath
    if not os.path.exists(self.outpath):
      logger.info('Pimouss :: Generator :: creating : %s' %(self.outpath))      
      os.makedirs(self.outpath)
    if self.chckpages()== False:
      logger.error('Pimouss :: process :: chckpages error')
      return
    if self.pages['pagelist']==None:
      logger.error('Pimouss :: process :: self.pages[%s]==None' %('pagelist'))
      return 2
    for page in self.pages['pagelist']:
      logger.info('Pimouss ::  Generator ::  writing %s' %(page+'.html') )
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
class iCmd(cmd.Cmd):
  """Simple interactive command processor"""  
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

class PimoussThread(threading.Thread): 
  """ launch Pimouss for a folder in a thread """  
  def __init__(self,folder_path): #add optons
    threading.Thread.__init__(self)
    self.folder_path=folder_path
    
  def run(self):
    Pimouss()
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
    pimouss.Builder.__init__(self)

#overide Generator class if needed
class Generator(iglou.Generator):
  def __init__(self):
    pimouss.Generator.__init__(self)   
'''

# command line interface
def _init(args):
  if not os.path.exists(args.inpath):
    logging.error('input path does not exist... Aborting.')
    return 1  
  if not os.path.isdir(args.inpath):  
    logging.error('input path is not a folder... Aborting.')
    return 1
  error=0
  pims=Pimouss(plugin=args.plugin)    
  #pims.init()    
  #if args.recursive == True:
  #  tmp_build_path=os.path.join(build_path,'_tmp')
  #  for dirpath, dirnames, filenames in os.walk(args.input_path):
  #    pimouss.build(dirpath,buildpath=tmp_build_path)
  #  pimouss.generate(tmp_build_path,outpath=generate_path) #remove tmp file?
  #else:
  #  pimouss.process(args.input_path,buildpath=build_path,outpath=generate_path)   
  return error

def _build(args):
  if not os.path.exists(args.inpath):
    logging.error('input path does not exist... Aborting.')
    return 1  
  if not os.path.isdir(args.inpath):  
    logging.error('input path is not a folder... Aborting.')
    return 1
  error=0
  pims=Pimouss(plugin=args.plugin)    
  pims.build(args.inpath,buildpath=args.output_path)
  return error

def _generate(args):
  if not os.path.exists(args.inpath):
    logging.error('input path does not exist... Aborting.')
    return 1  
  if not os.path.isdir(args.inpath):  
    logging.error('input path is not a folder... Aborting.')
    return 1
  error=0
  pims=Pimouss(plugin=args.plugin)    
  pims.generate(args.inpath,outpath=args.output_path) 
  return error

def _make(args):
  if not os.path.exists(args.inpath):
    logging.error('input path does not exist... Aborting.')
    return 1  
  if not os.path.isdir(args.inpath):  
    logging.error('input path is not a folder... Aborting.')
    return 1
  error=0
  pims=Pimouss(plugin=args.plugin)    
  pims.process(args.inpath,outpath=args.output_path)   
  return error

def _gui(args):
  error=0
  try:
    import pimouss
    pimouss.gui.main()
  except:
    try:
      logger.warning('can not find pimouss.gui')
      import gui
      gui.main()
    except:  
      logger.warning('neither gui')
      error=-1
  return error

def cli():
  try:
    import argparse
  except:  
    import external.argparse as argparse
    
  pims=Pimouss()
  plugins=pims.scan_plugin()#static method?
    
  parser=argparse.ArgumentParser(version='%s' %__version__ ,
                                   description='%s' %__description__,
                                   epilog=' by %s' %(__author__))
  paser_log=parser.add_mutually_exclusive_group()
  paser_log.add_argument("-d", "--debug",action='store_true',default=False,
                   help="verbose output logging")
  paser_log.add_argument("-q", "--quiet",action='store_true',default=False,
                   help="limit output logging to warning/error")
  
  subparsers = parser.add_subparsers(title="Available commands")

  parser_gui=subparsers.add_parser("gui",help="launch Qt (PySide) desktop interface.")  
  parser_gui.set_defaults(func=_gui)
  
  parser_init=subparsers.add_parser("init",help="init a pimouss project (write layout and static files)")  
  parser_init.set_defaults(func=_init)
  
  parent_subparser = argparse.ArgumentParser(add_help=False)  
  parent_subparser.add_argument("-tpl", "--layout_template",type=str,default=None,
                   help="layout template file to use")
  parent_subparser.add_argument("-s","--static_assets",type=str,default='static', # use pimouss.cfg
                   help="path of assets/static files")
  parent_subparser.add_argument("-of","--output_path",type=str,default='_html',#required=True,
                           help="output folder path (default to _html)")
  
  parent_subparser.add_argument("--tabstyle",choices=('pills','pills-right'),default=None,
                   help="layout template file to use") #only for generate?
  
  #parent_subparser.add_argument("--navstyle",choice=('static','static-invert'),default=None,
  #                 help="navigation bar style") #only for generate?
  #parent_subparser.add_argument("-p", "--plugin",choices=plugins,default=False,
  #                        help="plugin to use.")

  parser_build = subparsers.add_parser("build",parents=[parent_subparser],
                                     help="path -> markdown")
  parser_build.add_argument("-p", "--plugin",choices=plugins,default=None,
                          help="plugin to use.")
  parser_build.set_defaults(func=_build)
  
  parser_generate = subparsers.add_parser("generate",parents=[parent_subparser],
                                     help="markdown -> html")
  parser_generate.add_argument("-p", "--plugin",choices=plugins,default=None,
                          help="plugin to use.")
  parser_generate.set_defaults(func=_generate)
  
  parser_make = subparsers.add_parser("make",parents=[parent_subparser],
                                     help="path -> html")
  parser_make.add_argument("-p", "--plugin",choices=plugins,default=None,
                          help="plugin to use.")
  parser_make.set_defaults(func=_make) 
  # add auto mode?

  #parser_execute=subparsers.add_parser("execute",#parents=[parent_subparser],#parent parser??
  #                                   help="Execute command contains in INFILE (one cmd per line)")
  #parser_execute.set_defaults(func=_exec_from_file) 
  
  parser.add_argument("inpath",type=str,default='.',help="input path")
  #parser.add_argument("---inpath",type=str,default='.',help="input path")
  args=parser.parse_args()
  import datetime
  start=datetime.datetime.now()
  FORMAT='  %(message)s  \n'
  if args.quiet:
    logger.setLevel(logging.WARNING)
  if args.debug:
    logger.setLevel(logging.DEBUG)
  error=args.func(args)
  elapsed=datetime.datetime.now()-start    
  logger.info('elapsed time : %s' %elapsed)
  return error

if __name__ == '__main__':
  cli()  

    
