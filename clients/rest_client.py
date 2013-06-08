#!/usr/bin/python

import hashlib, json, requests, sys, time
from couchbase.client import Couchbase

import MySQLdb as mdb

CLIENT_CREDS_FILE='rest_client_creds'
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

def verify_system(client_uuid):
    try:
        h_server = mdb.connect(server_dict['HEMLOCK_MYSQL_SERVER'],
                               server_dict['HEMLOCK_MYSQL_USERNAME'],
                               server_dict['HEMLOCK_MYSQL_PW'],
                               "hemlock")
        cur = h_server.cursor()
        query = "SELECT * from systems WHERE uuid='"+client_uuid+"'"
        a = cur.execute(query)
        if a == 0:
            print client_uuid,"is not a valid system."
            sys.exit(0)
        h_server.commit()
        h_server.close()
    except:
        print "Failure connecting to the Hemlock server"
        sys.exit(0)

    return

def connect_client(client_dict):
    # connect to the rest server
    # required fields in the client creds file are as follows:
    #    REST_AUTH_URL
    #    REST_DATA_URL
    #    REST_USERNAME_FIELD
    #    REST_USERNAME
    #    REST_AUTH_TYPE
    #    REST_TOKEN_FIELD
    #    REST_DATA_TYPE
    #    REST_AUTH_FIELD
    #    REST_PW_FIELD
    #    REST_PW
    auth_url = client_dict['REST_AUTH_URL']
    auth_params = {client_dict['REST_USERNAME_FIELD']:client_dict['REST_USERNAME'],client_dict['REST_PW_FIELD']:client_dict['REST_PW']}
    r = ""
    try:
        if client_dict['REST_AUTH_TYPE'] == 'get':
            r = requests.get(auth_url, params=auth_params)
        elif client_dict['REST_AUTH_TYPE'] == 'post':
            r = requests.post(auth_url, params=auth_params)
        else:
            print "Unknown or unsupported REST_AUTH_TYPE."
            sys.exit(0) 
        req = json.loads(r.text)
        auth_token = req[client_dict['REST_TOKEN_FIELD']]
    except:
        print "Unable to get an auth token."
        sys.exit(0)
    return auth_token

def get_data(client_dict, auth_token, h_server, h_bucket, client_uuid):
    data_list = [[]]
    desc_list = []

    data_url = client_dict['REST_DATA_URL']
    data_params = {client_dict['REST_AUTH_FIELD']:auth_token}
    r = ""
    try:
        if client_dict['REST_DATA_TYPE'] == 'get':
            r = requests.get(data_url, params=data_params)
        elif client_dict['REST_DATA_TYPE'] == 'post':
            r = requests.post(data_url, params=data_params)
        else:
            print "Unknown or unsupported REST_AUTH_TYPE."
            sys.exit(0) 
        req = json.loads(r.text)
        i = k = 0
        while i < len(req):
            j = 0
            data_list[0].append([])
            desc_list.append([])
            record = req[i]
            for key in record:
                data_list[0][k].append(record[key])
                desc_list[k].append([key])
                j += 1
            if len(data_list[0]) % 1000 == 0:
                send_data(data_list, desc_list, h_server, h_bucket, client_dict, client_uuid)
                data_list = [[]]
                desc_list = []
                k = -1

            i += 1
            k += 1
    except:
        print "Unable to get data from the server."
        sys.exit(0)

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
        i = 0
        for record in table_data:
            j_dict = {}
            k = 0
            while k < len(record):
                j_dict[desc_list[j][k][0]] = record[k]
                k += 1
            uid = hashlib.sha1(repr(sorted(j_dict.items())))
            j_dict['hemlock-system'] = client_uuid
            j_dict['hemlock-date'] = time.strftime('%Y-%m-%d %H:%M:%S')
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
    if not args:
        print_help()
    i = 0
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
    auth_token = connect_client(client_dict)
    h_server, h_bucket = connect_server(server_dict)
    verify_system(client_uuid)
    get_data(client_dict, auth_token, h_server, h_bucket, client_uuid)
    update_hemlock(client_uuid, server_dict)
    print "Took",time.time() - start_time,"seconds to complete."
