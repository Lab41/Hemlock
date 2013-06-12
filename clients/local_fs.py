#!/usr/bin/python

import base64, fnmatch, json, hashlib, magic, os, sys, time, uuid
from couchbase.client import Couchbase
import MySQLdb as mdb

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


SERVER_CREDS_FILE='hemlock_creds'

def get_creds():
    server_dict = {}
    try:
        f = open(SERVER_CREDS_FILE, 'r')
        for line in f:
            # split each line on the first '='
            line = line.split("=",1)
            try:
                server_dict[line[0]] = line[1].strip()
            except:
                print "Malformed Server Creds file."
                sys.exit(0)
        f.close()
    except:
        print "Unable to open "+SERVER_CREDS_FILE
        sys.exit(0)
    return server_dict

def verify_system(client_uuid):
    try:
        h_server = mdb.connect(server_dict['HEMLOCK_MYSQL_SERVER'],
                               server_dict['HEMLOCK_MYSQL_USERNAME'],
                               server_dict['HEMLOCK_MYSQL_PW'],
                               "hemlock")
        cur = h_server.cursor()
        query = "SELECT * from systems WHERE uuid='"+client_uuid+"'"
        a = cur.execute(query)
        if a == 0:
            print client_uuid,"is not a valid system."
            sys.exit(0)
        h_server.commit()
        h_server.close()
    except:
        print "Failure connecting to the Hemlock server"
        sys.exit(0)

    return

def process_files(input, client_uuid, h_bucket):
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
                                if len(j_list) > 1000:
                                    errors = send_data(j_list, h_bucket, client_uuid, errors)
                                    j_list = []
                                else:
                                    j_list.append(j_str)
                                i += 1
                except:
                    f = open(file, 'rb')
                    j_str = json.dumps( { "payload": f.read() } )
                    if len(j_list) > 1000:
                        errors = send_data(j_list, h_bucket, client_uuid, errors)
                        j_list = []
                    else:
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
                                if len(j_list) > 1000:
                                    errors = send_data(j_list, h_bucket, client_uuid, errors)
                                    j_list = []
                                else:
                                    j_list.append(j_str)
                                i += 1
                except:
                    b64_text = base64.b64encode(f.read())
                    j_str = json.dumps( { "payload": b64_text } )
                    if len(j_list) > 1000:
                        errors = send_data(j_list, h_bucket, client_uuid, errors)
                        j_list = []
                    else:
                        j_list.append(j_str)
                    i += 1
            else:
                j_str = json.dumps( { "payload": f.read() } )
                if len(j_list) > 1000:
                    errors = send_data(j_list, h_bucket, client_uuid, errors)
                    j_list = []
                else:
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
                                if len(j_list) > 1000:
                                    errors = send_data(j_list, h_bucket, client_uuid, errors)
                                    j_list = []
                                else:
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
                if len(j_list) > 1000:
                    errors = send_data(j_list, h_bucket, client_uuid, errors)
                    j_list = []
                else:
                    j_list.append(j_str)
            else:
                print file, "no mimetype"
        f.close()
    if j_list:
        errors = send_data(j_list, h_bucket, client_uuid, errors)
    print errors,"errors."
    print i,"documents."

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

def connect_server(server_dict):
    # connect to the hemlock server
    # required fields in the server creds file are as follows:
    #    HEMLOCK_SERVER
    #    HEMLOCK_PW
    h_server = ""
    bucket = "hemlock"
    try:
        h_server = Couchbase(server_dict['HEMLOCK_COUCH_SERVER'],
                             bucket,
                             server_dict['HEMLOCK_COUCH_PW'])
        h_bucket = h_server[bucket]
    except:
        print "Failure connecting to the Hemlock server"
        sys.exit(0)
    return h_server, h_bucket

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

def update_hemlock(client_uuid, server_dict):
    # update mysql record to say when data was last updated for this system
    try:
        h_server = mdb.connect(server_dict['HEMLOCK_MYSQL_SERVER'],
                               server_dict['HEMLOCK_MYSQL_USERNAME'],
                               server_dict['HEMLOCK_MYSQL_PW'],
                               "hemlock")
        cur = h_server.cursor()
        query = "UPDATE systems SET updated_data='"+time.strftime('%Y-%m-%d %H:%M:%S')+"' WHERE uuid='"+client_uuid+"'"
        cur.execute(query)
        h_server.commit()
        h_server.close()
    except:
        print "Failure connecting to the Hemlock server"
        sys.exit(0)

    return

def print_help():
    print "--uuid \t<uuid of system> (use 'system-list' on the Hemlock server)"
    print "-i \t<input path to files> (default is /mnt/)"
    print "-h \thelp\n"
    sys.exit(0)

def process_args(args):
    if not args:
        print_help()
    # default initialization
    input = "/mnt/"

    # process args
    i = 0
    while i < len(args):
        if args[i] == "-i":
            try:
                input = args[i+1]
                i += 1
            except:
                print_help()
        elif args[i] == "--uuid":
            try:
                client_uuid = args[i+1]
                i += 1
            except:
                print_help()
        else:
            print_help()
        i += 1
    return input, client_uuid

def get_args():
    args = []
    for arg in sys.argv:
        args.append(arg)
    return args[1:]

if __name__ == "__main__":
    start_time = time.time()
    args = get_args()
    input, client_uuid = process_args(args)
    server_dict = get_creds()
    h_server, h_bucket = connect_server(server_dict)
    verify_system(client_uuid)
    process_files(input, client_uuid, h_bucket)
    update_hemlock(client_uuid, server_dict)
    print "Took",time.time() - start_time,"seconds to complete."
