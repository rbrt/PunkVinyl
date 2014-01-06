from recordlist.models import Records


def getId():
    rec = Records.objects.all()
    if len(rec) == 0:
        return 1
    return rec[len(rec) - 1].id + 1


def putItems(itemData):
    for item, label_name in itemData:
        print "label is %s and count is %d" % (label_name, len(item))
        existing_items = Records.objects.filter(sitename=label_name)
        to_delete = []
        # if a record is in the database and not in the new items,
        # remove from the database
        for record in existing_items:
            found = False
            for new_record in item:
                if record.album == new_record['album'] and record.band == new_record['band']:
                    found = True
                    break
            if not found:
                try:
                    to_delete.append(record)
                except AssertionError:
                    print "failed to delete %s %s" % (record.band, record.album)

        for i in range(len(to_delete)):
            to_delete[i].delete()

        # Add all new records to the database
        for record in item:
            if not existing_items.filter(band=record['band'], album=record['album']):
                print "adding %s %s" % (record['band'], record['album'])
                Records.objects.create(image=record['img'],
                                       band=record['band'],
                                       link=record['direct'],
                                       album=record['album'],
                                       price=record['price'],
                                       vinyl=record['size'],
                                       sitename=record['site'],
                                       id=getId()
                                       )
            else:
                # TODO: Make this update existing entries if anything has changed
                pass
