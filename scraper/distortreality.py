import Queue
import re
import threading
import urllib2
import BeautifulSoup


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

    regex = r'product.*?href="(/collections/.+?)">.*img src="(.*?)".*?\$([0-9]+\.[0-9]+).*?name">.*?\s([a-zA-Z0-9\s\&#;,]+?)-.*?([a-zA-Z0-9\s\&#;,]+?) ([LP127&quot;]+)'

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


    for i in range(1,last+1):
        newAddr = addr + extension + str(i)

        threadQueue.put(newAddr)

    threadQueue.join()

    while resultQueue.empty() == False:
        siteData = siteData + resultQueue.get().read()


    listBlocks = siteData.split('/li')
    items = []
    for block in listBlocks:
        values = re.findall(regex, block, re.DOTALL)
        if len(values) > 0:
            items.append(values[0])



    import pdb; pdb.set_trace()

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
                tmpContainer.append(addr + temp[0])
            # Put everything else in "as is"
            else:
                tmpContainer.append(part)

        tmpContainer.append(siteName)
        finalList.append(tmpContainer)

    for record in finalList:
        print record

    #finalList = hackedListToDict(finalList)
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