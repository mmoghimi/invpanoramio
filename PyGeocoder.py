import string
from google.appengine.api import urlfetch
import unicodedata

__author__ = 'mmoghimi'

class Callable:
    def __init__(self, anycallable):
        self.__call__ = anycallable

class PyGeocoder:
    def get_name(lat, long):
        query = "http://maps.google.com/maps/geo?q=%s,%s&output=json&oe=utf8&sensor=true_or_false&key=ABQIAAAAeJWZzQdtZ96kLOISc516kBQI7l6f26DRsmiK7g2tPTGLKSlIWxRb81Ija51HBP3a9eoCn-GxR3PacQ"%(str(lat), str(long))

        url = query
        result = urlfetch.fetch(url)
        if result.status_code == 200:
            dic = eval(result.content)
            address = dic["Placemark"][0]["address"]
            return filter(lambda x: x in string.printable, address)
            # return address.encode("ascii", "ignore")

    get_name = Callable(get_name)