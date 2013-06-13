#!/usr/bin/python

import base64, fnmatch, json, hashlib, magic, os, sys, time, uuid

# process pdfs
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO

# process xml
import xmltodict

# process powerpoint

# process word

# process excel
import xlrd

# process csv
import csv

class Hlocal_fs:
    def connect_client(self, client_dict):
        input = "/mnt/"
        try:
            input = client_dict['FILE_PATH']
        except:
            print "Failure with the creds file"
            sys.exit(0)
        return input

    def get_data(self, client_dict, c_server):
        j_list = process_files(c_server)
        # !! TODO fixed empty dictionary
        return j_list, {} 

    # !! TODO this needs to be updated
    def send_data(j_list, h_bucket, client_uuidi, errors):
        for record in j_list:
            if len(record) < 21000000:
                uid = hashlib.sha1(repr(record))
                while record[0] == '"' or record[0] == "'":
                    record = record.decode('unicode-escape')[1:-1]
                record = record[:-1]+",\"hemlock-system\":\""+client_uuid+"\","
                record += "\"hemlock-date\":\""+time.strftime('%Y-%m-%d %H:%M:%S')+"\"}"
                record = record.encode('ascii', 'ignore')
                try:
                    h_bucket.set(uid.hexdigest(), 0, 0, record)
                except:
                    errors += 1
                    print "couldn't insert record"
            else:
                errors += 1
                print "file was too big, didn't insert"
        return errors

    def process_files(input):
        matches = []
        errors = 0
        for root, dirnames, filenames in os.walk(input):
            for filename in fnmatch.filter(filenames, '*.*'):
                matches.append(os.path.join(root, filename))
        i = 0
        j_list = []
        for file in matches:
            print file
            file_mime = magic.from_file(file, mime=True)
            f = open(file, 'rb')
            try:
                if "csv" in file:
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
                                    i += 1
                    except:
                        f = open(file, 'rb')
                        j_str = json.dumps( { "payload": f.read() } )
                        j_list.append(j_str)
                        i += 1
                elif "xls" in file:
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
                                    i += 1
                    except:
                        b64_text = base64.b64encode(f.read())
                        j_str = json.dumps( { "payload": b64_text } )
                        j_list.append(j_str)
                        i += 1
                else:
                    j_str = json.dumps( { "payload": f.read() } )
                    j_list.append(j_str)
                    i += 1
            except:
                # !! TODO if file is xml
                # !! TODO if file is json
                # !! TODO if file is doc
                # !! TODO if file is ppt
                if file_mime:
                    if "pdf" in file_mime:
                        try:
                            text = convert_pdf(file)
                            j_str = json.dumps( { "payload" : text } )
                        except:
                            b64_text = base64.b64encode(f.read())
                            j_str = json.dumps( { "payload": b64_text } )
                    elif "text" in file_mime:
                        j_str = json.dumps( { "payload": repr(f.read()) } )
                    elif "pcap" in file_mime:
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
                    else:
                        #print file, file_mime
                        b64_text = base64.b64encode(f.read())
                        j_str = json.dumps( { "payload": b64_text } )
                    i += 1
                    j_list.append(j_str)
                else:
                    print file, "no mimetype"
            f.close()
        print errors,"errors."
        print i,"documents."
        return j_list

    def convert_pdf(input):
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

