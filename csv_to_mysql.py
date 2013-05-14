#!/usr/bin/python

import csv, getpass, sys, time
import MySQLdb as mdb

def get_auth():
    user = raw_input("Username:")
    pw = getpass.getpass("Password:")
    return user, pw

def mysql_server(server, user, pw, db):
    # connect to the mysql server
    try:
        m_server = mdb.connect(server, user, pw, db)
    except:
        print "MySQL server failure"
        sys.exit(0)
    return m_server

def process_csv(input, m_server, table):
    j = 0
    with open(input, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        hrow = reader.next()
        with m_server:
            cur = m_server.cursor()
            create_table = "CREATE TABLE IF NOT EXISTS `"+table+"`(Id INT PRIMARY KEY AUTO_INCREMENT, " 
            i = 0
            while i < len(hrow):
                create_table += "`"+hrow[i]+"` VARCHAR(200), "
                i += 1
            create_table = create_table[:-2]+")"
            cur.execute(create_table)
            for row in reader:
                data = "INSERT INTO `"+table+"`("
                i = 0
                while i < len(hrow):
                    data += "`"+hrow[i]+"`, " 
                    i += 1
                data = data[:-2]+") VALUES("
                i = 0
                while i < len(hrow):
                    data += "\""+row[i]+"\", "
                    i += 1
                data = data[:-2]+")"
                cur.execute(data)
                j += 1
    m_server.commit()
    m_server.close()
    print str(j), "keys added."

def print_help():
    print "-i \t<input file> (default is input.csv)"
    print "-s \t<mysql server> (default is localhost)"
    print "-d \t<database name> (default is test)"
    print "-t \t<table name> (default is table1)"
    print "-h \thelp\n"
    sys.exit(0)

def process_args(args):
    # default initialization
    input = "input.csv"
    server = "localhost"
    db = "test"
    table = "table1"
    
    # process args
    i = 0
    while i < len(args):
        if args[i] == "-s":
            try:
                server = args[i+1]
                i += 1
            except:
                print_help()
        elif args[i] == "-d":
            try:
                db = args[i+1]
                i += 1
            except:
                print_help()
        elif args[i] == "-t":
            try:
                table = args[i+1]
                i += 1
            except:
                print_help()
        elif args[i] == "-i":
            try:
                input = args[i+1]
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
    return input, server, db, table

def get_args():
    args = []
    for arg in sys.argv:
        args.append(arg)
    return args[1:]

if __name__ == "__main__":
    start_time = time.time()
    args = get_args()
    input, server, db, table = process_args(args)
    user, pw = get_auth()
    m_server = mysql_server(server, user, pw, db)
    process_csv(input, m_server, table)
    print "Took",time.time() - start_time,"seconds to complete."
