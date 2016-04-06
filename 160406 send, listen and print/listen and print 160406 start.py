#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 'listen and print *date* *something*.py' - proof of concept python json
# communicator, server part
#
# Copyleft 2016 Urist McPirate <eorg.chaos@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.


# disclaimers:
# 1. i use Pyro version 4.11... iirc there was some change in later versions,
# should be easy to migrate
# 2. also used python 2.7.9, should be runnable as-is on 3


# import and prepare
import json
import Pyro4
import hashlib
Pyro4.config.reset()
Pyro4.config.HMAC_KEY = hashlib.sha224('some random text').hexdigest()  # anti-tamper
listentohost = '127.0.0.1'
listentoport = 9669
# end import and prepare


# do the job
class theserver(object):
    def printdata(self, thedata):
        pythonobj = json.loads(thedata)
        print(repr(pythonobj))

theserver=theserver()
daemon=Pyro4.Daemon(host=listentohost, port=listentoport)
uri=daemon.register(theserver, 'theserver')
daemon.requestLoop()
# end do the job
