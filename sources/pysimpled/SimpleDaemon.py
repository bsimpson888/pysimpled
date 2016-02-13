#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import logging.handlers
import os
import platform
import sys

__author__ = 'Marco Bartel'


class SimpleDaemonException(Exception):
    def __init__(self, *args, **kwargs):
        super(SimpleDaemonException, self).__init__(*args, **kwargs)


class SimpleLogger(object):
    class SimpleInnerLogger(object):
        def __init__(self, logger, level, both=False, oldstream=None):
            self.logger = logger
            self.level = level
            self.both = both
            self.oldstream = oldstream

        def write(self, message):
            # Only log if there is a message (not just a new line)
            if self.both:
                self.oldstream.write(message)

            if message.rstrip() != "":
                self.logger.log(self.level, message.rstrip())

    def __init__(self, logPath, both=False):

        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        self.both = both

        self.logPath = logPath

        if not os.path.exists(os.path.dirname(self.logPath)):
            os.makedirs(os.path.dirname(self.logPath))

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.handlers.TimedRotatingFileHandler(self.logPath, when="midnight", backupCount=3)
        formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def __enter__(self):
        sys.stderr = self.SimpleInnerLogger(self.logger, logging.ERROR, both=self.both, oldstream=sys.stderr)
        sys.stdout = self.SimpleInnerLogger(self.logger, logging.INFO, both=self.both, oldstream=sys.stdout)

    def __exit__(self, type, value, traceback):
        # time.sleep(1)
        if type is None:
            sys.stdout = self.old_stdout
            sys.stderr = self.old_stderr


class SimplePid(object):
    def __init__(self, pidPath):

        self._pid = os.getpid()

        self.pidPath = pidPath
        if not os.path.exists(os.path.dirname(self.pidPath)):
            os.makedirs(os.path.dirname(self.pidPath))

    def __enter__(self):
        self.checkPidFile()  # exit if exists
        self.createPidFile()  # create PID file
        return self

    def __exit__(self, type, value, traceback):
        self.removePidFile()

    def pid(self):
        return self._pid

    def createPidFile(self):
        if not os.path.exists(os.path.dirname(self.pidPath)):
            os.makedirs(os.path.dirname(self.pidPath))
        fd = open(self.pidPath, "w")
        fd.write(unicode(self.pid()))
        fd.close()

    def checkPidFile(self):
        if os.path.isfile(self.pidPath):
            print "PID File exists already. Exiting..."
            sys.exit()

    def removePidFile(self):
        if os.path.isfile(self.pidPath):
            os.remove(self.pidPath)


class SimpleDaemon(object):
    debug = False

    def isWindows(self):
        return True if platform.system().lower() == "windows" else False

    def __init__(self, name):
        self.name = name
        self._pid = os.getpid()

        self.varPath = "c:\\temp" if self.isWindows() else "/var"
        self.pidFileName = "{name}.pid".format(name=self.name)
        self.logFileName = "{name}.log".format(name=self.name)

        self.pidPath = os.path.join(self.varPath, "run", self.pidFileName)
        self.logPath = os.path.join(self.varPath, "log", self.logFileName)

        if self.debug:
            print "pidPath:", self.pidPath
            print "logPath:", self.logPath

        if not self.debug:
            self.logger = SimpleLogger(self.logPath)

    def pid(self):
        return self._pid

    def __enter__(self):
        self.checkPidFile()  # exit if exists
        self.createPidFile()  # create PID file
        return self

    def __exit__(self, type, value, traceback):
        self.removePidFile()

    def createPidFile(self):
        if not os.path.exists(os.path.dirname(self.pidPath)):
            os.makedirs(os.path.dirname(self.pidPath))
        fd = open(self.pidPath, "w")
        fd.write(unicode(self.pid()))
        fd.close()

    def checkPidFile(self):
        if os.path.isfile(self.pidPath):
            print "PID File exists already. Exiting..."
            sys.exit()

    def removePidFile(self):
        if os.path.isfile(self.pidPath):
            os.remove(self.pidPath)
