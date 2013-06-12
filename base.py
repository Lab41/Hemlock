#!/usr/bin/python

import couchbase, hashlib, sys, time
import MySQLdb as mdb

SERVER_CREDS_FILE='hemlock_creds'

def client_import(client):
    exec "import clients."+client
    str = "clients."+client+"."+client.title()+"()"
    c_inst = eval(str)
    return client+'_creds', c_inst

def get_creds(CLIENT_CREDS_FILE):
    client_dict = {}
    server_dict = {}
    try:
        f = open('clients/'+CLIENT_CREDS_FILE, 'r')
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

def connect_server(server_dict):
    # connect to the hemlock server
    # required fields in the server creds file are as follows:
    #    HEMLOCK_COUCH_SERVER
    #    HEMLOCK__COUCH_PW
    h_server = ""
    h_bucket = "hemlock"
    try:
        h_server = couchbase.Couchbase.connect(host=server_dict['HEMLOCK_COUCH_SERVER'],
                             bucket=h_bucket,
                             password=server_dict['HEMLOCK_COUCH_PW'])
    except:
        print "Failure connecting to the Hemlock server"
        sys.exit(0)
    return h_server

def send_data(data_list, desc_list, h_server, client_dict, client_uuid):
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
            # !! TODO consider doing multiple set
            h_server.set(uid.hexdigest(), j_dict, format=couchbase.FMT_JSON)
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
    print "--client \t <name of client> (client file must exist in the clients folder)"
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
        elif args[i] == "--client":
            try:
                client = args[i+1]
                i += 1
            except:
                print_help()
        else:
            print_help()
        i += 1
    return client_uuid, client

def get_args():
    args = []
    for arg in sys.argv:
        args.append(arg)
    return args[1:]

if __name__ == "__main__":
    start_time = time.time()
    args = get_args()
    client_uuid, client = process_args(args)
    CLIENT_CREDS_FILE, c_inst = client_import(client)
    client_dict, server_dict = get_creds(CLIENT_CREDS_FILE)
    c_server = c_inst.connect_client(client_dict)
    h_server = connect_server(server_dict)
    verify_system(client_uuid)
    data_list, tables, desc_list = c_inst.get_data(client_dict, c_server)
    send_data(data_list, desc_list, h_server, client_dict, client_uuid)
    update_hemlock(client_uuid, server_dict)
    print "Took",time.time() - start_time,"seconds to complete."