#!/usr/bin/env python
# -*- coding: utf-8 -*-

#example_foto.py
# CSS, JS, and  images
'''
import glob
def get_static_files(folder):
  static=[]
  for folder in 
    static+=
  return

static=get static_files(os.path.join(,'static'))
'''

static=[]

#header /banner
index='''
# My awesomme fotos !
Here are some foto I wanted to share with you.
- - - 
'''

# 1st tab content
albumname1='''
## albumename1
- - -
   
![Name of album1/foto1](http://mikrolax.me/static/img/daria.jpg)   
Something I want to say about albumname1 foto1.   
    
    
![Name of album1/foto2](http://mikrolax.me/static/img/daria.jpg)   
Something I want to say about albumname1 foto2.  
'''

# 2nd tab content
albumname2='''
## albumename2
- - -
   
![Name of album2/foto1](http://mikrolax.me/static/img/daria.jpg)   
Something I want to say about albumname2 foto1.   

![Name of album2/foto2](http://mikrolax.me/static/img/daria.jpg)   
Something I want to say about albumname2 foto2.  
'''

# using bootstrap caroussel
caroussel='''
## albumename1

  <div id="albumename1" class="carousel slide">
  <ol class="carousel-indicators">
  <li data-target="#myCarousel" data-slide-to="0" class="active"></li>
  <li data-target="#myCarousel" data-slide-to="1"></li>
  <li data-target="#myCarousel" data-slide-to="2"></li>
  </ol>

  <div class="carousel-inner">
  <div class="active item">  </div>

  <div class="item"> 

  </div>

  <div class="item">  </div>

  </div>

  <a class="carousel-control left" href="#myCarousel" data-slide="prev">&lsaquo;</a>
  <a class="carousel-control right" href="#myCarousel" data-slide="next">&rsaquo;</a>
  </div>
'''

# "contact" tab
contact='''
You can rich me by [e-mail](mailto:john.doe@mail-example.org)   
Or on social network : [Facebook](http://facebook.com/john.doe) | [Twitter](http://twitter.com/john_doe)       
'''

# "about" tab
about='''
Something about myself or this website.   
'''

#layout
layout='''
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-8">
        <title>Awesome fotos</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="documentation pimouss  open source static website generator">
        <meta name="author" content="mikrolax">

        <!--[if lt IE 9]>
              <script src="static/js/html5shiv.js"></script>
        <![endif]-->
       <link href="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.2.1/css/bootstrap-combined.min.css" rel="stylesheet">

        </head>
        <body>
        
        <div class="container">
        $content
        </div>

        <footer class="footer">
          <div class="container">
          	<hr>
              <p> &copy; 2013 John Doe  </p>
          </div>
        </footer>

        <script src="http://code.jquery.com/jquery-1.8.2.min.js"></script>
        <script src="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.2.1/js/bootstrap.min.js"></script>

        </body>
        </html>
'''
  
datas={ 'foto.md': index,
        'foto.albumname1.md': albumname1,
        'foto.albumname2.md': albumname2,
        'foto.albumname1_caroussel.md': caroussel,
        'foto.about.md': about,
        'foto.contact.md': contact,
        'static': static, 
        'layout.tpl':layout
        }

