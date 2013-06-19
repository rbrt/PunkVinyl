from recordlist.models import Records


def putItems(itemData):

    for item, label_name in itemData:
        existing_items = Records.objects.filter(sitename=label_name)
        # if a record is in the database and not in the new items,
        # remove from the database
        for record in existing_items:
            found = False
            for new_record in item:
                if record.album == new_record['album'] and record.band == new_record['band']:
                    found = True
                    break
            if not found:
                record.delete()

        # Add all new records to the database
        for record in item:
            if not existing_items.filter(band=record['band'], album=record['album']):
                Records.objects.create(image=record['img'],
                                       band=record['band'],
                                       link=record['direct'],
                                       album=record['album'],
                                       price=record['price'],
                                       vinyl=record['size'],
                                       sitename=record['site']
                                       )
            else:
                print "%s is a duplicate" % str(record)