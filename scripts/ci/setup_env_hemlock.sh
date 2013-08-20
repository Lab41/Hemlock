#!/usr/bin/env bash

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

# install libssl
sudo apt-get install -y libssl0.9.8

# install Couchbase Server
sudo wget http://packages.couchbase.com/releases/2.0.0/couchbase-server-enterprise_x86_64_2.0.0.deb
sudo dpkg -i couchbase-server-enterprise_x86_64_2.0.0.deb
sudo service couchbase-server start

# setup bucket for test
/opt/couchbase/bin/couchbase-cli cluster-init -c 127.0.0.1:8091 --cluster-init-username=Administrator --cluster-init-password=password --cluster-init-ramsize=256
/opt/couchbase/bin/couchbase-cli bucket-create -c 127.0.0.1:8091 --bucket=hemlock --bucket-password=password --bucket-type=couchbase --bucket-port=11211 --bucket-ramsize=100 --bucket-replica=0 -u Administrator -p password
