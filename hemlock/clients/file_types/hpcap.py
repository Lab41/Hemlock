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

class Hpcap:
    def process_files(self, debug, file, file_mime, h_server, client_uuid):
        # !! TODO try/catch
        f = open(file, 'rb')
        h_inst = hfs.HFs()
        # DEBUG
        if file_mime:
            if "pcap" in file_mime:
                # DEBUG
                try:
                    u = str(uuid.uuid4())
                    cmd = "tshark -r "+file+" -T text -V > "+u
                    junk = os.popen(cmd).read()
                    g = open(u, 'rb')
                    a = []
                    b = {}
                    for line in g:
                        if line == "\n":
                            # a frame
                            for element in a:
                                # DEBUG
                                try:
                                    e_list = element.split(":",1)
                                    b[e_list[0].strip()] = e_list[1].strip()
                                except:
                                    # ignore junk
                                    junk = element
                            j_str = json.dumps(b)
                            a = []
                            b = {}
                            j_list.append(j_str)
                            h_inst.format_lists(debug, j_list, h_server, client_uuid)
                            j_list = []
                        a.append(line)
                    g.close()
                    cmd = "rm -rf "+u
                    junk = os.popen(cmd).read()
                except:
                    if g:
                        g.close()
                        cmd = "rm -rf "+u
                        junk = os.popen(cmd).read()
                    print sys.exc_info()[0]
                    print "need tshark installed to process pcap files"
                    b64_text = base64.b64encode(f.read())
                    j_str = json.dumps( { "payload": b64_text } )
