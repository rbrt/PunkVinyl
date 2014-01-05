import Queue
import re
import threading
import urllib2

# organizes a list of lists into
# a list of dictionaries so that the order in
# which details are pulled from each website
# doesn't matter anymore
def hackedListToDict(unorgList):
    # (direct link) (image link) (price) (band) (album) (vinyl size)
    #unorgList - direct, img, price, band, album, size, site
    #               0     1    2     3      4      5     6
    newList = []
    for item in unorgList:
        direct = item[0]
        img = item[1]
        price = item[2]
        band = item[3]
        album = item[4]
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

def getItems():
    addr = 'http://distortreality.storenvy.com/collections/27203-all-products'
    extension = '/?page='
    newAddr = addr
    siteName = "Distort Reality"

    morePages = True
    # set pageCount arbitrarily high when running tests, set to 1
    # for normal usage

    endOfSiteRegex = r'There are no products in this collection yet'

    # matches pattern pulled from most recent version
    # of distort reality.
    # (direct link) (image link) (price) (band) (album) (vinyl size)

    regex = r'product.*?href="(/collections/.+?)">.*img src="(.*?)".*?\$([0-9]+\.[0-9]+).*?name">.*?\s([a-zA-Z0-9\s\&#;,/]+?)-.*?([a-zA-Z0-9\s\&#;,?/\']+?) ([712LP]?)"|$'

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

    temp = re.findall(r'page=([0-9]*)', siteData)
    convertToInt = lambda lol: map(int, lol)
    temp = map(convertToInt, temp)
    last = max(temp)[0]
    print "last page is %d" % last

    # start up our threads. 8 was the highest number that worked
    # consistently, any more than that and we start running into issues
    for i in range(1,8):
        t = ThreadPageGet(threadQueue, resultQueue)
        t.setDaemon(True)
        t.start()


    for i in range(1,5):
        newAddr = addr + extension + str(i)

        threadQueue.put(newAddr)

    threadQueue.join()

    while resultQueue.empty() == False:
        siteData = siteData + resultQueue.get().read()

    listBlocks = siteData.split('/li')

    items = []
    # there is a problem here, most likely the regex is broken
    for block in listBlocks:
        values = re.findall(regex, block, re.DOTALL)
        if len(values) > 0:
            items.append(values[0])


    finalList = []

    for part in items:
        if len(part[0]) == 0 or part[5] == "1":
            pass
        else:
            # change apostrophe code into actual apostrophes and
            # convert prices and vinyl size into floats and ints
            tmpContainer = []
            # Change links to full links by appending baseAddr
            tmpContainer.append(addr + part[0])
            tmpContainer.append(part[1])
            # Change prices to floats
            try:
                tmpContainer.append(float(part[2]))
            except:
                print "price conversion fucked up"
                print part
                print "\n\n\n\n\n"
            tmpContainer.append(re.findall(r'([A-Z].*)', part[3])[0])
            try:
                tmpContainer.append(re.findall(r'([A-Z].*)', part[4])[0])
            except:
                print "title conversion"
                print part
                print "\n\n\n\n\n"
            # Change sizes to ints
            if part[5] == "LP" or part[5] == "12":
                tmpContainer.append(12)
            else:
                try:
                    tmpContainer.append(int(part[5]))
                except ValueError:
                    print "size conversion fucked up"
                    print part
                    print "\n\n\n\n\n"

            tmpContainer.append(siteName)
            finalList.append(tmpContainer)

    finalList = hackedListToDict(finalList)
    # for ugh in finalList:
    #     print "%s %s\n" % (ugh['band'], ugh['album'])
    # print len(finalList)
    return (finalList, "Distort Reality")

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

if __name__ == "__main__":
    getItems()