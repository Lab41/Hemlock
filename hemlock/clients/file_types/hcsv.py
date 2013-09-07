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

class Hcsv:
    def __init__(self):
        return
    def process_files(file):
        # DEBUG
        try:
            f.close()
            with open(file, 'rb') as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                hrow = reader.next()
                for row in reader:
                    j = 0
                    j_str = "{"
                    while j < len(hrow):
                        j_str += "\""+hrow[j]+"\":"
                        j_str += "\""+ row[j]+"\","
                        j += 1
                    j_str = j_str[:-1]+"}"
                    if j_str != "}":
                        j_str = json.dumps(repr(j_str))
                        j_list.append(j_str)
                        # !! TODO
                        # need to rework this line
                        self.format_lists(debug, j_list, h_server, client_uuid)
                        j_list = []
                        i += 1
        except:
            f = open(file, 'rb')
            j_str = json.dumps( { "payload": f.read() } )
            j_list.append(j_str)
            self.format_lists(debug, j_list, h_server, client_uuid)
            j_list = []
            i += 1
