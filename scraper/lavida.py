# Scraper for la vida es un mus records

# TODO: Get exchange rate somehow and convert prices to USD

import urllib2
import re
import os
import threading
import Queue
import sys

def getItems():
    # 7"s and 12"s are on separate pages, need to make two passes
    # 7" pages
    addr = 'http://lavidaesunmus.com/prestashop/category.php?id_category=6'
    extension = '&p='
    newAddr = addr
    laVidaItems = getSpecificItems(addr, extension, newAddr, 7)

    # 12" pages
    addr = 'http://lavidaesunmus.com/prestashop/category.php?id_category=10'
    newAddr = addr
    laVidaItems = laVidaItems + getSpecificItems(addr, extension, newAddr, 12)

    # Process the list to put elements in the right order
    return (arrangeItems(laVidaItems), "La Vida Es Un Mus")

def getSpecificItems(addr, extension, newAddr, vinylSize):
    # matches pattern pulled from most recent version
    # of la vida.
    # (image link) (direct link) (band and album) (price)
    #regex = r'<img src="(.*?)".*\n.*<h3><a href="(.*?)" title="(.*?)".*\n.*\n.*\n.*\n.*\n.*\$([0-9]*\.[0-9]*)'

    # Need image link, direct link, band, album, price
    # image, band and album, link, price
    regex = r'<a href="(.*?)".*?title="(.*?)\s[712LP].*?[\S\s]*?<img src="(.*?)"[\S\s]*?([0-9]+\.[0-9]+)'

    siteName = "La Vida Es Un Mus"

    threadQueue = Queue.Queue()
    resultQueue = Queue.Queue()

    # figure out the number of the last page of records
    # and get the first page of data while we're at it
    #try:
    firstPage = urllib2.urlopen(newAddr)
    siteData = firstPage.read()
    #except urllib2.HTTPError, err:
    #if err.code == 404:
        #hurr
    #elif err.code == 403:
        #durr
    #else:
    #except urllib2.URLError:


    # find the last page
    temp = re.findall(r'p=([0-9]*)', siteData)
    last = int(max(temp))
    print "last page is %d" % last

    # start up our threads. This site doesn't have a lot of pages,
    # so we can use "last" as our guideline
    for i in range(0,last):
        t = ThreadPageGet(threadQueue, resultQueue)
        t.setDaemon(True)
        t.start()

    # Loop to pull data from each page of the distro
    # Start from 2 because of site's conventions
    # +1 accounts for offset
    for i in range(2,last+1):
        newAddr = addr + extension + str(i)

        threadQueue.put(newAddr)

    threadQueue.join()

    while not resultQueue.empty():
        siteData = siteData + resultQueue.get().read()

    #Turn pound sterling symbol into $ to make finding prices easier
    tempData = re.sub(u'\u00A3', '$', siteData)

    items = re.findall(regex, tempData)
    finalList = []

    for line in items:
        # Clean up all the weird characters encountered, and
        # change prices to floats
        tmpContainer = []
        for part in line:
            part = re.sub(r'\&#039;', '\'', part)
            part = re.sub(r'[0-9]+\&quot;', '', part)
            part = re.sub(r'[0-9]+\&rdquo;', '', part)
            part = re.sub(r'\&auml;', 'a', part)
            part = re.sub(r'\&amp;', '&', part)
            part = re.sub(r'\&Uuml;', 'u', part)
            part = re.sub(r'\&ndash;', '-', part)
            part = re.sub(r'\&ne;', 'Y', part)
            part = re.sub(r'RESTOCK', '', part)
            part = re.sub(r'BACK IN STOCK', '', part)

            part = re.sub(r'&Alpha;', '', part)
            part = re.sub(r'&nu;', '', part)
            part = re.sub(r'\xcf', '', part)
            part = re.sub(r'\x8e', '', part)
            part = re.sub(r'&phi;', '', part)
            part = re.sub(r'&epsilon;', '', part)
            part = re.sub(r'&lambda;', '', part)
            part = re.sub(r'&eta;', '', part)
            part = re.sub(r'&Epsilon;', '', part)
            part = re.sub(r'&pi;', '', part)
            part = re.sub(r'&iota;', '', part)
            part = re.sub(r'&beta;', '', part)
            part = re.sub(r'\xce', '', part)
            part = re.sub(r'\xaf', '', part)
            part = re.sub(r'&omega;', '', part)
            part = re.sub(r'&sigma;', '', part)
            # Change prices to floats
            if re.match(r'[0-9]*\.[0-9]*', part):
                tmpContainer.append(float(part))
            # Put everything else in "as is"
            else:
                tmpContainer.append(part)

        # Add vinyl size and website origin to list
        tmpContainer.append(vinylSize)
        tmpContainer.append(siteName)
        finalList.append(tmpContainer)

    return finalList

# Rearranges the order of elements in a list so that the returned
# list will be in the form:
# [string, string, string, string,	float, 	int, string]
#img link, band, directlink, album, price, vinylsize, sitename
def arrangeItems(items):
#items take form of [image link, direct link, band album, price, size, site]

    # image, band and album, link, price
    newList = []
    for item in items:
        tmpContainer = []
        album = re.findall(r'-(.+)$', item[1])
        band = re.findall(r'(.*)-.+$', item[1])

        # No '-' found, so it's probably a comp.
        # Set band to V/A and album to everything after
        # make this only do V/A if "V/A" is found, otherwise
        # put it all under "album"
        if len(album) == 0 or len(band) == 0:
            if re.match(r'V/A', item[1]):
                band = "V/A"
                album = re.findall(r'V/A(.*)', item[1])
                album = album[0]
            else:
                band = item[1]
                band = band[0]
                album = ''
        else:
            band = band[0]
            album = album[0]

        newList.append({'img': item[0],
                        'band': band,
                        'direct': item[2],
                        'album': album,
                        'price': item[3],
                        'size': item[4],
                        'site': item[5]
                        })
    return newList


# This class runs as a thread which will grab a webpage from
# a queue of pages that need to be scraped
class ThreadPageGet(threading.Thread):
    # queueA - The queue of pages to get
    # queueB - Where the results of a page are sent
    def __init__(self, queueA, queueB):
        threading.Thread.__init__(self)
        self.queueA = queueA
        self.queueB = queueB

    def run(self):
        while True:
            # get address from queueA
            addr = self.queueA.get()

            try:
                print "Thread waiting for: " + addr
                pageData = urllib2.urlopen(addr)
            except IOError:
                print "Unable to open: " + addr
            self.queueB.put(pageData)
            self.queueA.task_done()
