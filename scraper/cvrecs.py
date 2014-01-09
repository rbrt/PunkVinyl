import Queue
import re
import threading
import urllib2

# founditems = re.findall(r'<span class="product_name">(.*?)</span>', site, re.DOTALL)
# founditems = [item.replace('\n', '') for item in founditems]
# founditems = [re.findall(r'\s.*([a-zA-Z0-9]* LP|12"|7")', item)[0] for item in founditems]

# cleaneditems = [re.findall(r'\s+([A-Za-z][A-Za-z0-9\s/-]+ (?:LP|7"|12"))', item) for item in founditems if item]
# finalitems = [item for item in cleaneditems if len(item) > 0]

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
        mistake = False
        try:
            direct = item[0]
            img = item[1]
            price = item[2]
            band = item[3]
            album = item[4]
            size = item[5]
            site = item[6]
        except Exception as e:
            print "list to dict error"
            print e
            print item
            mistake = True
        if not mistake:
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
    addr = 'http://cvrecs.storenvy.com/collections/100368-all-products'
    baseAddr = 'http://cvrecs.storenvy.com'
    extension = '/?page='
    newAddr = addr
    siteName = "CVRECS"

    morePages = True
    # set pageCount arbitrarily high when running tests, set to 1
    # for normal usage

    endOfSiteRegex = r'There are no products in this collection yet'

    # matches pattern pulled from most recent version
    # of distort reality.
    # (direct link) (image link) (price) (band) (album) (vinyl size)

    regex = r'class="product.*?href="(/collections/.+?)">.*?img src="(.*?)".*?\$([0-9]+\.[0-9]+).*?<span class="product_name">(.*?)</span>'

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

    vinylTypes = r'(?:LP|7"|12"|lp|EP|ep|MLP|mlp|Lp|Ep)'
    infoRegex = r'\s+([A-Za-z][A-Za-z0-9\s/.!?\'(),"-]+ ' + vinylTypes + ')'

    items = [item for item in re.findall(regex, siteData, re.DOTALL)
             if len(re.findall(infoRegex, item[-1])) != 0]

    items = [list(item) for item in items]

    for item in items:
        item[-1] = re.findall(infoRegex, item[-1])[0].replace('\n', '')

    toDelete = []

    for item in items:
        albuminfo = item[-1]
        del item[-1]
        if 'split' in albuminfo:
            band = re.findall(r'(.*?)split.*'+vinylTypes, albuminfo)[0]
            album = 'split'
            vinyl = re.findall(r'(LP|7"|12"|lp|EP|ep|MLP|mlp)', albuminfo)[0]
            item.append(band)
            item.append(album)
            item.append(vinyl)
        elif '-' in albuminfo:
            band = re.findall(r'(.*?)-.*'+vinylTypes, albuminfo)[0]
            album = re.findall(r'.*?-(.*)'+vinylTypes, albuminfo)[0]
            vinyl = re.findall(vinylTypes, albuminfo)[0]
            item.append(band)
            item.append(album)
            item.append(vinyl)
        elif 'S/T' in albuminfo:
            band = re.findall(r'(.*?)S/T.*'+vinylTypes, albuminfo)[0]
            album = "S/T"
            vinyl = re.findall(vinylTypes, albuminfo)[0]
            item.append(band)
            item.append(album)
            item.append(vinyl)
        else:
            try:
                band = re.findall(r'(.*?)"', albuminfo)[0]
                album = re.findall(r'"(.*?)"', albuminfo)[0]
                vinyl = re.findall(vinylTypes, albuminfo)[0]
                item.append(band)
                item.append(album)
                item.append(vinyl)
            except:
                toDelete.append(item)

    items = [item for item in items if len(item) > 0 and item not in toDelete]

    finalList = []

    for part in items:
        if "label-soldout" in part[1]:
            print "ignoring " + item[-3] + " because its sold out"
        elif len(part[0]) == 0 or part[5] == "1":
            del part
        else:
            # change apostrophe code into actual apostrophes and
            # convert prices and vinyl size into floats and ints
            tmpContainer = []
            # Change links to full links by appending baseAddr
            tmpContainer.append(baseAddr + part[0])
            tmpContainer.append(part[1])
            # Change prices to floats
            try:
                tmpContainer.append(float(part[2]))
            except:
                print "price conversion fucked up"
                print part
                print "\n\n\n\n\n"
            try:
                tmpContainer.append(part[3])
            except:
                "name conversion"
                print part
            try:
                tmpContainer.append(part[4])
            except:
                print "title conversion"
                print part
                print "\n\n\n\n\n"
            # Change sizes to ints
            if part[5].lower() in "lpmlp12" or part[5] == "12":
                tmpContainer.append(12)
            else:
                try:
                    tmpContainer.append(7)
                except ValueError:
                    print "size conversion fucked up"
                    print part
                    print "\n\n\n\n\n"

            tmpContainer.append(siteName)
            finalList.append(tmpContainer)

    for item in finalList:
        print item

    finalList = hackedListToDict(finalList)
    return (finalList, "CVRECS")

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
            pageData = ""
            try:
                #print "Thread waiting for: " + addr
                pageData = urllib2.urlopen(addr)
            except IOError:
                print "Unable to open: " + addr
            self.queueB.put(pageData)
            self.queueA.task_done()

if __name__ == "__main__":
    getItems()
