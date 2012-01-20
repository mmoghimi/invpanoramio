import matplotlib.pyplot as plt


tags_list = ["panoramio", "building", "car", "tree", "street", "landmark"]
counter = 0
for tag in tags_list:

    fig = plt.figure()
    ax = fig.add_subplot(111)

    handle = open("data/db_%s.txt"%tag, "r")
    p = [x.replace('\n', '').split('\t')[-2:] for x in handle.readlines()]

    lat = [float(a[0]) for a in p]
    long = [float(a[1]) for a in p]
    handle.close()

    ax.plot(long, lat, '.')
    ax.set_title('Spread of images downloaded from %s'%tag)
    plt.xlabel('longitude')
    plt.ylabel('latitude')
#    plt.show()
    plt.savefig("figures/db_%s.png"%tag)
