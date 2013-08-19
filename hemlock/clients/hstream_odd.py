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

import sys
from socket import *

class HStream_Odd:
    def connect_client(self, client_dict):
        # connect to the stream server
        # required fields in the client creds file are as follows:
        #    HOST
        #    PORT
        c_server = ""
        host = client_dict['HOST']
        port = int(client_dict['PORT'])
        try:
            sockobj = socket(AF_INET, SOCK_STREAM)
            sockobj.bind((host, port))
            sockobj.listen(2)
            c_server = sockobj
        except:
            print "Failure connecting to the client server"
            sys.exit(0)
        return c_server

    def worker(self, connection, address):
        data_list = [[]]
        desc_list = []
        print connection, address
        print "start"
        d = ""
        while True:
            data = connection.recv(1024)
            if not data: break
            print address, "got data:", data
            d += data
        print 'Server disconnected by', address
        connection.close()

        print "end"
        return "did " + d, data_list

        # !! TODO actually store data in arrays
        #data_list[0][i].append(str(record_dict[k]))
        #desc_list[i].append([str(k)])

        #return data_list, desc_list
