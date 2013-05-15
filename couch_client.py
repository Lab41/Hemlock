#!/usr/bin/python

import getpass, json, sys, time, uuid
from couchbase.client import Couchbase

def get_auth():
    pw = getpass.getpass("Password:")
    return pw

def couch_server(server, bucket, pw):
    # connect to the couch server
    try:
        c_server = Couchbase(server, bucket, pw)
        c_bucket = c_server[bucket]
    except:
        print "Couch server failure"
        sys.exit(0)
    return c_server, c_bucket

def print_help():
    print "-b \t<bucket> (default is default)"
    print "-s \t<couch server uri> (default is localhost:8091)"
    print "-h \thelp\n"
    sys.exit(0)

def couch_operations(c_server, c_bucket):
    try:
        print c_bucket.get("357")[2]
    except:
        print "record not found in this bucket"
    new_rec = { "test":"foo"}
    id = str(uuid.uuid4())
    print id
    c_bucket.set(id, 0, 0, json.dumps(new_rec))
    
def process_args(args):
    # default initialization
    server = "localhost:8091"
    bucket = "default"

    # process args
    i = 0
    while i < len(args):
        if args[i] == "-s":
            try:
                server = args[i+1]
                i += 1
            except:
                print_help()
        elif args[i] == "-b":
            try:
                bucket = args[i+1]
                i += 1
            except:
                print_help()
        else:
            print_help()
        i += 1
    return server, bucket

def get_args():
    args = []
    for arg in sys.argv:
        args.append(arg)
    return args[1:]

if __name__ == "__main__":
    start_time = time.time()
    args = get_args()
    server, bucket = process_args(args)
    pw = get_auth()
    c_server, c_bucket = couch_server(server, bucket, pw)
    couch_operations(c_server, c_bucket)
    print "Took",time.time() - start_time,"seconds to complete."
