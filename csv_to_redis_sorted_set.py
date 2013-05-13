#!/usr/bin/python

import csv, sys, time

def output_file(ouput):
    fo = open(ouput, 'w')
    return fo

def process_csv(header, input, fo):
    with open(input, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        if header == 1:
            hrow = reader.next()
        for row in reader:
            print row


    print "header: ",hrow

def print_help():
    print "\n-nh \tno header (default is first line is header)"
    print "-i \t<input file> (default is input.csv)"
    print "-o \t<output file> (default is output.txt)"
    print "-h \thelp\n"
    sys.exit(0)

def process_args(args):
    # default initialization
    header = 1
    input = "input.csv"
    output = "output.txt"
    
    # process args
    i = 0
    while i < len(args):
        if args[i] == "-nh":
            header = 0
        elif args[i] == "-i":
            try:
                input = args[i+1]
                i += 1
            except:
                print_help()
        elif args[i] == "-o":
            try:
                output = args[i+1]
                f = open(output, 'w')
                f.close()
                i += 1
            except:
                print_help()
        else:
            print_help()
        i += 1
    try:
        f = open(input, 'r')
        f.close()
    except:
        print_help()
    return header, input, output

def get_args():
    args = []
    for arg in sys.argv:
        args.append(arg)
    return args[1:]

if __name__ == "__main__":
    start_time = time.time()
    args = get_args()
    header, input, output = process_args(args)
    fo = output_file(output)
    process_csv(header, input, fo)
    print "Took",time.time() - start_time,"seconds to complete."
