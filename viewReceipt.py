#!/usr/bin/python

import boto
import os

sdb = boto.connect_sdb('AMAZON_ACCESS_KEY', 'AMAZON_SECRET_KEY')
#domain = sdb.create_domain('logsup')
domain = sdb.get_domain('logsup')

item = domain.get_item('logsup-TODO.enc')

for item in domain:
	print item

