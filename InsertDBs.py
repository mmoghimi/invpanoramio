import jinja2
import os

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

import cgi
import datetime
import urllib
import webapp2

from google.appengine.ext import db
from google.appengine.api import users

from Image import *

#handle = open("data/db_tree.txt", "r")
#print(handle.readline())
#handle.close()

class InsertDBs(webapp2.RequestHandler):
    def get(self):        
        template_values = {
            'url_linktext': '*',
        }

        tags_list = ['im2gps']
#        tags_list = ['panoramio', 'car', 'tree', 'building', 'street', 'landmark']
#        tags_list = ['street', 'landmark']

        for tag in tags_list:
            p = db.Key.from_path('images', tag)
            print(p)
            
            db_tag = open("data/db_%s.txt"%tag, "r")
            
            cnt = 0
            for line in db_tag.xreadlines():
                cnt += 1
                
#                if cnt == 100:
#                    break
                line = line.decode('utf-8').split('\t')
                
                #print(line[1], line[0])
                #print(line[1], str(line[1]))

                image = Image(parent = p, id = int(line[0]))
                image.tag = str(line[1])
                image.tags = db.Text(line[2])
                image.url = str(line[3])
                image.gps = db.GeoPt(str(line[4]), str(line[5]))
                image.put()
        
            db_tag.close()
            
            print("%d rows inserted for tag:%s."%(cnt, tag))

        template = jinja_environment.get_template('insert_dbs.html')
        self.response.out.write(template.render(template_values))
