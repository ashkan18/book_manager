__author__ = 'ashkan'


class BookModel(object):
    def __init__(self, data):
        self.first_name = data[0]
        self.last_name = data[1]
        self.title = data[2]
        self.date = data[3]

    def __unicode__(self):
        return "{}, {}, {}, {}".format(self.first_name, self.last_name, self.title, self.date)
