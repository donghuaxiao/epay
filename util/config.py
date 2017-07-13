# -*- coding: utf-8 -*-


class PropertiesParser(object):

    def __init__(self):
        self._file_name = None
        self._props = None

    def read(self, file_name):
        self._file_name = file_name
        self._props = {}
        try:
            with open(self._file_name, 'r') as f:
                for line in f:
                    if line.startswith('#'): # comments
                        continue
                    items = line.strip().split('=')
                    self._props[items[0].strip()] = items[1].strip()
        except Exception as e:
            print e.message

    def get_property(self, name, default_value=None):
        if name in self._props:
            return self._props.get(name)
        else:
            return default_value

    def get_properties(self):
        return self._props

