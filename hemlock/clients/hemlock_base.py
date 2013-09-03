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

from multiprocessing import Pool
from socket import *
from hemlock_debugger import Hemlock_Debugger

import ast
import couchbase
import datetime
import hashlib
import MySQLdb as mdb
import sys
import time

class Hemlock_Base():
    def __init__(self):
        self.log = Hemlock_Debugger()
        self.SERVER_CREDS_FILE = '../hemlock_creds'

    def client_import(self, debug, client):
        self.log.debug(debug, "Importing: h"+client)
        exec "import h"+client

        cmd = "h"+client+".H"+client.title()+"()"
        self.log.debug(debug, "Initializing: "+cmd)

        c_inst = eval(cmd)
        self.log.debug(debug, "Client handle: "+str(c_inst))
        return client+'_creds', c_inst

    def get_creds(self, debug, CLIENT_CREDS_FILE):
        client_dict = {}
        server_dict = {}

        # read in client creds file
        try:
            self.log.debug(debug, "Opening client_creds file: "+CLIENT_CREDS_FILE)
            f = open(CLIENT_CREDS_FILE, 'r')
            self.log.debug(debug, "Client creds file handle: "+str(f))
            for line in f:
                self.log.debug(debug, line)
                if len(line) > 0 and line[0] != "#" and "=" in line:
                    # split each line on the first '='
                    line = line.split("=",1)
                    try:
                        client_dict[line[0]] = line[1].strip()
                    except:
                        print "Malformed Client Creds file."
                        self.log.debug(debug, str(sys.exc_info()[0]))
                        sys.exit(0)
            f.close()
        except:
            print "Unable to open "+CLIENT_CREDS_FILE
            self.log.debug(debug, str(sys.exc_info()[0]))
            sys.exit(0)

        # read in hemlock server creds file
        try:
            self.log.debug(debug, "Opening server_creds file: "+self.SERVER_CREDS_FILE)
            f = open(self.SERVER_CREDS_FILE, 'r')
            self.log.debug(debug, "Server creds file handle: "+str(f))
            for line in f:
                self.log.debug(debug, line)
                if len(line) > 0 and line[0] != "#" and "=" in line:
                    # split each line on the first '='
                    line = line.split("=",1)
                    try:
                        server_dict[line[0]] = line[1].strip()
                    except:
                        print "Malformed Server Creds file."
                        self.log.debug(debug, str(sys.exc_info()[0]))
                        sys.exit(0)
            f.close()
        except:
            print "Unable to open "+self.SERVER_CREDS_FILE
            self.log.debug(debug, str(sys.exc_info()[0]))
            sys.exit(0)
        return client_dict, server_dict

    def verify_system(self, debug, client_uuid, server_dict):
        # verify the client system is registered
        # required fields in the server creds file are as follows:
        #    HEMLOCK_MYSQL_SERVER
        #    HEMLOCK_MYSQL_USERNAME
        #    HEMLOCK_MYSQL_PW
        try:
            h_server = mdb.connect(server_dict['HEMLOCK_MYSQL_SERVER'],
                                   server_dict['HEMLOCK_MYSQL_USERNAME'],
                                   server_dict['HEMLOCK_MYSQL_PW'],
                                   "hemlock")
            self.log.debug(debug, "MySQL connection handle: "+str(h_server))
            cur = h_server.cursor()
            self.log.debug(debug, "MySQL cursor handle: "+str(cur))
            query = "SELECT * from systems WHERE uuid='"+client_uuid+"'"
            self.log.debug(debug, "Executing mysql query: "+query)
            a = cur.execute(query)
            if a == 0:
                print client_uuid,"is not a valid system."
                sys.exit(0)
            h_server.commit()
            h_server.close()
            self.log.debug(debug, "Successfully closed the mysql connection.")
        except:
            print "Failure connecting to the Hemlock server"
            self.log.debug(debug, str(sys.exc_info()[0]))
            sys.exit(0)
        return

    def connect_server(self, debug, server_dict):
        # connect to the hemlock server
        # required fields in the server creds file are as follows:
        #    HEMLOCK_COUCHBASE_SERVER
        #    HEMLOCK_COUCHBASE_BUCKET
        #    HEMLOCK_COUCHBASE_USERNAME
        #    HEMLOCK_COUCHBASE_PW
        h_server = ""
        try:
            h_server = couchbase.Couchbase.connect(host=server_dict['HEMLOCK_COUCHBASE_SERVER'],
                                 bucket=server_dict['HEMLOCK_COUCHBASE_BUCKET'],
                                 username=server_dict['HEMLOCK_COUCHBASE_USERNAME'],
                                 password=server_dict['HEMLOCK_COUCHBASE_PW'])
            self.log.debug(debug, "Couchbase connection handle: "+str(h_server))
        except:
            print "Failure connecting to the Hemlock server"
            self.log.debug(debug, str(sys.exc_info()[0]))
            sys.exit(0)
        return h_server

    def send_data(self, debug, data_list, desc_list, h_server, client_uuid):
        j_dict = {}
        j = 0
        i = 0
        e = 0
        # DEBUG
        for table_data in data_list:
            t_dict = {}
            for record in table_data:
                j_dict = {}
                k = 0
                while k < len(record):
                    rec = record[k]
                    if type(rec) == datetime.datetime:
                        rec = str(rec)
                    j_dict[desc_list[j][k][0]] = rec
                    k += 1
                uid = hashlib.sha1(repr(sorted(j_dict.items())))
                j_dict['hemlock-system'] = client_uuid
                j_dict['hemlock-date'] = time.strftime('%Y-%m-%d %H:%M:%S')
                t_dict[uid.hexdigest()] = j_dict
                # requires couchbase 1.0 client
                # !! TODO this should a parameter, not hardcoded
                if len(t_dict) > 250000:
                    try:
                        h_server.set_multi(t_dict, format=couchbase.FMT_JSON)
                    except:
                        print "Failure."
                    t_dict = {}
                #try:
                #    h_server.set(uid.hexdigest(), j_dict, format=couchbase.FMT_JSON)
                #except:
                #    print "Failed to send record."
                #    e += 1
                i += 1
            # requires couchbase 1.0 client
            if t_dict:
                try:
                    h_server.set_multi(t_dict, format=couchbase.FMT_JSON)
                except:
                    print "Failure."
            j += 1
        # DEBUG
        print i,"records"
        print e,"errors"
        return

    def update_hemlock(self, debug, client_uuid, server_dict):
        # update mysql record to say when data was last updated for this system
        # DEBUG
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

    def stream_callback(self, data):
        print data

    def stream_workers(self, debug):
        # DEBUG
        objects= [0] * 10
        pool = Pool(processes=4)
        for obj in objects:
            pool.apply_async(call_worker, callback=self.stream_callback) 
        pool.close()
        pool.join()
        #    #Hemlock_Base().send_data(data_list, desc_list, h_server, client_uuid)
        #    #Hemlock_Base().update_hemlock(client_uuid, server_dict)

    def print_help(self):
        print "--uuid \t<uuid of system> (use 'system-list' on the Hemlock server)"
        print "--client \t <name of client> (client file must exist in the clients folder)"
        print "-h \thelp\n"
        sys.exit(0)

    def process_args(self, debug, args):
        # process args
        splits = -1
        client = None
        client_uuid = None
        i = 0
        # DEBUG
        if not args:
            self.print_help()
        while i < len(args):
            if args[i] == "--uuid":
                try:
                    client_uuid = args[i+1]
                    i += 1
                except:
                    self.print_help()
            elif args[i] == "--client":
                try:
                    client = args[i+1]
                    i += 1
                except:
                    self.print_help()
            elif args[i] == "--splits":
                try:
                    splits = args[i+1]
                    i += 1
                except:
                    splits = -1
            else:
                self.print_help()
            i += 1
        if not client or not client_uuid:
            self.print_help()

        return client_uuid, client, splits

    def get_args(self, debug):
        # DEBUG
        args = []
        for arg in sys.argv:
            args.append(arg)
        return args[1:]

if __name__ == "__main__":
    start_time = time.time()
    hemlock = Hemlock_Base()
    debug = 0
    args = hemlock.get_args(debug)
    client_uuid, client, splits = hemlock.process_args(debug, args)
    CLIENT_CREDS_FILE, c_inst = hemlock.client_import(debug, client)
    client_dict, server_dict = hemlock.get_creds(debug, CLIENT_CREDS_FILE)
    global c_server
    c_server = c_inst.connect_client(debug, client_dict)
    data_list = []
    desc_list = []
    h_server = hemlock.connect_server(debug, server_dict)
    hemlock.verify_system(debug, client_uuid, server_dict)
    # DEBUG
    if not client.startswith("stream"):
        data_list, desc_list = c_inst.get_data(debug, client_dict, c_server, h_server, client_uuid)
    else:
        hemlock.stream_workers(debug)
    hemlock.send_data(debug, data_list, desc_list, h_server, client_uuid)
    hemlock.update_hemlock(debug, client_uuid, server_dict)
    print "Took",time.time() - start_time,"seconds to complete."
