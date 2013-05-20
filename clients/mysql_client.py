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

    # mysql specific
    c_server.commit()
    c_server.close()

    return data_list, tables

# !! TODO MOVE THIS PART BELOW OUT OF HERE
def connect_server(server_dict):
    # connect to the hemlock server
    # required fields in the server creds file are as follows:
    #    HEMLOCK_SERVER
    #    HEMLOCK_PW 
    h_server = ""
    try:
        h_server = Couchbase(server_dict['HEMLOCK_SERVER'],
                             "hemlock", 
                             server_dict['HEMLOCK_PW'])
    except:
        print "Failure connecting to the Hemlock server"
        sys.exit(0)
    return h_server

def send_data(data_list, tables):
    # !! TODO
    j = 0
    for table_data in data_list:
        print tables[j][0]
        i = 0
        for record in table_data:
            i += 1
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
    data_list, tables = get_data(client_dict, c_server)
    h_server = connect_server(server_dict)
    send_data(data_list, tables)
    update_hemlock()
    print "Took",time.time() - start_time,"seconds to complete."
