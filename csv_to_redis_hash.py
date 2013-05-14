#!/usr/bin/python

import csv, redis, sys, time, uuid

def redis_server(server):
    # connect to the redis server
    try:
        r_server = redis.Redis(server)
    except:
        print "Redis server failure"
        sys.exit(0)
    return r_server

def process_csv(input, r_server):
    j = 0
    with open(input, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        hrow = reader.next()
        for row in reader:
            r_uuid = str(uuid.uuid4())
            i = 0
            while i < len(hrow):
                r_server.hset(r_uuid, hrow[i], row[i])
                i += 1
            #print "Added key: ",r_uuid
            j += 1
    print str(j), "keys added."

def print_help():
    print "-i \t<input file> (default is input.csv)"
    print "-s \t<redis server> (default is localhost)"
    print "-h \thelp\n"
    sys.exit(0)

def process_args(args):
    # default initialization
    input = "input.csv"
    server = "localhost"
    
    # process args
    i = 0
    while i < len(args):
        if args[i] == "-s":
            try:
                server = args[i+1]
                i += 1
            except:
                print_help()
        elif args[i] == "-i":
            try:
                input = args[i+1]
                i += 1
            except:
                print_help()
        else:
            print_help()
        i += 1
    try:
        f = open(input, 'r')
        f.close()
    except:
        print_help()
    return input, server

def get_args():
    args = []
    for arg in sys.argv:
        args.append(arg)
    return args[1:]

if __name__ == "__main__":
    start_time = time.time()
    args = get_args()
    input, server = process_args(args)
    r_server = redis_server(server)
    process_csv(input, r_server)
    print "Took",time.time() - start_time,"seconds to complete."
