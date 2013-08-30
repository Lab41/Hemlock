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

import redis
import sys

class HRedis:
    def __init__(self):
        self.log = Hemlock_Debugger()

    def connect_client(self, debug, client_dict):
        # connect to the redis server
        # required fields in the client creds file are as follows:
        #    REDIS_SERVER
        c_server = ""
        # DEBUG
        try:
            c_server = redis.Redis(client_dict['REDIS_SERVER'])
        except:
            print "Failure connecting to the client server"
            sys.exit(0)
        return c_server

    def get_data(self, debug, client_dict, c_server, h_server, client_uuid):
        data_list = [[]]
        desc_list = []

        # DEBUG
        keys = c_server.keys('*')

        # DEBUG
        i = 0
        for key in keys:
            key_type = c_server.type(key)
            if key_type == "hash":
                data_list[0].append([])
                desc_list.append([])
                record_dict = c_server.hgetall(key)
                for k in record_dict:
                    data_list[0][i].append(str(record_dict[k]))
                    desc_list[i].append([str(k)])
                i += 1
            elif key_type == "string":
                # !! TODO
                print "Unsupported object type."
            elif key_type == "list":
                # !! TODO
                print "Unsupported object type."
            elif key_type == "set":
                # !! TODO
                print "Unsupported object type."
            elif key_type == "zset":
                # !! TODO
                print "Unsupported object type."
            else:
                # ignore - shouldn't ever get here
                print "Key doesn't exist."

        return data_list, desc_list
