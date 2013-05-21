#!/usr/bin/python

import json, sys, time, uuid
from couchbase.client import Couchbase

import MySQLdb as mdb

CLIENT_CREDS_FILE='mysql_client_creds'
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
    # connect to the mysql server
    # required fields in the client creds file are as follows:
    #    MYSQL_SERVER
    #    MYSQL_DB
    #    MYSQL_USERNAME
    #    MYSQL_PW 
    # optional:
    #    MYSQL_TABLE (if not specified it will try all tables 
    #                 the credentials has access to)
    c_server = ""
    try:
        c_server = mdb.connect(client_dict['MYSQL_SERVER'], 
                               client_dict['MYSQL_USERNAME'], 
                               client_dict['MYSQL_PW'], 
                               client_dict['MYSQL_DB'])
    except:
        print "Failure connecting to the client server"
        sys.exit(0)
    return c_server

def get_data(client_dict, c_server):
    query_list = []
    data_list = []
    desc_list = []
    tables = ()
    cur = c_server.cursor()

    if "MYSQL_TABLE" in client_dict:
        # modify this line if you want to be more fine-grained
        # with what data is pulled from the table
        query = "SELECT * FROM "+client_dict['MYSQL_TABLE']
        query_list.append(query)
    else:
        cur.execute("SHOW TABLES")
        tables = cur.fetchall()
        for table in tables:
            # modify this line if you want to be more fine-grained
            # with what data is pulled from the tables
            query = "SELECT * FROM "+table[0]
            query_list.append(query)

    print query_list
    for query in query_list:
        cur.execute(query)
        data_list.append(cur.fetchall())

    if tables: 
        for table in tables:
            cur.execute("DESC "+table[0])
            desc_list.append(cur.fetchall())
    else:
        cur.execute("DESC "+client_dict['MYSQL_TABLE'])
        desc_list.append(cur.fetchall())
        
    # mysql specific
    c_server.commit()
    c_server.close()

    return data_list, tables, desc_list

# !! TODO MOVE THIS PART BELOW OUT OF HERE
def connect_server(server_dict):
    # connect to the hemlock server
    # required fields in the server creds file are as follows:
    #    HEMLOCK_SERVER
    #    HEMLOCK_PW 
    h_server = ""
    bucket = "hemlock"
    try:
        h_server = Couchbase(server_dict['HEMLOCK_SERVER'],
                             bucket, 
                             server_dict['HEMLOCK_PW'])
        h_bucket = h_server[bucket]
    except:
        print "Failure connecting to the Hemlock server"
        sys.exit(0)
    return h_server, h_bucket

def send_data(data_list, desc_list, tables, h_server, h_bucket, client_dict):
    # !! TODO
    j_dict = {}
    j = 0
    for table_data in data_list:
        if tables:
            print tables[j][0]
        else:
            print client_dict['MYSQL_TABLE']
        i = 0
        for record in table_data:
            j_dict = {}
            k = 0
            uid = str(uuid.uuid4())
            j_dict['hemlock-uuid'] = uid
            while k < len(record):
                try:
                    j_dict[desc_list[0][k][0]] = record[k]
                except:
                    print k
                    print desc_list
                    print record
                k += 1
            h_bucket.set(uid, 0, 0, json.dumps(j_dict))
            i += 1
        print j_dict
        print i,"records"
        j += 1
    return

def update_hemlock():
    # update mysql record to say when data was last updated for this system
    # !! TODO
    return

if __name__ == "__main__":
    start_time = time.time()
    client_dict, server_dict = get_creds()
    c_server = connect_client(client_dict)
    data_list, tables, desc_list = get_data(client_dict, c_server)
    h_server, h_bucket = connect_server(server_dict)
    send_data(data_list, desc_list, tables, h_server, h_bucket, client_dict)
    update_hemlock()
    print "Took",time.time() - start_time,"seconds to complete."
