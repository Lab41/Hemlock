#!/usr/bin/env python
#
#   Copyright (c) 2013 In-Q-Tel, Inc/Lab41, All Rights Reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from hemlock_debugger import Hemlock_Debugger

import hemlock_base

import MySQLdb as mdb
import MySQLdb.cursors
import sys

class HMysql:
    def __init__(self):
        self.log = Hemlock_Debugger()

    def connect_client(self, debug, client_dict):
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
        # DEBUG
        try:
            c_server = mdb.connect(client_dict['MYSQL_SERVER'],
                                   client_dict['MYSQL_USERNAME'],
                                   client_dict['MYSQL_PW'],
                                   client_dict['MYSQL_DB'],
                                   cursorclass = MySQLdb.cursors.SSCursor)
        except:
            print "Failure connecting to the client server"
            sys.exit(0)
        return c_server

    def get_data(self, debug, client_dict, c_server, h_server, client_uuid):
        # DEBUG
        h_inst = hemlock_base.Hemlock_Base()
        query_list = []
        data_list = []
        desc_list = []
        tables = ()
        cur = c_server.cursor()

        # DEBUG
        if "MYSQL_TABLE" in client_dict:
            # modify this line if you want to be more fine-grained
            # with what data is pulled from the table
            query = "SELECT * FROM "+client_dict['MYSQL_TABLE']
            query_list.append(query)
        else:
            cur.execute("SHOW FULL TABLES WHERE Table_type = \"BASE TABLE\"")
            tables = cur.fetchall()
            for table in tables:
                # modify this line if you want to be more fine-grained
                # with what data is pulled from the tables
                query = "SELECT * FROM "+table[0]
                query_list.append(query)

        # DEBUG
        for query in query_list:
            table = query.split("FROM ")
            cur.execute("DESC "+table[1])
            desc_list.append(cur.fetchall())
            cur.execute(query)
            result = 1
            while result:
                result = cur.fetchmany(1000)
                data_list.append(result)
                h_inst.send_data(debug, data_list, desc_list, h_server, client_uuid)
                data_list = []
            desc_list = []

        # DEBUG
        try:
            c_server.commit()
            cur.close()
            c_server.close()
        except:
            print "Failed to close MySQL connection."

        return data_list, desc_list
