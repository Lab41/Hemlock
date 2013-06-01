#!/usr/bin/python

import base64, fnmatch, json, magic, os, sys, time, uuid
from couchbase.client import Couchbase

# process pdfs
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO

# process word

# process excel

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

def process_files(input):
    matches = []
    for root, dirnames, filenames in os.walk(input):
        for filename in fnmatch.filter(filenames, '*.*'):
            matches.append(os.path.join(root, filename))
    i = 0
    j_dict = []
    for file in matches:
        print file
        file_mime = magic.from_file(file, mime=True)
        f = open(file, 'rb')
        try:
            # if file is text
            j_str = json.dumps( { "payload": f.read() } )
            print "worked, text"
        except:
            # !! TODO if file is csv/xls
            # !! TODO if file is xml
            # !! TODO if file is json
            # !! TODO if file is pdf
            if file_mime:
                if "pdf" in file_mime:
                    try:
                        text = convert_pdf(file)
                        j_str = json.dumps( { "payload" : text } )
                    except:
                        b64_text = base64.b64encode(f.read())
                        j_str = json.dumps( { "payload": b64_text } )
                
                # !! TODO if file has text - doc, etc.
                else:
                    b64_text = base64.b64encode(f.read())
                    j_str = json.dumps( { "payload": b64_text } )
                    print "failed, binary"
                j_dict.append(j_str)
        f.close()
        i += 1
    print i,"documents."
    #print j_dict

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
def send_data(data_list, desc_list, h_server, h_bucket, client_dict, client_uuid):
    j_dict = {}
    j = 0
    for table_data in data_list:
        i = 0
        for record in table_data:
            j_dict = {}
            k = 0
            while k < len(record):
                j_dict[desc_list[j][k][0]] = record[k]
                k += 1
            uid = hashlib.sha1(repr(sorted(j_dict.items())))
            j_dict['hemlock-system'] = client_uuid
            j_dict['hemlock-date'] = time.strftime('%Y-%m-%d %H:%M:%S')
            h_bucket.set(uid.hexdigest(), 0, 0, json.dumps(j_dict))
            i += 1
        print j_dict
        print i,"records"
        j += 1
    return

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
    process_files(input)
    update_hemlock(client_uuid, server_dict)
    print "Took",time.time() - start_time,"seconds to complete."
