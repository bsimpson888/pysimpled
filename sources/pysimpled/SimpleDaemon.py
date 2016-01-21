#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import logging.handlers
import os

import sys

__author__ = 'Marco Bartel'

class SimpleDaemonException(Exception):
    def __init__(self, *args, **kwargs):
        super(SimpleDaemonException, self).__init__(*args, **kwargs)


class SimpleDaemonLogger(object):
    class SimpleDaemonInnerLogger(object):
        def __init__(self, logger, level):
            self.logger = logger
            self.level = level

        def write(self, message):
            # Only log if there is a message (not just a new line)
            if message.rstrip() != "":
                self.logger.log(self.level, message.rstrip())

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

        # Replace stdout with logging to file at INFO level
        sys.stdout = self.SimpleDaemonInnerLogger(logger, logging.INFO)
        # Replace stderr with logging to file at ERROR level
        sys.stderr = self.SimpleDaemonInnerLogger(logger, logging.ERROR)




class SimpleDaemon(object):
    debug = True

    @property
    def windows(self):
        return True if os.name == "nt" else False

    def __init__(self, name):
        self.name = name
        if self.windows:
            self.varPath = "c:\\temp"
        else:
            self.varPath = "/var"


        self.pidFileName = "{name}.pid".format(name=self.name)
        self.logFileName = "{name}.log".format(name=self.name)

        self.pidPath = os.path.join(self.varPath, "run", self.pidFileName)
        self.logPath = os.path.join(self.varPath, "log", self.logFileName)

        if self.debug:
            print "pidPath:", self.pidPath
            print "logPath:", self.logPath


        if not self.debug:
            self.logger = SimpleDaemonLogger(self.logPath)

    def __enter__(self):
        if os.path.isfile(self.pidPath):
            return False
        else:
            if not os.path.exists(os.path.dirname(self.pidPath)):
                os.makedirs(os.path.dirname(self.pidPath))

            pid = os.getpid()
            fd = open(self.pidPath, "w")
            fd.write(unicode(pid))
            fd.close()

        return self

    def __exit__(self, type, value, traceback):
        print "dlökjfldfkj"
        print type





if __name__ == '__main__':
    with SimpleDaemon("test") as daemon:
        print daemon
        print "running"


