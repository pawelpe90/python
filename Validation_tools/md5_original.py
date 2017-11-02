import os
import os.path
import ntpath
import sys
import hashlib
from cStringIO import StringIO

def md5_for_file(f, block_size=2**20):
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()

directory = sys.argv[1]
files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory,f))]
for f in files:
	md5 = md5_for_file(f)
	print("For file: {} MD5 equals: {}".format(os.path.abspath(f), md5))