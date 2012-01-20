#!/usr/bin/python2.7
#from google.appengine.api import urlfetch
import urllib2

__author__ = 'mmoghimi'
import xml.dom.minidom

def xmltodict(xmlstring):
    doc = xml.dom.minidom.parseString(xmlstring)
    remove_whilespace_nodes(doc.documentElement)
    return elementtodict(doc.documentElement)

def elementtodict(parent):
    child = parent.firstChild
    if (not child):
        return None
    elif (child.nodeType == xml.dom.minidom.Node.TEXT_NODE):
        return child.nodeValue

    d={}
    while child is not None:
        if (child.nodeType == xml.dom.minidom.Node.ELEMENT_NODE):
            try:
                d[child.tagName]
            except KeyError:
                d[child.tagName]=[]
            d[child.tagName].append(elementtodict(child))
        child = child.nextSibling
    return d

def remove_whilespace_nodes(node, unlink=True):
    remove_list = []
    for child in node.childNodes:
        if child.nodeType == xml.dom.Node.TEXT_NODE and not child.data.strip():
            remove_list.append(child)
        elif child.hasChildNodes():
            remove_whilespace_nodes(child, unlink)
    for node in remove_list:
        node.parentNode.removeChild(node)
        if unlink:
            node.unlink()

def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step

def get_tags(photo_url):
#    print(photo_url)

    data_html = urllib2.urlopen(photo_url).read()
    start_tag = '<ul id="tags">'
    end_tag = '</ul>'

    start = data_html.find(start_tag)
    end = data_html.find(end_tag, start)

    ul_tag = data_html[start:end+len(end_tag)]

    if not len(ul_tag):
        return []

    dic = xmltodict(ul_tag)

    tags = [x[u'a'][0].strip() for x in dic[u'li']]
    if tags[-1].startswith(u"Show all tags"):
        tags = tags[:-1]

    return tags



if __name__=="__main__":

    db_panoramio = open("data/db_panoramio.txt", "w")

    tag = "panoramio"

    step_lat = 1
    step_long = 1
    counter = 0
    for long in drange(-180, 180, step_long):
        for lat in drange(0, 90, step_lat):
            print(lat, lat+step_lat, long, long+step_long)

            url = "http://www.panoramio.com/map/get_panoramas.php?set=public&from=0&to=10&minx=-%f&miny=-%f&maxx=%f&maxy=%f&size=medium&mapfilter=true"%(lat, long, lat+step_lat, long+step_long)
            response = urllib2.urlopen(url)
            data = eval(response.read().replace("true", "True").replace("false", "False"))
            #            print(data)
            for photo in data['photos']:
                counter += 1
                latitude = photo['latitude']
                longitude = photo['longitude']
                url = photo['photo_file_url']
                tags = " ".join(get_tags(photo['photo_url']))

                line = u'%d\t%s\t%s\t%s\t%s\t%s\n'%(counter, tag, tags, url, latitude, longitude)
                db_panoramio.write(line.encode('utf-8'))

    db_panoramio.close()
