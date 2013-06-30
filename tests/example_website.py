#!/usr/bin/env python
# -*- coding: utf-8 -*-

static=[]

#header /banner
index='''
# Welcome!
- - - 


'''

# Product page
product1='''
## product1
- - -
   
![product1](/img/product1.jpg)   
Something general I want to say about product1.     
'''
product1_tech='''
## Features
- - -
   * feature1 description
   * feature2 description
   * feature3 description
   * feature4 description
      
Something else.     
'''
product1_price='''
## Pricing
- - -

Insert tables defining prices, etc... 
     
'''

product2='''
## product2
- - -
   
![product2](/img/product2.jpg)   
Something general I want to say about product1.     
'''
product2_tech='''
## Features
- - -
   * feature1 description
   * feature2 description
   * feature3 description
   * feature4 description
      
Something else.     
'''
product2_price='''
## Pricing
- - -

Insert tables defining prices, etc... 
     
'''
# Services page
services='''
## Services
- - -
   Some description of provided services  
'''


# "contact" tab
contact='''
You can rich me by e-mail : [mailto:john.doe@mail-example.org](john.doe@mail-example.org)
Or on social network : [http://facebook.com/john.doe](Facebook) | [http://twitter.com/john_doe](Twitter)    
'''

# "about" tab
about='''
Something about myself or this website. Licence, privacy, legal mention.
'''

#layout
layout='''
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-8">
        <title>My Website</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="mywebsite description">
        <meta name="author" content="mywebsite">

        <!--[if lt IE 9]>
              <script src="static/js/html5shiv.js"></script>
        <![endif]-->
       <link href="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.2.1/css/bootstrap-combined.min.css" rel="stylesheet">
      
      </head>
        <body>


        <div class="container">

        <h1> My awesome website </h1> <hr>
        
        <ul class="nav nav-pills">
          <li><a href="index.html">Home</a></li>
          <li><a href="services.html"> Services </a></li>
           
          <li class="dropdown">
          <a class="dropdown-toggle" data-toggle="dropdown" href="#">
            Products
            <b class="caret"></b>
          </a>
            <ul class="dropdown-menu">
            <!-- links -->
              <li><a href="product1.html"> Product1 </a> </li>
              <li><a href="product2.html"> Product2 </a> </li>
                        
            </ul>
          </li>
        </ul>

        $content
        </div>

        <footer class="footer">
          <div class="container">
          	<hr>
              <p> &copy; 2013 mywebsite.com  </p>
          </div>
        </footer>

        <script src="http://code.jquery.com/jquery-1.8.2.min.js"></script>
        <script src="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.2.1/js/bootstrap.min.js"></script>

        </body>
        </html>
'''
  
datas={ 'index.md': index,
        'product1.md': product1,
        'product1.technical_description.md': product1_tech,
        'product1.pricing.md': product1_price,
        'product2.md': product2,
        'product2.technical_description.md': product2_tech,
        'product2.pricing.md': product2_price,
        'services.md': services,
        'contact.md': contact,
        'static': static, 
        'layout.tpl':layout
        }

