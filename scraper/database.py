
import sqlite3 as lite
import sys

def putItems(itemData, dbpath):

    # connect to database
    con = lite.connect(dbpath)

    with con:
        # set the cursor and get version info
        cur = con.cursor()
        cur.execute('SELECT SQLITE_VERSION()')
        data = cur.fetchone()
        print "SQLite version: %s" % data

        # insert data
        cur.execute("DROP TABLE IF EXISTS Records")
        cur.execute("CREATE TABLE Records(Image TEXT, Band TEXT, Link TEXT, Album TEXT, Price REAL, Vinyl INT, Sitename TEXT)")

        for item in itemData:
            entry = [item['img'],
                     item['band'],
                     item['direct'],
                     item['album'],
                     item['price'],
                     item['size'],
                     item['site']
            ]
            cur.execute("INSERT INTO Records VALUES(?,?,?,?,?,?,?)", entry)
            # Add an Id field for a primary key
        cur.execute("ALTER TABLE Records ADD COLUMN Id")

