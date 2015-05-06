#!/usr/bin/python
from hashlib import md5
from boto.glacier.layer1 import Layer1
from boto.glacier.vault import Vault
from boto.glacier.concurrent import ConcurrentUploader
import sys
import os.path
from Crypto.Cipher import AES
import os, random, struct

def hashy(filey):
	infile = open(filey, 'r')
	hash = md5()
	while True:
    		data = infile.read(1024)
    		if data == '':
        		break
    		hash.update(data)
	infile.close()
	return hash.hexdigest()

def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    """ -- Stolen with some modifications --
	Encrypts a file using AES (CBC mode) with the
        given key.

        key:
            The encryption key - a string that must be
            either 16, 24 or 32 bytes long. Longer keys
            are more secure.

        in_filename:
            Name of the input file

        out_filename:
            If None, '<in_filename>.enc' will be used.

        chunksize:
            Sets the size of the chunk which the function
            uses to read and encrypt the file. Larger chunk
            sizes can be faster for some files and machines.
            chunksize must be divisible by 16.
    """
    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))

def glacierFreeze(amaKey, amaSec, fname, targetVault):
        g1 = Layer1(amaKey, amaSec)
        uploader = ConcurrentUploader(g1, targetVault, 32*1024*1024)
        archive_id = uploader.upload(fname, fname)
        return archive_id
