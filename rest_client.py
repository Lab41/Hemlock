#!/usr/bin/python

import requests, json

couch_url = "http://l41-vsrv-cbase1.b.internal:8091/pools/default"
#data = json.dumps({'name':'test', 'description':'some test data'}) 
r = requests.get(couch_url)
print r.status_code
print r.headers['content-type']
print r.encoding
print r.text

print r.json
j = json.loads(r.text)
print j['storageTotals']
