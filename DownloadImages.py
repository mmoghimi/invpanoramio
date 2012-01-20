import jinja2
import os

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

import cgi
import datetime
import urllib
import webapp2

from google.appengine.ext import db
from google.appengine.api import users

import flickrapi
import Image

class DownloadImages(webapp2.RequestHandler):
    def get(self):
        api_key = "4090923a26e9a28315e3489b726a1885"
        flickr = flickrapi.FlickrAPI(api_key)
        
        counter = 0

        per_page = 1000
        page = 0
        tag = 'car'
        
        photos = flickr.photos_search(tags=tag, has_geo="1", per_page="1", page="1", extras="geo", privacy_filter="1", sort="interestingness-desc")[0]
        total = photos.get('total')
        print_var('total')
        
        while False:
            page += 1
            if counter >= 1 or counter >= total:
                break

            photos = flickr.photos_search(tags=tag, has_geo="1", per_page=str(per_page), page=str(page), extras="geo", privacy_filter="1", sort="interestingness-desc")[0]

            for p in photos:
                print("Processing photo #" + str(counter) + " ...")
                counter += 1

                server = p.get('server')
                farm = p.get('farm')
                id = p.get('id')
                sec = p.get('secret')
                latitude = p.get('latitude')
                longitude = p.get('longitude')
                title = p.get('title')
                url = get_photo_url(farm, server, id, sec)
                new_name = get_new_photo_name(counter, farm, server, id, sec, latitude, longitude)

                print(p)
                print_var('title')
                print_var('latitude')
                print_var('longitude')
                print_var('url')
                print_var('new_name')

                os.system("wget " + url + " -O " + tag + "/" + new_name + " &")

        
        template_values = {
            'url_linktext': '*',
        }

        template = jinja_environment.get_template('download_images.html')
        self.response.out.write(template.render(template_values))
        
def print_var(v):
    print(v + ": " + eval(v))

def get_photo_url(farm, server, id, secret):
    return "http://farm%s.static.flickr.com/%s/%s_%s.jpg"%(farm, server, id, secret)

def get_new_photo_name(counter, farm, server, id, secret, latitude, longitude):
    return "%04d_%s,%s,%s,%s_%s_%s.jpg"%(counter, farm, server, id, secret, latitude, longitude)

#def create_dir(dir_name):
#    os.system("mkdir " + dir_name)

