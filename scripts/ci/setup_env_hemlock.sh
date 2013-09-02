#!/usr/bin/env bash

# !! TODO
#    update apt-get commands and check if actually ubuntu/debian
#    add another path for centos/redhat

# add couchbase to apt sources
sudo wget -O/etc/apt/sources.list.d/couchbase.list http://packages.couchbase.com/ubuntu/couchbase-ubuntu1204.list
wget -O- http://packages.couchbase.com/ubuntu/couchbase.key | sudo apt-key add - 

sudo apt-get update -qq

# install gcc
sudo apt-get install -y gcc

# install python dev tools
sudo apt-get install -y python-dev

# install libcouchbase
sudo apt-get install -y libcouchbase2 libcouchbase-dev

# install python couchbase client
sudo pip install couchbase --upgrade

# install mysql-python connector
sudo apt-get install -y python-mysqldb
