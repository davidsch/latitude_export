import ConfigParser
import os
from os.path import expanduser, dirname, join, exists, realpath, isdir

class Settings(object):
    def __init__(self, config_file=None):
        if config_file is None:
            config_file = self.find_config()
        else:
            config_file = expanduser(config_file)
        self.reload(config_file)
        _debug = self.config.get('LatitudeExporter', 'debug').lower()
        self.DEBUG = _debug == 'true'
        self.setup()

    def reload(self, config_file):
        self.config = ConfigParser.ConfigParser()
        self.config.read(config_file)

    def find_config(self):
        files = ('latitude.ini', 'settings.ini')
        search = [
            os.getcwd(),
            expanduser('~'),
            join(expanduser('~'), '.config', 'latitude')]
        for s in search:
            for f in files:
                n = join(s, f)
                if not exists(n):
                    continue
                return n
        raise Exception('no configuration file found')

    def setup(self):
        # create datadir
        _datadir = self.config.get('LatitudeExporter', 'datadir')
        _datadir = expanduser(_datadir)
        if not exists(_datadir):
            os.makedirs(_datadir)
        assert isdir(_datadir)
        #self.config.set('LatitudeExporter', 'datadir', _datadir)
        self.datadir = _datadir

    def get(self, category, key):
        return self.config.get(category, key)

    def exporters(self):
        exporters = self.config.get('LatitudeExporter', 'exporters')
        exporters = [x.strip() for x in exporters.split(',')]
        return [__import__('latitude.exporter.%s' % e, {}, {}, ['exporter']).exporter
                                                for e in exporters]
    def formats(self):
        formats = self.config.get('LatitudeExporter', 'formats')
        formats = [x.strip() for x in formats.split(',')]
        return [__import__('latitude.data.%s' % f, {}, {}, ['format']).format
                                                for f in formats]

    def get_storage_path(self, storage):
        dirname = self.datadir
        storage_path = join(dirname, storage)
        return storage_path