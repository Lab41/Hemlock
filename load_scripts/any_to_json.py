#!/usr/bin/python

import base64, fnmatch, json, magic, os, sys, time, uuid

# process pdfs
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO

# process word

# process excel

# process csv
import csv

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
    print j_dict

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

def print_help():
    print "-i \t<input path to files> (default is /mnt/)"
    print "-h \thelp\n"
    sys.exit(0)

def process_args(args):
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
        else:
            print_help()
        i += 1
    return input

def get_args():
    args = []
    for arg in sys.argv:
        args.append(arg)
    return args[1:]

if __name__ == "__main__":
    start_time = time.time()
    args = get_args()
    input = process_args(args)
    process_files(input)
    print "Took",time.time() - start_time,"seconds to complete."

