import time
from Image import Image
from PyGeocoder import PyGeocoder
import jinja2
import os
#import appengine_utilities

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

import cgi
import datetime
import urllib
import webapp2
import random

from pygeocoder.pygeocoder import Geocoder
from google.appengine.ext import db
from google.appengine.api import users
#import appengine_utilities.sessions
from gaesessions import get_current_session

import flickrapi

class Game(webapp2.RequestHandler):
    default_image_url = "http://www.google.com/intl/en_com/images/srpr/logo3w.png"
    tags_list = ["im2gps", "panoramio", "building", "car", "tree", "street", "landmark"]
#    tags_list = []

    def get_image(self, id, tag):
        try:
            images = db.GqlQuery("SELECT * FROM Image WHERE id = :1 AND tag = :2", id, tag)
            #        images = db.GqlQuery("SELECT * FROM Image WHERE id = 1")
            #        images = db.GqlQuery("SELECT * FROM Image WHERE id = 1 AND tag=building")
            #        images = db.GqlQuery("""SELECT * FROM Image WHERE id = :1 """, 199)
            #                            "ORDER BY id DESC LIMIT 10")

            #        images = db.GqlQuery("SELECT * "
            #                            "FROM Image "
            #                            "WHERE WHERE ANCESTOR IS :1"
            #                            "ORDER BY id DESC LIMIT 10",
            #                            db.Key.from_path('images', 'car'))

            #        images = Image.all()
            #for image in images:
            #   print(image.id, image.tag, image.url)
            #   print(image)
            #   print(image.id)
            #   pass

            return images[0]

        except:
            return None

    def create_image(self):
        image = Image(parent = None, id = int(-1))
        image.tag = str("")
        image.tags = db.Text("")
        image.url = str("http://www.feeltealclub.com/adm/zbl/images/image_not_found.jpg")
        image.gps = db.GeoPt(0, 0)
        image.address = ""
        return image


    def initialize_session(self):
        self.session["iter"] = 0
        self.session["tag"] = "panoramio"
        self.session["gps"] = (0, 0)

        self.session["limits"] = {}
        for tag in self.tags_list:
            self.session["limits"][tag] = 1000
        self.session["limits"]["panoramio"] = 2186
        self.session["limits"]["im2gps"] = 300

    def restart_session(self):
        self.session.clear()
        self.initialize_session()

    def update_location(self, selected_gps):
        alpha = 0.3
        p = self.session["gps"]
        new_lat = p[0] + alpha * (selected_gps.lat - p[0])
        new_long = p[1] + alpha * (selected_gps.lon - p[1])
        self.session["gps"] = new_lat, new_long

    def select_images(self):
        tag = self.session["tag"]
        num_images = self.session["limits"][tag]

        left_id = random.randint(1, num_images)
        left_image = self.get_image(left_id, tag)
        if left_image is None:
            left_image = self.create_image()
        self.session["left_image"] = left_image

        right_id = left_id
        while right_id == left_id:
            right_id = random.randint(1, num_images)

        right_image = self.get_image(right_id, tag)
        if right_image is None:
            right_image = self.create_image()
        self.session["right_image"] = right_image


        return left_image, right_image

    def get_geo_name(self, gps):
        return ""
    #        results = Geocoder.reverse_geocode(45.424571, -75.695661)
    #        return results[0]
    #        GOOGLE_KEY = "ABQIAAAAeJWZzQdtZ96kLOISc516kBQI7l6f26DRsmiK7g2tPTGLKSlIWxRb81Ija51HBP3a9eoCn-GxR3PacQ"
    #        g = geocoders.Google(GOOGLE_KEY)
    #        p = Point(gps.lat, gps.lat)
    #        return g.reverse(p)

    def get(self):
        start_time = time.time()

        self.message = ""
    #        self.session = appengine_utilities.sessions.Session()
        self.session = get_current_session()

        # initialize session
        if not self.session.has_key("iter"):
            self.initialize_session()

        # handling actions
        action = self.request.get("action")
        if  action == "restart":
            self.restart_session()
        elif action == "pass":
            pass
        elif action == "tag_select":
            if len(self.request.get("tag_select")) > 0:
                self.session["tag"] = self.request.get("tag_select")
        elif action == "select_left":
            if self.session.has_key("left_image"):
                self.update_location(self.session["left_image"].gps)
            else:
                self.message += " There was no previous left image!"
        elif action == "select_right":
            if self.session.has_key("right_image"):
                self.update_location(self.session["right_image"].gps)
            else:
                self.message += " There was no previous right image!"


        self.session["iter"] += 1

        t1 = time.time()
        left_image, right_image = self.select_images()
        t2 = time.time()

        debug_message = "select_images took %.2f sec"%(t2-t1)

        left_image.address = PyGeocoder.get_name(left_image.gps.lat, left_image.gps.lon)
        right_image.address = PyGeocoder.get_name(right_image.gps.lat, right_image.gps.lon)

        end_time = time.time();

        debug_message += "\n while the whole get took %.2f sec"%(end_time-start_time)
        template_values = {
            'message': self.message,
            'debug_message': debug_message,
            #            'left_image_url': left_image_url,
            #            'test_image_url': 'http://www.google.com/intl/en_com/images/srpr/logo3w.png',
            "test_image_url": "http://dailydish.typepad.com/.a/6a00d83451c45669e201675fafab5a970b-800wi",
            #            'right_image_url': right_image_url,
            "left_image": left_image,
            "right_image": right_image,
            "tags_list": Game.tags_list,
            "current_tag": self.session["tag"],
            "iter": self.session["iter"],
            "message": self.get_geo_name(left_image.gps),
            "current_gps": self.session["gps"],
            "current_address": PyGeocoder.get_name(self.session["gps"][0], self.session["gps"][1])
        }

        template = jinja_environment.get_template('game.html')
        self.response.out.write(template.render(template_values))
