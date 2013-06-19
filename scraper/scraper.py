# TODO: Handle combining data from multiple websites before
#	 	passing it on to the database
import shutil
import os
from datetime import datetime

from django.core.mail import send_mail

import havoc
import lavida
import database

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__)) + '/../'
dbPath = os.path.join(PROJECT_DIR, 'database/')
dbName = 'test.db'


def get_records():
    # Individual grabs allow us to inspect each scraper's results
    print dbPath + dbName

    #havocItems = havoc.getItems()
    laVidaItems = lavida.getItems()

    check = [#havocItems,
             laVidaItems,]
    
    items = []

    for item in check:
        if not item[0]:
            send_error_mail(item[1])
        else:
            items += item[0]

    shutil.copyfile(dbPath + dbName, dbPath + "backup-" + dbName)
    database.putItems(items, dbPath + dbName)

def send_error_mail(distro_name):
    message = """
              Scrape from %s on %s returned zero results
              """ % (distro_name, str(datetime.now()))

    send_mail("Empty Scrape",
              message,
              "auto@recordsite.com",
              ['robbutler902@gmail.com']
             )