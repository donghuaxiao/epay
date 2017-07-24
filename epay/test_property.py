# -*- coding:utf-8 -*-

from util.config import PropertiesParser
import unittest


class TestProperties(unittest.TestCase):

    def setUp(self):
        self.props = PropertiesParser()

    def test_load_file(self):
        self.props.read('epay.cfg')
        db_props = self.props.get_properties()
        for (k, v) in db_props.iteritems():
            print "%s = %s" % (k, v)


if __name__ == '__main__':
    unittest.main()