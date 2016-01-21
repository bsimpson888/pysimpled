#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import logging.handlers
import os

import sys

__author__ = 'Marco Bartel'

class SimpleDaemonLogger(object):
    def __init__(self, logPath):
        self.logPath = logPath
        if not os.path.exists(os.path.dirname(self.logPath)):
            os.makedirs(os.path.dirname(self.logPath))

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        handler = logging.handlers.TimedRotatingFileHandler(self.logPath, when="midnight", backupCount=3)
        formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        class SimpleDaemonInnerLogger(object):
            def __init__(self, logger, level):
                """Needs a logger and a logger level."""
                self.logger = logger
                self.level = level

            def write(self, message):
                # Only log if there is a message (not just a new line)
                if message.rstrip() != "":
                    self.logger.log(self.level, message.rstrip())


        # Replace stdout with logging to file at INFO level
        sys.stdout = SimpleDaemonInnerLogger(logger, logging.INFO)
        # Replace stderr with logging to file at ERROR level
        sys.stderr = SimpleDaemonInnerLogger(logger, logging.ERROR)




class SimpleDaemon(object):
    debug = False

    def __init__(self, name):
        self.name = name
        self.pidFileName = "{name}.pid".format(name=self.name)

        self.pidPath = "/var/run/{fileName}".format(fileName=self.pidFileName)

        self.logFileName = "{name}.log".format(name=self.name)
        self.logPath = "/var/log/{fileName}".format(fileName=self.logFileName)

        if not self.debug:
            self.createLogger()

    def createLogger(self):
        self.logger = SimpleDaemonLogger(self.logPath)

    def __enter__(self):
        print "create pidfile..."

    def __exit__(self, type, value, traceback):
        print "delete pidfile"





if __name__ == '__main__':
    with SimpleDaemon("test") as daemon:
        print "running"


