#!/usr/bin/python

import boto
import os

#This just creates the SDB library for you to write records to 

sdb = boto.connect_sdb('AMAZON_ACCESS_KEY', 'AMAZON_SECRET')
domain = sdb.create_domain('logsup')

item = domain.new_item('logsupTest')

item['sysinfo'] = os.uname()[1]
item.save()

for item in domain:
	print item.name, item['sysinfo']
