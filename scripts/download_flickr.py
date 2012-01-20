#!/usr/bin/python2.7

import flickrapi

def print_var(v):
    print(v + ": " + eval(v))

def get_photo_url(farm, server, id, secret):
    return "http://farm%s.static.flickr.com/%s/%s_%s.jpg"%(farm, server, id, secret)

def get_new_photo_name(counter, farm, server, id, secret, latitude, longitude):
    return "%04d_%s,%s,%s,%s_%s_%s.jpg"%(counter, farm, server, id, secret, latitude, longitude)



api_key = "4090923a26e9a28315e3489b726a1885"
flickr = flickrapi.FlickrAPI(api_key)



tags_list = ['car', 'tree', 'building', 'street', 'landmark']


for tag in tags_list:
    db_tag = open("data/db_%s.txt"%tag, "w")

    counter = 0
    per_page = 100
    page = 0

    photos = flickr.photos_search(tags=tag, has_geo="1", per_page="1", page="1", extras="geo", privacy_filter="1", sort="interestingness-desc")[0]
    total = photos.get('total')
    print_var('total')

    while True:
        page += 1
        if counter >= 1000 or counter >= total:
            break
            

        photos = flickr.photos_search(tags=tag, has_geo="1", per_page=str(per_page), page=str(page), extras="geo,tags", privacy_filter="1", sort="interestingness-desc")[0]

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
            tags = p.get('tags')
            url = get_photo_url(farm, server, id, sec)
            new_name = get_new_photo_name(counter, farm, server, id, sec, latitude, longitude)

            print(p)
            #print_var('title')
            #print_var('latitude')
            #print_var('longitude')
            #print_var('url')
            #print_var('new_name')
            #print_var('tags')
            
            #print(u'%d\t%s\t%s\t%s\t%s\t%s\n'%(counter, tag, tags, url, latitude, longitude))

            #os.system("wget " + url + " -O " + tag + "/" + new_name + " &")
            line = u'%d\t%s\t%s\t%s\t%s\t%s\n'%(counter, tag, tags, url, latitude, longitude)
            db_tag.write(line.encode('utf-8'))
            
    db_tag.close()

