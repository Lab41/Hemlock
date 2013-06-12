#!/usr/bin/python

import redis, sys

class Redis:
    def connect_client(client_dict):
        # connect to the redis server
        # required fields in the client creds file are as follows:
        #    REDIS_SERVER
        c_server = ""
        try:
            c_server = redis.Redis(client_dict['REDIS_SERVER'])
        except:
            print "Failure connecting to the client server"
            sys.exit(0)
        return c_server

    def get_data(client_dict, c_server, h_server, h_bucket, client_uuid):
        data_list = [[]]
        desc_list = []

        keys = c_server.keys('*')

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
                if len(data_list[0]) % 10000 == 0:
                    send_data(data_list, desc_list, h_server, h_bucket, client_dict, client_uuid)
                    data_list = [[]]
                    desc_list = []
                    i = -1
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

        if desc_list:
            send_data(data_list, desc_list, h_server, h_bucket, client_dict, client_uuid)
        return
