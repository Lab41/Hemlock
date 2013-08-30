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
import datetime
import MySQLdb as mdb
import sys
import time

class Hemlock_Runner():
    def __init__(self):
        self.log = Hemlock_Debugger()

    def mysql_server(self, debug, server, user, pw, db):
        # DEBUG
        # connect to the mysql server
        try:
            m_server = mdb.connect(server, user, pw, db)
        except:
            print "MySQL server failure"
            sys.exit(0)
        return m_server

    def get_creds(self, debug, m_server, cliend_id, aes_key):
        # DEBUG
        # get client_dict
        cur = m_server.cursor()
        data_action = "SELECT AES_DECRYPT(credentials, '"+aes_key+"') from clients where uuid = '"+cliend_id+"'"
        cur.execute(data_action)
        results = cur.fetchall()
        client_dict = ast.literal_eval(results[0][0])

        # DEBUG
        # get server_dict
        cur = m_server.cursor()
        data_action = "SELECT AES_DECRYPT(credentials, '"+aes_key+"') from hemlock_server"
        cur.execute(data_action)
        results = cur.fetchall()
        server_dict = ast.literal_eval(results[0][0])
        return client_dict, server_dict
