#TODO: - Build in a mechanism to detect if a website has changed,
#		 maybe just check if no results are returned??	
#	   - Catch "badstatusline" exception and handle it
#	   - Kill duplicate entries
#	   - Create another entry when a split is encountered
#		 with band names reversed

import urllib2
import re
import os
import threading
import Queue
import sys

# organizes a list of lists into
# a list of dictionaries so that the order in
# which details are pulled from each website
# doesn't matter anymore
def hackedListToDict(unorgList):
    #unorgList - direct, img, band, album, price, size, site
    #               0     1    2     3      4      5     6
    newList = []
    for item in unorgList:
        direct = item[0]
        img = item[1]
        band = item[2]
        album = item[3]
        price = item[4]
        size = item[5]
        site = item[6]
        newList.append({'direct': direct,
                        'img': img,
                        'band': band,
                        'album': album,
                        'price': price,
                        'size': size,
                        'site': site,
                        })
    return newList

# Returns a list containing entries in the form:
# [string, string, string, string,	float, 	int, string]
#img link, band, directlink, album, price, vinylsize, sitename
#
# now we get:
# direct, img, band, album, price, size, site
def getItems():
    addr = 'https://www.havocrecords.com/all-items'
    baseAddr = 'https://www.havocrecords.com'
    extension = '?field_artist_value_selective=All&field_format_value=All&tid=All&field_country_tid_selective=All&sort_by=title&sort_order=ASC&page='
    newAddr = addr
    siteName = "Havoc Records"

    morePages = True
    # set pageCount arbitrarily high when running tests, set to 1
    # for normal usage

    endOfSiteRegex = r'No products match your search'

    # matches pattern pulled from most recent version
    # of havocrex.
    # (image link) (band) (direct link) (album) (price) (vinyl size)
    #regex = r'foaf:Image" src="(.*)" width=.*skos:prefLabel">([a-zA-Z0-9\s\&#;,-]*)<.*a href="(/[a-zA-Z0-9-]*/[a-zA-Z0-9-]*)">([a-zA-Z0-9-\s/,"()\&#;]*).*\$([0-9]*\.[0-9]*)<.*Vinyl\s//\s([0-9]*")'
    regex = r'href="(/.*?/.*?)">.*foaf:Image" src="(.*?)".*? datatype="">([a-zA-Z0-9\s\&#;,-]*?)<.*?href.*?>([a-zA-Z0-9\s\&#;,-]*?)</a.*?\$([0-9]+\.[0-9]+).*?Vinyl // (.*?)<'

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

    temp = re.findall(r'"Go to last page.*page=([0-9]*)', siteData)
    last = int(temp[0])
    print "last page is %d" % last

    # start up our threads. 8 was the highest number that worked
    # consistently, any more than that and we start running into issues
    for i in range(1,8):
        t = ThreadPageGet(threadQueue, resultQueue)
        t.setDaemon(True)
        t.start()


    # Loop to pull data from each page of the distro
    # +2 accounts for offset and also adds one because
    # Havoc's site doesn't actually point to the last page
    for i in range(1,last+2):
        newAddr = addr + extension + str(i)

        threadQueue.put(newAddr)

    threadQueue.join()

    while resultQueue.empty() == False:
        siteData = siteData + resultQueue.get().read()

    items = re.findall(regex, siteData)
    finalList = []

    # print out everything we found. Later on, this can add each
    # field to a database. Get the threaded approach working first
    for line in items:
        # change apostrophe code into actual apostrophes and
        # convert prices and vinyl size into floats and ints
        tmpContainer = []
        for part in line:
            part = re.sub(r'&#039;', '\'', part)
            # Change prices to floats
            if re.match(r'[0-9]*\.[0-9]*', part):
                tmpContainer.append(float(part))
            # Change sizes to ints
            elif re.match(r'[0-9]*"', part):
                temp = re.findall(r'([0-9]*)"', part)
                tmpContainer.append(int(temp[0]))
            # Change links to full links by appending baseAddr
            elif re.match(r'/[a-zA-Z0-9-]*/[a-zA-Z0-9-]*', part):
                temp = re.findall(r'/[a-zA-Z0-9-]*/[a-zA-Z0-9-]*', part)
                tmpContainer.append(baseAddr + temp[0])
            # Put everything else in "as is"
            else:
                tmpContainer.append(part)

        tmpContainer.append(siteName)
        finalList.append(tmpContainer)

    finalList = hackedListToDict(finalList)
    return (finalList, "Havoc Records")

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
            addr = self.queueA.get();

            try:
                #print "Thread waiting for: " + addr
                pageData = urllib2.urlopen(addr)
            except IOError:
                print "Unable to open: " + addr
            self.queueB.put(pageData)
            self.queueA.task_done()




