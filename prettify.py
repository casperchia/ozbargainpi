#!/usr/bin/python

from byteify import byteify
import json


# Prints out the deals_data json file in an easy to read format

DEALS_DATA_DIR = "file location of deals_data"

f = open(DEALS_DATA_DIR, 'r')
data = json.load(f)
data = byteify(data)

for id in data:
	print id, data[id]['date'], "Votes:", data[id]['votes'], "Emailed:", data[id]['emailed'], data[id]['title']
