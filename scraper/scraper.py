# TODO: Handle combining data from multiple websites before
#	 	passing it on to the database

import havoc
import lavida
import database
import shutil
import os

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__)) + '/../'

#os.path.join(PROJECT_DIR,'database/test.db')

dbPath = os.path.join(PROJECT_DIR, 'database/')
# Change this to use actual db or test db
dbName = 'test.db'

# Individual grabs allow us to inspect each scraper's results
havocItems = havoc.getItems()
laVidaItems = lavida.getItems()


items = havocItems + laVidaItems

# back up existing database before we move the existing one over
shutil.copyfile(dbPath + dbName, dbPath + "backup-" + dbName)

# ultimately, putItems should take all of the records as one so
# they are in the same database.
database.putItems(items, dbPath + dbName)

