# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import csv, codecs, cStringIO
from parl.items import Subject, Speaker


class ParlPipeline(object):
    def process_item(self, item, spider):
        return item

class CSVWriter(object):

    def __init__(self):
        self.subjectWriter =  UnicodeWriter(open("subjects.csv", "wb"))
        self.speakersWriter =  UnicodeWriter(open("speakers.csv", "wb"))

    def process_item(self, item, spider):
        if item.__class__ == Subject:
            self.subjectWriter.writerow(item.values())
        else:
            self.speakersWriter.writerow(item.values())


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)