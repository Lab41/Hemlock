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

import fnmatch, os, sys, time, uuid
from pymongo import MongoClient

def mongo_server(server, port, database, collection):
    # connect to the redis server
    try:
        m_server = MongoClient(server, port)
        m_database = m_server[database]
        m_collection = m_database[collection]
    except:
        print "Mongo server failure"
        sys.exit(0)
    return m_server, m_database, m_collection

def process_doc(input, m_server, m_database, m_collection):
    matches = []
    docs = []
    for root, dirnames, filenames in os.walk(input):
        for filename in fnmatch.filter(filenames, '*.txt'):
            matches.append(os.path.join(root, filename))
    j = 0
    k = 0
    for file in matches:
        if len(docs) % 100 == 0 and len(docs) > 0:
            m_collection.insert(docs)
            print str(j), "total docs."
            print str(k), "docs failed."
            docs = []

        doc = open(file, 'r').read()
        try:
            doc = unicode(doc, "utf-8")
            doc = {"doc": doc}
            docs.append(doc)
            j += 1
        except:
            k += 1
    if len(docs) > 0:
        m_collection.insert(docs)
    print str(j), "total docs."
    print str(k), "docs failed."

def print_help():
    print "-i \t<input path to files> (default is /mnt/)"
    print "-s \t<mongo server> (default is localhost)"
    print "-p \t<mongo port> (default is 27017)"
    print "-d \t<mongo database> (default is local)"
    print "-c \t<mongo collection> (default is collection)"
    print "-h \thelp\n"
    sys.exit(0)

def process_args(args):
    # default initialization
    input = "/mnt/"
    server = "localhost"
    port = 27017
    database = "local"
    collection = "collection"

    # process args
    i = 0
    while i < len(args):
        if args[i] == "-s":
            try:
                server = args[i+1]
                i += 1
            except:
                print_help()
        elif args[i] == "-p":
            try:
                port = int(args[i+1])
                i += 1
            except:
                print_help()
        elif args[i] == "-d":
            try:
                database = args[i+1]
                i += 1
            except:
                print_help()
        elif args[i] == "-c":
            try:
                collection = args[i+1]
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
    return input, server, port, database, collection

def get_args():
    args = []
    for arg in sys.argv:
        args.append(arg)
    return args[1:]

if __name__ == "__main__":
    start_time = time.time()
    args = get_args()
    input, server, port, database, collection = process_args(args)
    m_server, m_database, m_collection = mongo_server(server, port, database, collection)
    process_doc(input, m_server, m_database, m_collection)
    print "Took",time.time() - start_time,"seconds to complete."

