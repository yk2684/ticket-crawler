import io
import os
import six
import csv

from scrapy.contrib.exporter import CsvItemExporter
from scrapy.extensions.feedexport import IFeedStorage
from w3lib.url import file_uri_to_path
from zope.interface import implementer


@implementer(IFeedStorage)
class FixedFileFeedStorage(object):

    def __init__(self, uri):
        self.path = file_uri_to_path(uri)

    def open(self, spider):
        dirname = os.path.dirname(self.path)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)
        return open(self.path, 'ab')

    def store(self, file):
        file.close()


class FixLineCsvItemExporter(CsvItemExporter):

    def __init__(self, file, include_headers_line=False, join_multivalued=',', **kwargs):
        super(FixLineCsvItemExporter, self).__init__(file, include_headers_line, join_multivalued, **kwargs)
        self._configure(kwargs, dont_fail=True)
        self.stream.close()
        storage = FixedFileFeedStorage(file.name)
        file = storage.open(file.name)
        self.stream = io.TextIOWrapper(
            file,
            line_buffering=False,
            write_through=True,
            encoding=self.encoding,
            newline="\n",
        ) if six.PY3 else file
        self.csv_writer = csv.writer(self.stream, **kwargs)