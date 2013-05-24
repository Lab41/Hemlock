#!/usr/bin/python

import hashlib, json, redis, sys, time
from couchbase.client import Couchbase

import MySQLdb as mdb

CLIENT_CREDS_FILE='redis_client_creds'
SERVER_CREDS_FILE='hemlock_creds'

def get_creds():
    client_dict = {}
    server_dict = {}
    try:
        f = open(CLIENT_CREDS_FILE, 'r')
        for line in f:
            # split each line on the first '='
            line = line.split("=",1)
            try:
                client_dict[line[0]] = line[1].strip()
            except:
                print "Malformed Client Creds file."
                sys.exit(0)
        f.close()
    except:
        print "Unable to open "+CLIENT_CREDS_FILE
        sys.exit(0)
    try:
        f = open(SERVER_CREDS_FILE, 'r')
        for line in f:
            # split each line on the first '='
            line = line.split("=",1)
            try:
                server_dict[line[0]] = line[1].strip()
            except:
                print "Malformed Server Creds file."
                sys.exit(0)
        f.close()
    except:
        print "Unable to open "+SERVER_CREDS_FILE
        sys.exit(0)
    return client_dict, server_dict

def connect_client(client_dict):
    # connect to the redis server
    # required fields in the client creds file are as follows:
    #    REDIS_SERVER
    c_server = ""
    try:
        c_server = redis.Redis(client_dict['REDIS_SERVER'])
    except:
        print "Failure connecting to the client server"
        sys.exit(0)
    return c_server

def get_data(client_dict, c_server, h_server, h_bucket, client_uuid):
    data_list = [[]]
    desc_list = []

    keys = c_server.keys('*')

    i = 0
    for key in keys:
        key_type = c_server.type(key)
        if key_type == "hash":
            data_list[0].append([])
            desc_list.append([])
            record_dict = c_server.hgetall(key)
            for k in record_dict:
                data_list[0][i].append(str(record_dict[k]))
                desc_list[i].append([str(k)])
            if len(data_list[0]) % 10000 == 0:
                send_data(data_list, desc_list, h_server, h_bucket, client_dict, client_uuid)
                data_list = [[]]
                desc_list = []
                i = -1
            i += 1
        elif key_type == "string":
            # !! TODO
            print "Unsupported object type."
        elif key_type == "list":
            # !! TODO
            print "Unsupported object type."
        elif key_type == "set":
            # !! TODO
            print "Unsupported object type."
        elif key_type == "zset":
            # !! TODO
            print "Unsupported object type."
        else:
            # ignore - shouldn't ever get here
            print "Key doesn't exist."

    if desc_list:
        send_data(data_list, desc_list, h_server, h_bucket, client_dict, client_uuid)
    return

# !! TODO MOVE THIS PART BELOW OUT OF HERE
def connect_server(server_dict):
    # connect to the hemlock server
    # required fields in the server creds file are as follows:
    #    HEMLOCK_SERVER
    #    HEMLOCK_PW 
    h_server = ""
    bucket = "hemlock"
    try:
        h_server = Couchbase(server_dict['HEMLOCK_COUCH_SERVER'],
                             bucket, 
                             server_dict['HEMLOCK_COUCH_PW'])
        h_bucket = h_server[bucket]
    except:
        print "Failure connecting to the Hemlock server"
        sys.exit(0)
    return h_server, h_bucket

def send_data(data_list, desc_list, h_server, h_bucket, client_dict, client_uuid):
    j_dict = {}
    j = 0
    for table_data in data_list:
        print desc_list[j]
        i = 0
        for record in table_data:
            j_dict = {}
            k = 0
            while k < len(record):
                j_dict[desc_list[j][k][0]] = record[k]
                k += 1
            uid = hashlib.sha1(repr(sorted(j_dict.items())))
            j_dict['hemlock-system'] = client_uuid
            h_bucket.set(uid.hexdigest(), 0, 0, json.dumps(j_dict))
            i += 1
        print j_dict
        print i,"records"
        j += 1
    return

def update_hemlock(client_uuid, server_dict):
    # update mysql record to say when data was last updated for this system
    try:
        h_server = mdb.connect(server_dict['HEMLOCK_MYSQL_SERVER'],
                               server_dict['HEMLOCK_MYSQL_USERNAME'],
                               server_dict['HEMLOCK_MYSQL_PW'],
                               "hemlock")
        cur = h_server.cursor()
        query = "UPDATE systems SET updated_data='"+time.strftime('%Y-%m-%d %H:%M:%S')+"' WHERE uuid='"+client_uuid+"'"
        cur.execute(query)
        h_server.commit()
        h_server.close()
    except:
        print "Failure connecting to the Hemlock server"
        sys.exit(0)

    return

def print_help():
    print "--uuid \t<uuid of system> (use 'system-list' on the Hemlock server)"
    print "-h \thelp\n"
    sys.exit(0)

def process_args(args):
    # process args
    i = 0
    if not args:
        print_help()
    while i < len(args):
        if args[i] == "--uuid":
            try:
                client_uuid = args[i+1]
                i += 1
            except:
                print_help()
        else:
            print_help()
        i += 1
    return client_uuid
   
def get_args():
    args = []
    for arg in sys.argv:
        args.append(arg)
    return args[1:]

if __name__ == "__main__":
    start_time = time.time()
    args = get_args()
    client_uuid = process_args(args)
    client_dict, server_dict = get_creds()
    c_server = connect_client(client_dict)
    h_server, h_bucket = connect_server(server_dict)
    get_data(client_dict, c_server, h_server, h_bucket, client_uuid)
    update_hemlock(client_uuid, server_dict)
    print "Took",time.time() - start_time,"seconds to complete."
