import unittest
import logging
import shutil
import os

from pyPackage import Package, Options
from pyBaseApp import Configuration

class TestPackage(unittest.TestCase):

    def test_package(self):
     
        settings = Configuration().settings('tests/unit/resources/settings.yml')
        try:
            options = Options(settings)
            Package(options)
        except ValueError:
            logging.error('package value is missing in settings')

        self.assertTrue(os.path.exists(settings['distpath']))

    def test_package2(self):
        settings = Configuration().settings('tests/unit/resources/settings2.yml')
        data = settings['data'] if 'data' in settings else None
        try:
            options = Options(settings)
            Package(options, data)
        except ValueError:
            logging.error('package value is missing in settings')

        self.assertTrue(os.path.exists(settings['distpath']))
