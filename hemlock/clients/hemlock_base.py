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

import ast, couchbase, datetime, hashlib, sys, time
import MySQLdb as mdb
from multiprocessing import Pool
from socket import *

SERVER_CREDS_FILE='../hemlock_creds'

# has to be outside the class, since instance objects can't be pickled
def call_worker():
    connection, address = c_server.accept()
    d, data_list = c_inst.worker(connection, address)
    return d, data_list

class Hemlock_Base():
    def client_import(self, client):
        exec "import h"+client
        str = "h"+client+".H"+client.title()+"()"
        c_inst = eval(str)
        return client+'_creds', c_inst

    def get_creds(self, CLIENT_CREDS_FILE):
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

    def verify_system(self, client_uuid):
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

    def connect_server(self, server_dict):
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

    def send_data(self, data_list, desc_list, h_server, client_uuid):
        j_dict = {}
        j = 0
        i = 0
        e = 0
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
        print i,"records"
        print e,"errors"
        return

    def update_hemlock(self, client_uuid, server_dict):
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

    def stream_callback(self, data):
        print data

    def stream_workers(self):
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

    def process_args(self, args):
        # process args
        splits = -1
        client = None
        client_uuid = None
        i = 0
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

    def get_args(self):
        args = []
        for arg in sys.argv:
            args.append(arg)
        return args[1:]

if __name__ == "__main__":
    start_time = time.time()
    hemlock = Hemlock_Base()
    args = hemlock.get_args()
    client_uuid, client, splits = hemlock.process_args(args)
    CLIENT_CREDS_FILE, c_inst = hemlock.client_import(client)
    client_dict, server_dict = hemlock.get_creds(CLIENT_CREDS_FILE)
    global c_server
    c_server = c_inst.connect_client(client_dict)
    data_list = []
    desc_list = []
    h_server = hemlock.connect_server(server_dict)
    if not client.startswith("stream"):
        data_list, desc_list = c_inst.get_data(client_dict, c_server, h_server, client_uuid)
    else:
        hemlock.stream_workers()
    hemlock.verify_system(client_uuid)
    hemlock.send_data(data_list, desc_list, h_server, client_uuid)
    hemlock.update_hemlock(client_uuid, server_dict)
    print "Took",time.time() - start_time,"seconds to complete."
