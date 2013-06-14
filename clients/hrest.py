#!/usr/bin/python

import json, requests, sys

class HRest:
    def connect_client(self, client_dict):
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
        auth_url = client_dict['REST_AUTH_URL']
        auth_params = {client_dict['REST_USERNAME_FIELD']:client_dict['REST_USERNAME'],client_dict['REST_PW_FIELD']:client_dict['REST_PW']}
        r = ""
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

    def get_data(self, client_dict, c_server, h_server, client_uuid):
        data_list = [[]]
        desc_list = []

        data_url = client_dict['REST_DATA_URL']
        data_params = {client_dict['REST_AUTH_FIELD']:c_server}
        r = ""
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
