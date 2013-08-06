#!/usr/bin/python

import sys
from socket import *

class HOdd:
    def connect_client(self, client_dict):
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

    def worker(self, connection, address, w_queue):
        data_list = [[]]
        desc_list = []
        print 'Server connected by', address
        while True:
            data = connection.recv(1024)
            if not data: break
            print address, "got data:", data
            connection.send(data)
        print 'Server disconnected by', address
        connection.close()
        w_queue.put("hi")

        #data_list[0][i].append(str(record_dict[k]))
        #desc_list[i].append([str(k)])

        #return data_list, desc_list
