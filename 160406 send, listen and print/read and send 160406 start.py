#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 'read and send *date* *something*.py' - proof of concept python json
# communicator, client part, sends string, list, dict and int if intable
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
import socket
import Pyro4
import hashlib
Pyro4.config.reset()
Pyro4.config.HMAC_KEY = hashlib.sha224('some random text').hexdigest()  # anti-tamper
connectto = '127.0.0.1:9669'
timeout_value = 5  # seconds
socket.setdefaulttimeout(timeout_value)
# end import and prepare


# do the job
while True:
    inputdatum = raw_input('enter something: ')
    try:
        serverproxy = Pyro4.Proxy('PYRO:theserver@' + connectto)
        serverproxy.printdata(json.dumps(inputdatum, ensure_ascii=True))
        # test other types
        constructedlist = []
        for symbol in inputdatum:
            constructedlist.append(symbol)
        serverproxy.printdata(json.dumps(constructedlist, ensure_ascii=True))
        constructeddict = {}
        for i in range(len(inputdatum)/2):
            constructeddict[inputdatum[i]] = inputdatum[i+len(inputdatum)/2]
        serverproxy.printdata(json.dumps(constructeddict, ensure_ascii=True))
        try:
            serverproxy.printdata(json.dumps(int(inputdatum), ensure_ascii=True))
        except:
            pass
        # end test other types
    except (Pyro4.errors.CommunicationError, socket.timeout):
        raise LookupError("can't connect to server :(")
# end do the job
