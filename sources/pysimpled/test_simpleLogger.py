import os
from unittest import TestCase

import time

from sources.pysimpled.SimpleDaemon import SimpleLogger, SimplePid


class TestSimpleLogger(TestCase):
    def test_SimpleLogger(self):
        lockFilePath = '/tmp/test.lock'
        logFilePath = '/tmp/test.log'
        with SimpleLogger(logFilePath, both=True):
            with SimplePid(lockFilePath):
                self.assertTrue(os.path.exists(lockFilePath))
        self.assertTrue(not os.path.exists(lockFilePath))
