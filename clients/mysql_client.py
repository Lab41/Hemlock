#!/usr/bin/python

import json, sys, time, uuid
from couchbase.client import Couchbase

import MySQLdb as mdb

CLIENT_CREDS_FILE='mysql_client_creds'
SERVER_CREDS_FILE='hemlock_creds'

def get_creds():
    client_dict = {}
    f = open(CLIENT_CREDS_FILE, 'r')
    for line in f:
        # split each line on the first '='
        line = line.split("=",1)
        try:
            client_dict[line[0]] = line[1].strip()
        except:
            print "Malformed Client Creds file."
    return client_dict

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
    return c_server

def get_data(client_dict, c_server):
    data = ""
    cur = c_server.cursor()

    if "MYSQL_TABLE" in client_dict:
        print "table"
        # !! TODO
    else:
        cur.execute("SHOW TABLES")
        results = cur.fetchall()
        print results
        # !! TODO

    # mysql specific
    c_server.commit()
    c_server.close()

    return data

# !! TODO MOVE THIS PART BELOW OUT OF HERE
def connect_server():
    # !! TODO
    return

def send_data():
    # !! TODO
    return

def update_hemlock():
    # update mysql record to say when data was last updated for this system
    # !! TODO
    return

if __name__ == "__main__":
    start_time = time.time()
    client_dict = get_creds()
    c_server = connect_client(client_dict)
    data = get_data(client_dict, c_server)
    connect_server()
    send_data()
    update_hemlock()
    print "Took",time.time() - start_time,"seconds to complete."
