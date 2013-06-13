#!/usr/bin/python

import sys
from pymongo import MongoClient

class HMongo:
    def connect_client(self, client_dict):
        # connect to the mongo server
        # required fields in the client creds file are as follows:
        #    MONGO_SERVER
        #    MONGO_PORT
        #    MONGO_DB
        #    MONGO_COLLECTION
        c_server = ""
        try:
            c_server = MongoClient(client_dict['MONGO_SERVER'],
                                   int(client_dict['MONGO_PORT']))
            c_database = c_server[client_dict['MONGO_DB']]
            c_collection = c_database[client_dict['MONGO_COLLECTION']]
        except:
            print "Failure connecting to the client server"
            sys.exit(0)
        return c_collection

    def get_data(self, client_dict, c_server):
        data_list = [[]]
        desc_list = []

        i = 0
        for record in c_server.find():
            data_list[0].append([])
            desc_list.append([])
            for key in record:
                data_list[0][i].append(str(record[key]))
                desc_list[i].append([str(key)])
            i += 1
        return data_list, desc_list
