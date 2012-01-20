from google.appengine.ext import db

class Image(db.Model):
    """An image from Flickr."""
    id = db.IntegerProperty(required=True)
    url = db.TextProperty()
    gps = db.GeoPtProperty()
    tag = db.StringProperty()
    tags = db.StringProperty(multiline=True)
