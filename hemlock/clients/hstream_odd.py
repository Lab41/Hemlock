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

import ast
import json
import logging
import multiprocessing
import socket
import sys

def handle(debug, connection, address, h_server, client_uuid):
    h_inst = hemlock_base.Hemlock_Base()
    data_list = [[]]
    desc_list = []
    logging.basicConfig(filename='scheduler.log', level=logging.DEBUG)
    logger = logging.getLogger("process-%r" % (address,))
    try:
        logger.debug("Connected %r at %r", connection, address)
        while True:
            data = connection.recv(1024)
            if data == "":
                logger.debug("Socket closed remotely")
                break
            logger.debug("Received data %r", data)

            j_str = "{"
            j_str += "\"stream\":"
            j_str += "\""+data.strip()+"\"}"
            print j_str
            j_str = json.dumps(repr(j_str))
            j_list = []
            j_list.append(j_str)

            i = 0
            for record in j_list:
                data_list[0].append([])
                desc_list.append([])
                while record[0] == '"' or record[0] == "'":
                    record = record.decode('unicode-escape')[1:-1]
                record = record.encode('ascii', 'ignore')
                record = ast.literal_eval(record)
                for key in record:
                    data_list[0][i].append(str(record[key]))
                    desc_list[i].append([str(key)])
                i += 1
            # !! TODO
            #    should be this moved so that it doesn't send data
            #    for every piece recieved, will it be too slow?
            h_inst.send_data(debug, data_list, desc_list, h_server, client_uuid)
    except:
        logger.exception("Problem handling request")
    finally:
        logger.debug("Closing socket")
        connection.close()

class HStream_Odd:
    def __init__(self):
        self.log = Hemlock_Debugger()
        self.logger = logging.getLogger("server")

    def connect_client(self, debug, client_dict, h_server, client_uuid):
        # connect to the stream server
        # required fields in the client creds file are as follows:
        #    HOST
        #    PORT
        hostname = client_dict['HOST']
        port = int(client_dict['PORT'])

        logging.basicConfig(filename='scheduler.log', level=logging.DEBUG)
        try:
            logging.info("Listening")
            self.start(debug, hostname, port, h_server, client_uuid)
        except:
            logging.exception("Unexpected exception")
        finally:
            logging.info("Shutting down")
            for process in multiprocessing.active_children():
                logging.info("Shutting down process %r", process)
                process.terminate()
                process.join()
        logging.info("All done")

        return ""

    def start(self, debug, hostname, port, h_server, client_uuid):
        self.logger.debug("listening")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((hostname, port))
        self.socket.listen(1)

        while True:
            conn, address = self.socket.accept()
            self.logger.debug("Got connection")
            process = multiprocessing.Process(target=handle, args=(debug, conn, address, h_server, client_uuid))
            process.daemon = True
            process.start()
            self.logger.debug("Started process %r", process)
