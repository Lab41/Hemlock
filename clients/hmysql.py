#!/usr/bin/python

import sys
import MySQLdb as mdb

class HMysql:
    def connect_client(self, client_dict):
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

    def get_data(self, client_dict, c_server, h_server, client_uuid):
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
        
        try:
            c_server.commit()
            c_server.close()
        except:
            print "Failed to close MySQL connection."

        return data_list, desc_list
