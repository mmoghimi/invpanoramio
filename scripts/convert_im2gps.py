__author__ = 'mmoghimi'


def get_photo_url(server, id, secret):
    return "http://static.flickr.com/%s/%s_%s_b.jpg"%(server, id, secret)

out = open("data/db_im2gps.txt", "w")

city_list = ["Tokyo", "nyc", "London"]

counter = 0
image = {}
tag = 'im2gps'

for city in city_list:
    file_address = "/home/mmoghimi/Dropbox/geolocation/im2gps-Flickr_code_2009_05_14/query_imgs/out/%s.txt"%city

    handle = open(file_address)
    city_counter = 0

    for line in handle.xreadlines():
        if line.count(':') < 1:
            continue

    #    print(line)

        pos = line.find(':')
        key = line[:pos]
        value = line[pos+1:]

        image[key] = value.strip()
    #    print(key, value)

        cache = {}

        if line.startswith("interestingness"):

    #        print(image)
            tags = image["tags"]

            image["photo"] = image["photo"].split()
            id = image["photo"][0]
            secret = image["photo"][1]
            server = image["photo"][2]
            url = get_photo_url(server, id, secret)

            latitude = image["latitude"].strip()
            longitude = image["longitude"].strip()

            # checking for duplicates
            if cache.has_key(url):
                continue

            cache[url] = True

            counter += 1
            line = u'%d\t%s\t%s\t%s\t%s\t%s\n'%(counter, tag, tags, url, latitude, longitude)
            out.write(line.encode('utf-8'))
            print(line)

            city_counter += 1
            if city_counter == 100:
                break

            image = {}


    handle.close()

out.close()