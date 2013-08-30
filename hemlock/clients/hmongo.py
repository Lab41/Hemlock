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
from pymongo import MongoClient

import sys

class HMongo:
    def __init__(self):
        self.log = Hemlock_Debugger()

    def connect_client(self, debug, client_dict):
        # connect to the mongo server
        # required fields in the client creds file are as follows:
        #    MONGO_SERVER
        #    MONGO_PORT
        #    MONGO_DB
        #    MONGO_COLLECTION
        c_server = ""
        # DEBUG
        try:
            c_server = MongoClient(client_dict['MONGO_SERVER'],
                                   int(client_dict['MONGO_PORT']))
            c_database = c_server[client_dict['MONGO_DB']]
            c_collection = c_database[client_dict['MONGO_COLLECTION']]
        except:
            print "Failure connecting to the client server"
            sys.exit(0)
        return c_collection

    def get_data(self, debug, client_dict, c_server, h_server, client_uuid):
        data_list = [[]]
        desc_list = []

        # DEBUG
        i = 0
        for record in c_server.find():
            data_list[0].append([])
            desc_list.append([])
            for key in record:
                data_list[0][i].append(str(record[key]))
                desc_list[i].append([str(key)])
            i += 1
        return data_list, desc_list
