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

import file_types
from file_types import *
from hemlock_debugger import Hemlock_Debugger

import hemlock_base

import ast
import fnmatch
import magic
import os
import pkgutil
import sys
import time

class HFs:
    def __init__(self):
        self.log = Hemlock_Debugger()

    def connect_client(self, debug, client_dict):
        # DEBUG
        input = "/"
        try:
            input = client_dict['FILE_PATH']
        except:
            print "Failure with the creds file"
            sys.exit(0)
        return input

    def get_data(self, debug, client_dict, c_server, h_server, client_uuid):
        # DEBUG
        self.scan_file_types(debug, c_server, h_server, client_uuid)
        return [[]], []

    def format_lists(self, debug, j_list, h_server, client_uuid):
        # DEBUG
        data_list = [[]]
        desc_list = []
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
        h_inst = hemlock_base.Hemlock_Base()
        h_inst.send_data(debug, data_list, desc_list, h_server, client_uuid)
        return 

    def scan_file_types(self, debug, c_server, h_server, client_uuid):
        pkgpath = os.path.dirname(file_types.__file__)
        fs_mods = [name for _, name, _ in pkgutil.iter_modules([pkgpath])]

        file_type_list = {}
        for mod in fs_mods:
            exec "from file_types import "+mod
            cmd = mod+"."+mod.capitalize()+"()"
            c_inst = eval(cmd)
            file_type_list[mod] = c_inst
            #c_inst.process_files(debug, file, file_mime, h_server, client_uuid)

        # remove generic from the list
        fs_mods.remove("hgeneric")

        # DEBUG
        matches = []
        errors = 0
        for root, dirnames, filenames in os.walk(c_server):
            for filename in fnmatch.filter(filenames, '*.*'):
                matches.append(os.path.join(root, filename))
        i = 0
        # DEBUG
        for file in matches:
            file_mime = magic.from_file(file, mime=True)
            flag = 1
            for mod in fs_mods:
                if flag == 1:
                    try:
                        # try extensions first
                        if mod[1:] in file:
                            flag = 0
                            print file, mod
                            file_type_list[mod].process_files(debug, file, file_mime, h_server, client_uuid)
                        # if no extensions match, try mimetype
                        if file_mime and flag:
                            if mod[1:] in file_mime:
                                flag = 0
                                print file, mod
                                file_type_list[mod].process_files(debug, file, file_mime, h_server, client_uuid)
                    except:
                        print sys.exc_info()[0]
                        print file + " failed."
            if flag == 1:
                # if no mimetypes match, use generic
                junk = 1
                file_type_list["hgeneric"].process_files(debug, file, file_mime, h_server, client_uuid)
             
            i += 1
        print i
