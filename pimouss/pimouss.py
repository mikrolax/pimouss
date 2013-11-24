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
logging.basicConfig(level=logging.INFO,format='%(asctime)s-%(levelname)s-%(name)s-  %(message)s')
logger=logging.getLogger('pimouss')

import external.markdown2 as markdown2

#very basic one file approch template
tpl_page='''.
<!DOCTYPE html>
  <html>
    <head>
      <title> $title </title>
      <link href="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.2.1/css/bootstrap-combined.min.css" rel="stylesheet">
    </head>    
    <body>
     <div class="container"> 
      $content
      <!-- <hr><p>&copy; sebastien stang - 2013</p> -->
     </div>
      <script src="http://code.jquery.com/jquery-1.8.2.min.js"></script>
      <script src="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.2.1/js/bootstrap.min.js"></script>
    </body>
  </html>
'''
tpl_article='''
  $content
'''

def _we_are_frozen():
  return hasattr(sys, "frozen")
def _module_path():
  if _we_are_frozen():
    return os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding( )))
  else:
    return os.path.dirname(os.path.abspath(__file__))

tab_styles=[('tabs','left'),('tabs','right'),
            ('pills','left'),('pills','right')]
            
def make_tabs(snippet,names,style='tabs',place='left'): 
  """  snippet/names : list of HTML snippet and associated names. style/place for tabs customisation """ 
  #tpl='''<div class="tabbable tabs-left">  
  #          <ul class="nav nav-tabs"> 
  tpl='''<div class="tabbable %s-%s">  
            <ul class="nav nav-%s"> 
            $links
            </ul>
          
            <div class="tab-content">
            $tabs
            </div>
          </div>''' %(style,place,style)
  links=''
  tabs=''
  i=0
  for item in snippet: #use enumerate
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
     
def generate_page(template,articles,pagename='',title='',style='tabs',place='left'):
  html=''' '''
  tabs=[]
  tabsnames=[]
  idx=0
  for article in articles:
    res=string.split(os.path.basename(article),'.')
    html_article=''' '''
    if os.path.exists(article+'.tpl'):
      logger.debug('generate_page:using user defined article template : %s' %(res[0]+'.tpl'))
      article_tpl=open(os.path.basename(article)+'.tpl','r').read()
    else:
      #logger.debug('generate_page: No specific template for article, using default')
      article_tpl=tpl_article
    logger.debug('generate_page: markdown process on article: %s',os.path.basename(article))        
    html_article=md2html(article_tpl,article)
    if len(articles)>1:  
      if len(res)==2 and res[0] == pagename:
        logger.debug('generate_page: adding html for %s' %(os.path.basename(article)))      
        html+=html_article
      else:
        tabs.append(html_article)
        tabsnames.append(res[1])
    idx+=1  
  if len(articles)>1:
    if style=='raw':
      logger.debug('generate_page: using raw style')      
      for article in tabs:
        html+=article  
    else:
      logger.debug('generate_page: making tabs (%s-%s): %s' %(tabsnames,style,place))   
      tmp=make_tabs(tabs,tabsnames,style=style,place=place)
      html+=tmp.decode('utf-8')
  else:    
    html+=html_article #.encode('utf-8') 
  page=string.Template(template) 
  html_page=page.substitute(title=title,content=html.encode('utf-8'))
  return html_page
  
def md2html(template,filepath):
  """  write html snippet based on template and file """
  content=''
  s = string.Template(template)  
  try:
    content=markdown2.markdown_path(filepath)
  except:
    logger.warning('md2html:markdown convertion failed... Trying safe mode ')
    try:
      content=markdown2.markdown_path(filepath,safe_mode=True)
    except:
      logger.error('md2html:markdown convertion failed for %s. Use raw text.' %filepath)
      import codecs
      try:
        content=codecs.open(filepath,'r','utf-8').read()
      except:
        logger.error('md2html:invalid file? %s ' %filepath)
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

default_template=os.path.join(_module_path(),'layout.tpl')
if not os.path.exists(default_template):
  logger.info('writing default layout: %s' %(default_template))
  open(default_template,'w').write(tpl_page)  

class Pimouss(object):
  def __init__(self,plugin=None,layout=None,static_dir=None): #static_dir=os.path.join(module_path(),'static')
    self.builder=None
    self.generator=None
    self.layout=layout
    self.static_dir=static_dir
    if self.layout==None:
      self.layout=os.path.join(_module_path(),'layout.tpl')  
    else:  
      if not os.path.exists(self.layout):
        logger.error('Pimouss :: invalid template: %s. Use default (%s)')#or create it?
        self.layout=os.path.join(_module_path(),'layout.tpl')          
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
  
  def scan_plugin(self):
    """ return a list of available plugin  """
    pluginpath=_module_path()
    plugins=[]
    for f in os.listdir(pluginpath):
      if os.path.isfile(os.path.join(pluginpath,f)) and os.path.splitext(os.path.join(pluginpath,f))[-1]=='.py' :
        if 'plugin_' in os.path.basename(f):
          logger.debug("found plugin : %s",f)
          plugins.append(f)
    return plugins    
    
  def build(self,srcpath,buildpath=None):
    if srcpath==None:
      logger.error('invalid source path %s' %buildpath)
      return -1
    if buildpath==None:
      buildpath=srcpath 
    logger.info('build %s -> %s' %(srcpath,buildpath))                  
    self.pages=self.builder.scan(srcpath)
    self.builder.write(srcpath,buildpath)
    #if self.static_dir:
    #  self.cp_static_files(self.static_dir,buildpath)

  def generate(self,buildpath,outpath=None,style=None,pos=None):
    if buildpath==None:
      logger.error('invalid buildpath %s' %buildpath)
      return -1
    if outpath==None:
      outpath=os.path.join(buildpath,'_html')
    logger.info('generate %s -> %s (layout: %s) ' %(buildpath,outpath,self.layout))
    if self.layout:
      self.generator.layout=self.layout  
    self.generator.process(buildpath,outpath,style=style,pos=pos)
    return 0
    
  def process(self,inpath,buildpath=None,outpath=None,style='tabs',pos=None):
    if inpath==None:
      logger.error('process: invalid inpath %s' %inpath)
      return -1
    if buildpath==None:
      buildpath=inpath
    if outpath==None:
      outpath=inpath                  
    logger.info('process %s -> %s -> %s' %(inpath,buildpath,outpath))
    self.build(inpath,buildpath)      
    self.generate(buildpath,outpath,style=style,pos=pos)
    if self.static_dir:
      self.cp_static_files(self.static_dir,outpath)
    else:
      self.cp_static_files(inpath,outpath)
    return 0
        
  def cp_static_files(self,inpath,outpath):
    """ automatic search for a 'static' folder and copy tree to output """ 
    if inpath==self.static_dir:
      dest=os.path.join(outpath,os.path.basename(inpath))
      if os.path.exists(dest):
        logger.warning('Remove old static folder')
        shutil.rmtree(dest) #not efficient. Should do it incrementaly...
      logger.info('cp_static_files %s -> %s' %(inpath,dest))
      copyfiles(inpath,dest)      
    else:
      for folder in os.listdir(inpath):
        if folder == 'static':
          logger.info('found static folder, copy all...')
          dest=os.path.join(outpath,folder)
          src=os.path.join(inpath,folder)
          if os.path.exists(dest):
            logger.warning('Remove old static folder')
            shutil.rmtree(dest) #not efficient. Should do it incrementaly...
          logger.info('cp_static_files %s -> %s' %(src,dest))
          copyfiles(src,dest)
    return 0
    
    
def copyfiles(src,dst):
    logger.warning('copyfiles from %s to %s' %(src,dst))
    #try:
    shutil.copytree(src, dst)
    #except:
    #  logger.warning("error copying files...")
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

def scan_path(path,ext_lst=['md','markdown']):
  """ Scan for markdown files in a  folder. Not (yet?) recursive """
  if not os.path.exists(path):
    logger.debug('scan_path: invalid path : %s' %(path,files))
    return -1
  pages={}
  files=[]
  for item in glob.glob(os.path.join(path,'*.*')):
    if string.split(os.path.basename(item),'.')[-1] in ext_lst:
      files.append(item)
  logger.debug('scan_path: %s : %s' %(path,files))
  res = None
  pagelist=[]
  articledict={}
  for item in files:
    res=os.path.basename(item).split()
    res=string.split(os.path.basename(item),'.')
    #print 'scan_path: res : %s' %res      
    if res[0] not in pagelist:
      logger.debug('scan_path: add page : %s' %res[0])      
      pagelist.append(res[0])
      articledict[res[0]]=[]  #or add itself?
    articledict[res[0]].append(item)    
  pages['pagelist'] = pagelist
  if len(pagelist)>0:
    for page in pagelist:      
      logger.debug('scan_path: pages= %s' %page)
      logger.debug('scan_path: articles= %s' %articledict[page])      
      pages[page]=articledict[page] 
  #look for templates/layout... To ENHANCE...
  pages['template']=glob.glob(os.path.join(path,'*.tpl'))              
  if os.path.isfile(os.path.join(path,'layout.tpl')):
    logger.info('scan_path: found general layout file : %s' %os.path.join(path,'layout.tpl'))
    pages['layout']=os.path.join(path,'layout.tpl')
  return pages
  
  
class Builder(object): 
  """  File based generic mardown/txt/HTML content parser. Only One level deep   """
  def __init__(self):
    self.path=None
    self.ext_lst=['txt','md','html']
    self.excludes=['static','js','img','css']
    self.outfolder=None
    self.layout=None
    self.pages={}
    self.pages['pagelist']=[]
    #self.cfg=Config()
        
  def scan(self,path): 
    """ Scan directory and output a dict   """
    if os.path.exists(path):
      self.path=path
      logger.debug('builder.scan: %s' %self.path)
      self.pages=scan_path(path,self.ext_lst)
    else:
      logger.error('builder.scan: path does not exist : %s' %path)
    return self.pages  
  
  def write(self,srcpath,buildpath):
    self.outfolder=buildpath
    if not os.path.exists(self.outfolder):
      os.makedirs(self.outfolder)  
    if buildpath != srcpath:  
      logger.info('builder.write to %s' %self.outfolder)
      for page in self.pages['pagelist']:
        for item in self.pages[page]:
          try:
            shutil.copy(item,os.path.join(self.outfolder,os.path.basename(item))) 
          except:
            logger.warning('builder.write cannot copy %s to %s' %(item,os.path.join(self.outfolder,os.path.basename(item))))    
          if self.layout == None:
            if not os.path.exists(os.path.join(self.outfolder,'layout.tpl')):
              shutil.copy(self.layout,os.path.join(self.outfolder,'layout.tpl'))   #use basename? 
      cfg=os.path.basename(self.path)+'.pims'
    else:
      cfg='.pims'
    logger.debug('builder.write to %s' %self.outfolder)
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
  def __init__(self):
    self.outpath=None
    self.pages={}
    self.layout=None
    self.style='tabs'  # tabs style
    #self.cfg=Config()
    
  def scan(self,path):
    if os.path.exists(path):
      self.path=path
      logger.debug('generator.scan: %s' %self.path)
      self.pages=scan_path(path)
    else:
      logger.error('generator.scan: path does not exist : %s' %path)
    #print self.pages
    #if self.layout==None and layout in self.pages.keys(): 
    #self.layout=self.pages['layout']

  def chckpages(self):
    """ Check minimal keys... """
    #defindedPagesKeys=Pages().keys() #TBD
    result=False
    minimalPagesKeys=['pagelist']
    for key in self.pages.keys():
      if key in minimalPagesKeys:
        result=True
      if key not in minimalPagesKeys:
        logger.debug('generator.chckpages: undefined keys: %s' %key)
    return result
  
  def process(self,path,outpath=None,pagelist=None,style='tabs',pos=None): #render?
    if path== None:
      logger.error('generator.process: invalid path : %s' %(path))
      return -1
    if not os.path.exists(path):
      logger.error('generator.process: invalid path : %s' %(path))
      return -1
    if pagelist==None:
      self.scan(path) #get config...
    if outpath == None:
      logger.warning('generator.process: no output folder specified, using "_www" folder')          
      self.outpath=os.path.join(path,'_www')
    else:
      self.outpath=outpath
    if not os.path.exists(self.outpath):
      logger.info('generator.process: creating : %s' %(self.outpath))      
      os.makedirs(self.outpath)
    if self.chckpages()== False:
      logger.error('generator.process: chckpages error')
      return 1
    if self.pages['pagelist']==None:
      logger.error('generator.process: self.pages[%s]==None' %('pagelist'))
      return 2
    for page in self.pages['pagelist']:
      logger.info('generator.process:  writing %s.html (layout:%s style: %s)' %(page,self.layout,self.style))
      if self.layout != None:
        page_tpl=open(self.layout).read()
      else:
        page_tpl=tpl_page # ???
      if style:
        self.style=style
      html_page=generate_page(page_tpl,self.pages[page],pagename=page,title=page,style=self.style) #self.title
      with open(os.path.join(self.outpath,page+'.html'),'w') as f:
        f.write(html_page)
    #copyfiles(path,self.outpath) #?

  #def run(self,path):
  # scan()
  # write()
    

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
    logger.error('input path does not exist... Aborting.')
    return 1  
  if not os.path.isdir(args.inpath):  
    logger.error('input path is not a folder... Aborting.')
    return 1
  error=0
  pims=Pimouss(plugin=args.plugin,layout=args.layout_template,static_dir=args.static_dir)
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
    logger.error('input path does not exist... Aborting.')
    return 1  
  if not os.path.isdir(args.inpath):  
    logger.error('input path is not a folder... Aborting.')
    return 1
  logger.info('build:')
  logger.info('  input      : %s'%args.inpath)
  logger.info('  output     : %s'%args.output_path)
  logger.info('  plugin     : %s'%args.plugin)
  logger.info('  template   : %s'%args.layout_template)
  logger.info('  static_dir : %s'%args.static_dir)
  error=0
  pims=Pimouss(plugin=args.plugin,layout=args.layout_template,static_dir=args.static_dir)
  pims.build(args.inpath,buildpath=args.output_path)
  return error

def _generate(args):
  if not os.path.exists(args.inpath):
    logger.error('input path does not exist... Aborting.')
    return 1  
  if not os.path.isdir(args.inpath):  
    logger.error('input path is not a folder... Aborting.')
    return 1
  logger.info('generate:')
  logger.info('  input      : %s'%args.inpath)
  logger.info('  output     : %s'%args.output_path)
  logger.info('  plugin     : %s'%args.plugin)
  logger.info('  template   : %s'%args.layout_template)
  logger.info('  static_dir : %s'%args.static_dir)
  logger.info('  tab style  : %s'%args.tab_style)
  logger.info('  tab pos    : %s'%args.tab_position)
  error=0
  pims=Pimouss(plugin=args.plugin,layout=args.layout_template,static_dir=args.static_dir)
  pims.generate(args.inpath,outpath=args.output_path,style=args.tab_style,pos=args.tab_position) 
  return error

def _make(args):
  if not os.path.exists(args.inpath):
    logger.error('input path does not exist... Aborting.')
    return 1  
  if not os.path.isdir(args.inpath):  
    logger.error('input path is not a folder... Aborting.')
    return 1
  logger.info('make:')
  logger.info('  input      : %s'%args.inpath)
  logger.info('  output     : %s'%args.output_path)
  logger.info('  plugin     : %s'%args.plugin)
  logger.info('  template   : %s'%args.layout_template)
  logger.info('  static_dir : %s'%args.static_dir)
  logger.info('  tab style  : %s'%args.tab_style)
  logger.info('  tab pos    : %s'%args.tab_position)
  error=0
  pims=Pimouss(plugin=args.plugin,layout=args.layout_template,static_dir=args.static_dir)
  pims.process(args.inpath,outpath=args.output_path,style=args.tab_style,pos=args.tab_position)   
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
  paser_log.add_argument("-d", "--debug",action='store_true',default=False,help="verbose output logging")
  paser_log.add_argument("-q", "--quiet",action='store_true',default=False,help="limit output logging to warning/error")
  subparsers = parser.add_subparsers(title="Available commands")
  parser_gui=subparsers.add_parser("gui",help="launch Qt (PySide) desktop interface.")  
  parser_gui.set_defaults(func=_gui)
  parent_subparser = argparse.ArgumentParser(add_help=False)  
  parent_subparser.add_argument("-tpl", "--layout_template",type=str,default=None,help="layout template file to use")
  parent_subparser.add_argument("-static","--static_dir",type=str,default=None,help="directory path of assets/static files")
  parent_subparser.add_argument("-of","--output_path",type=str,default=None,help="output folder path (default to _html)")
  parent_subparser.add_argument("-p", "--plugin",choices=plugins,default=None,help="plugin to use.")
  parser_init=subparsers.add_parser("init",parents=[parent_subparser],help="TODO init a pimouss project (write layout and static files).")  
  parser_init.set_defaults(func=_init)
  parser_build = subparsers.add_parser("build",parents=[parent_subparser],help="path -> markdown")
  parser_build.set_defaults(func=_build)
  parser_generate = subparsers.add_parser("generate",parents=[parent_subparser],help="markdown -> html")
  parser_generate.add_argument("-tstyle","--tab_style",choices=('tabs','pills'),default='tabs',
                               help="tabs style (generation only), default to tabs")
  parser_generate.add_argument("-tpos","--tab_position",choices=('left','right'),default=None,
                               help="tabs position (generation only), default to left")
  parser_generate.set_defaults(func=_generate)
  parser_make = subparsers.add_parser("make",parents=[parent_subparser],help="path -> html")
  parser_make.add_argument("-tstyle","--tab_style",choices=('tabs','pills'),default='tabs',
                           help="tabs style (generation only), default to tabs")
  parser_make.add_argument("-tpos","--tab_position",choices=('left','right'),default=None,
                           help="tabs position (generation only), default to left")
  parser_make.set_defaults(func=_make) 
  # add auto mode?
  #parser_execute=subparsers.add_parser("execute",#parents=[parent_subparser],#parent parser??
  #                                   help="Execute command contains in INFILE (one cmd per line)")
  #parser_execute.set_defaults(func=_exec_from_file) 
  parser.add_argument("inpath",type=str,default='.',help="input path")
  args=parser.parse_args()
  import datetime
  start=datetime.datetime.now()
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

