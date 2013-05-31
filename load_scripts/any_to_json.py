#!/usr/bin/python

import fnmatch, magic, os, sys, time, uuid

def process_files(input):
    matches = []
    for root, dirnames, filenames in os.walk(input):
        for filename in fnmatch.filter(filenames, '*.*'):
            matches.append(os.path.join(root, filename))
    i = 0
    for file in matches:
        print file
        print magic.from_file(file, mime=True)
        # !! TODO if file is text/doc
        # !! TODO if file is csv/xls
        # !! TODO if file has text
        # !! TODO open file
        i += 1
    print i,"documents."

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

