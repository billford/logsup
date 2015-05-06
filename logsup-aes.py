#!/usr/bin/python

import gzip
import boto
import ConfigParser
import io
import os
from hashlib import md5
from datetime import datetime
from optparse import OptionParser
from time import time
from logsuplib import hashy
from logsuplib import encrypt_file
from logsuplib import glacierFreeze

#### pull in some config variables to make this a little easier to use

config = ConfigParser.ConfigParser()
config.read ('/usr/local/src/logsup/logsup.conf') #Change this to wherever you have the config file at (*hopefully /etc/logsup?)

#you should have to change NOTHING below this line unless I'm a terrible person

#whoGets = config.get('DEFAULT', 'gpgRec')
#gpgCreds = config.get('DEFAULT','gpgPass')
amaAccess = config.get('DEFAULT','amaKey')
amaCreds = config.get('DEFAULT', 'amaSec')
amaKick = config.get('DEFAULT','amaBucket')
amaGlacier = config.get('DEFAULT', 'targetVault')

#Begin actual code (well as close I ever get to actual code anyway)
use = "Usage: %prog [-f] filename"
par = OptionParser(usage = use)
par.add_option("-f", "--filename", dest="filez", type="string", help="Specify path to a file to encrypt and cloudify")
(options, args) = par.parse_args()
if options.filez is None:
	par.error("Please specify a path to a file to encrypt")
elif options.filez is not None:
	fileUpload = options.filez
	preCompMD5sum = hashy(fileUpload)
	if os.path.isfile(fileUpload) == True:
			#compression
			file_in = open(fileUpload , 'rb')
			timeStuffs = str(time())
			fileLoaded = fileUpload + "." + timeStuffs + ".gz"
			file_out = gzip.open(fileLoaded, 'wb')
			file_out.writelines(file_in)
			file_out.close()
			file_in.close()
			preCryptMD5sum = hashy(fileLoaded)

			#Encryption
			encrypt_file('oq6af65}*fRhw=k<WTm,4{.x7CssW-w,', fileLoaded)
			fileExt = fileLoaded + ".enc"
			postCryptMD5Sum = hashy(fileLoaded + ".enc")

			supStatus = glacierFreeze(amaAccess, amaCreds, fileExt, amaGlacier)
			#IF we have an archive ID then submit meta info to SDB receipt
			if supStatus:
				sdb = boto.connect_sdb(amaAccess, amaCreds)
				domain = sdb.get_domain('logsup')
				item = domain.new_item('logsup-' + fileExt)
				item['timestamp'] = timeStuffs
				item['hostname'] = os.uname()[1]
				item['filename'] = fileExt
				item['preCompressionMD5sum'] = preCompMD5sum
				item['preEncryptionMD5sum'] = preCryptMD5sum
				item['postCryptMD5Sum'] = postCryptMD5Sum
				item['archiveID'] = supStatus
				item.save()
				os.remove(fileLoaded)
				os.remove(fileExt)
			else:
				print "Upload to Glacier Failed"
	else:
		print "File does not exist"
