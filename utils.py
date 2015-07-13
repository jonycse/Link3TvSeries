__author__ = 'AbuZahedJony'
import urllib2, os
def download_file(url, download_path, block_sz):
    file_name = url.split('/')[-1]
    u = urllib2.urlopen(url)
    download_path = download_path + file_name
    print "Path", download_path

    # if you do not want to download existing file uncomment this line
    #if os.path.exists(download_path):
    #    print "Skipping ..... File already exists"
    #    return

    f = open(download_path, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s [SIZE: %s]\n" % (file_name, file_size)

    file_size_dl = 0
    k = 0
    p = 0
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        k += 1
        if k>120:
            p += 1
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print status
            k = 0
        if p>5:
            print "Downloading: %s [SIZE: %s]" % (file_name, file_size)
            p = 0

    f.close()