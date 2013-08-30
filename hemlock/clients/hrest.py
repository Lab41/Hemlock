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

import json
import requests
import sys

class HRest:
    def __init__(self):
        self.log = Hemlock_Debugger()

    def connect_client(self, debug, client_dict):
        # connect to the rest server
        # required fields in the client creds file are as follows:
        #    REST_AUTH_URL
        #    REST_DATA_URL
        #    REST_USERNAME_FIELD
        #    REST_USERNAME
        #    REST_AUTH_TYPE
        #    REST_TOKEN_FIELD
        #    REST_DATA_TYPE
        #    REST_AUTH_FIELD
        #    REST_PW_FIELD
        #    REST_PW

        # DEBUG
        auth_url = client_dict['REST_AUTH_URL']
        auth_params = {client_dict['REST_USERNAME_FIELD']:client_dict['REST_USERNAME'],client_dict['REST_PW_FIELD']:client_dict['REST_PW']}
        r = ""
        # DEBUG
        try:
            if client_dict['REST_AUTH_TYPE'] == 'get':
                r = requests.get(auth_url, params=auth_params)
            elif client_dict['REST_AUTH_TYPE'] == 'post':
                r = requests.post(auth_url, params=auth_params)
            else:
                print "Unknown or unsupported REST_AUTH_TYPE."
                sys.exit(0) 
            req = json.loads(r.text)
            auth_token = req[client_dict['REST_TOKEN_FIELD']]
        except:
            print "Unable to get an auth token."
            sys.exit(0)
        return auth_token

    def get_data(self, debug, client_dict, c_server, h_server, client_uuid):
        data_list = [[]]
        desc_list = []

        # DEBUG
        data_url = client_dict['REST_DATA_URL']
        data_params = {client_dict['REST_AUTH_FIELD']:c_server}
        r = ""
        # DEBUG
        try:
            if client_dict['REST_DATA_TYPE'] == 'get':
                r = requests.get(data_url, params=data_params)
            elif client_dict['REST_DATA_TYPE'] == 'post':
                r = requests.post(data_url, params=data_params)
            else:
                print "Unknown or unsupported REST_AUTH_TYPE."
                sys.exit(0) 
            req = json.loads(r.text)
            i = k = 0
            while i < len(req):
                data_list[0].append([])
                desc_list.append([])
                record = req[i]
                for key in record:
                    data_list[0][k].append(record[key])
                    desc_list[k].append([key])
                i += 1
                k += 1
        except:
            print "Unable to get data from the server."
            sys.exit(0)

        return data_list, desc_list
