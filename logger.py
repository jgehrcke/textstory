# -*- coding: utf-8 -*-
# Copyright (c) 2015-2019 Jan-Philip Gehrcke. See LICENSE file for details.

from __future__ import unicode_literals
import logging


logging.basicConfig(
    format='%(asctime)s:%(msecs)05.1f  %(levelname)s: %(message)s',
    datefmt='%H:%M:%S')

log = logging.getLogger()
log.setLevel(logging.INFO)
