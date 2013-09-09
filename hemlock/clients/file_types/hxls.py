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

from hemlock.clients import hfs

class Hxls:
    def process_files(self, debug, file, file_mime, h_server, client_uuid):
        # !! TODO try/catch
        f = open(file, 'rb')
        h_inst = hfs.HFs()
        # DEBUG
        try:
            wb = xlrd.open_workbook(file)
            wb_sn = wb.sheet_names()
            for sn in wb_sn:
                sh = wb.sheet_by_name(sn)
                j = 0
                header = []
                for rownum in xrange(sh.nrows):
                    j_str = "{"
                    if j == 0:
                        header = sh.row_values(rownum)
                    else:
                        row = sh.row_values(rownum)
                        k = 0
                        header2 = []
                        while k < len(header):
                            if header[k] != "":
                                if header[k] in header2:
                                    j_str += "\""+unicode(header[k])+str(k)+"\":\""+unicode(row[k])+"\","
                                else:
                                    j_str += "\""+unicode(header[k])+"\":\""+unicode(row[k])+"\","
                                header2.append(header[k])
                            else:
                                j_str += "\"empty-"+str(k)+"\":\""+unicode(row[k])+"\","
                            k += 1
                    j += 1
                    j_str = j_str[:-1]+"}"
                    if j_str != "}":
                        j_str = json.dumps(j_str)
                        j_list.append(j_str)
                        h_inst.format_lists(debug, j_list, h_server, client_uuid)
                        j_list = []
                        i += 1
        except:
            b64_text = base64.b64encode(f.read())
            j_str = json.dumps( { "payload": b64_text } )
            j_list.append(j_str)
            h_inst.format_lists(debug, j_list, h_server, client_uuid)
            j_list = []
            i += 1
