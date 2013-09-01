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

import hemlock_base

import logging
import multiprocessing
import socket
import sys

def handle(connection, address):
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("process-%r" % (address,))
    try:
        logger.debug("Connected %r at %r", connection, address)
        while True:
            data = connection.recv(1024)
            if data == "":
                logger.debug("Socket closed remotely")
                break
            logger.debug("Received data %r", data)
            #connection.sendall(data)
            #logger.debug("Sent data")
    except:
        logger.exception("Problem handling request")
    finally:
        logger.debug("Closing socket")
        connection.close()

class HStream_Odd:
    def __init__(self):
        self.log = Hemlock_Debugger()
        self.logger = logging.getLogger("server")

    def start(self, hostname, port):
        self.logger.debug("listening")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((hostname, port))
        self.socket.listen(1)

        while True:
            conn, address = self.socket.accept()
            self.logger.debug("Got connection")
            process = multiprocessing.Process(target=handle, args=(conn, address))
            process.daemon = True
            process.start()
            self.logger.debug("Started process %r", process)

    def connect_client(self, debug, client_dict):
        # connect to the stream server
        # required fields in the client creds file are as follows:
        #    HOST
        #    PORT
        #c_server = ""
        hostname = client_dict['HOST']
        port = int(client_dict['PORT'])

        # !! TODO
        logging.basicConfig(level=logging.DEBUG)
        try:
            logging.info("Listening")
            self.start(hostname, port)
        except:
            logging.exception("Unexpected exception")
        finally:
            logging.info("Shutting down")
            for process in multiprocessing.active_children():
                logging.info("Shutting down process %r", process)
                process.terminate()
                process.join()
        logging.info("All done")

        # DEBUG
        #try:
        #    sockobj = socket(AF_INET, SOCK_STREAM)
        #    sockobj.bind((host, port))
        #    sockobj.listen(2)
        #    c_server = sockobj
        #except:
        #    print "Failure connecting to the client server"
        #    sys.exit(0)
        #return c_server

    def worker(self, debug, connection, address):
        data_list = [[]]
        desc_list = []
        print connection, address
        print "start"
        d = ""
        # DEBUG
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
