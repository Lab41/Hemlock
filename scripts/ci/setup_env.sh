#!/usr/bin/env bash

# add couchbase to apt sources
sudo wget -O/etc/apt/sources.list.d/couchbase.list http://packages.couchbase.com/ubuntu/couchbase-ubuntu1204.list
wget -O- http://packages.couchbase.com/ubuntu/couchbase.key | sudo apt-key add - 
sudo apt-get update -qq

# install libcouchbase
sudo apt-get install libcouchbase2 libcouchbase-dev

# install python couchbase client
sudo pip install couchbase --upgrade
