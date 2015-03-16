# Introduction #

Logsup takes a file, encrypts it and uploads it to Amazon's S3 storage service. It also writes a "receipt" for that file in Amazon's SDB so you can have a bunch of details about it separate from the file (most of that info exists in metadata too). That's about it.

# Details #
```

wget http://python-gnupg.googlecode.com/files/python-gnupg-0.2.7.tar.gz

apt-get install python-boto
```

Obviously have Python installed

CONFIGURE GPG CONFIGURE GPG CONFIGURE GPG

^^HOPEFULLY THAT WAS CLEAR!?!?!

Nothing will work without GPG so, you know, CONFIGURE IT


move the logsup.conf file wherever you want to
edit logsup.conf to point to wherever you moved logsup.conf

```

### Configuration File for logsup

[DEFAULT]
#Who gets this file?
gpgRec = <gpg recipient>
#Sorry, need private key password :-( Know a better way to encrypt?
gpgPass = <gpg key password>

#Your aws access key
amaKey = <amazon access key>
#Your aws secret key (I know, it's not really secret if it's here but who is using your server you don't know about)
amaSec = <amazon secret key>
#The bucket you would like to use (defaults to logsup)
amaBucket = logsup
```

Edit logsup.conf to add your GPG / Amazon configurations

example usage:

logsup.py -f /var/log/syslog.1


You can add the above to a postrotate section in logrotate or you know cron or whatever

Enjoy!