#!/usr/bin/env bash

# !! TODO
#    update apt-get commands and check if actually ubuntu/debian
#    add another path for centos/redhat

# !! TODO make this optional
# add couchbase to apt sources
sudo wget -O/etc/apt/sources.list.d/couchbase.list http://packages.couchbase.com/ubuntu/couchbase-ubuntu1204.list
wget -O- http://packages.couchbase.com/ubuntu/couchbase.key | sudo apt-key add - 

sudo apt-get update -qq

# install gcc
sudo apt-get install -y gcc

# install python dev tools
sudo apt-get install -y python-dev

# !! TODO make this optional
# install libcouchbase
sudo apt-get install -y libcouchbase2 libcouchbase-dev

# !! TODO make this optional
# install python couchbase client
sudo pip install couchbase --upgrade

# install mysql-python connector
sudo apt-get install -y python-mysqldb

# install python-magic
sudo apt-get install -y python-magic

# install hemlock man page
sudo cp docs/_build/man/hemlock.1 /usr/share/man/man1/hemlock.1.gz
