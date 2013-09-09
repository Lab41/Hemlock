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
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

import base64
import json

class Hpdf:
    def process_files(self, debug, file, file_mime, h_server, client_uuid):
        # !! TODO try/catch
        f = open(file, 'rb')
        h_inst = hfs.HFs()
        # DEBUG
        if file_mime:
            if "pdf" in file_mime:
                # DEBUG
                try:
                    text = self.convert_pdf(debug, file)
                    j_str = json.dumps( { "payload" : text } )
                except:
                    b64_text = base64.b64encode(f.read())
                    j_str = json.dumps( { "payload": b64_text } )
                j_list.append(j_str)
                h_inst.format_lists(debug, j_list, h_server, client_uuid)
                j_list = []


    def convert_pdf(self, debug, input):
        # DEBUG
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)

        fp = file(input, 'rb')
        process_pdf(rsrcmgr, device, fp)
        fp.close()
        device.close()

        str = retstr.getvalue()
        retstr.close()
        return str
