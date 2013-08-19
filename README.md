Hemlock
=======

Hemlock is an open-source project exploring ways to create a common data access
layer that eliminates the need to understand underlying data topologies but
still preserving the requirements of each data source such as access control,
performance, and formats.

![Hemlock L](https://raw.github.com/Lab41/Hemlock/master/docs/images/overview_hemlock.png "Hemlock")

Install instructions
====================

```bash
sudo pip install hemlock

Or build from source:
git clone https://github.com/Lab41/Hemlock.git
```

Required Dependencies
---------------------

Python modules:
- [MySQLdb](http://mysql-python.sourceforge.net/MySQLdb.html)
- [texttable](https://pypi.python.org/pypi/texttable)
- [couchbase](http://www.couchbase.com/communities/python/getting-started) >= 1.0

Build a server running [MySQL](http://www.mysql.com/) to store user accounts, tenants, and registered 
systems.


Build a [Couchbase](http://www.couchbase.com/) cluster to store metadata and data of registered systems.

Build an [ElasticSearch](http://www.elasticsearch.org/) cluster to store the index of Couchbase.


Installing
----------

1. Create database ``hemlock`` in MySQL.
2. Create bucket ``hemlock`` in Couchbase.
3. Create index ``hemlock`` in ElasticSearch.


Credential files
----------------

1. Create a ``hemlock_creds`` file (see hemlock_creds_sample for an example): 
    ```bash
    SAMPLE hemlock_creds:
    
    HEMLOCK_MYSQL_SERVER=192.168.1.10
    HEMLOCK_MYSQL_USERNAME=user
    HEMLOCK_MYSQL_PW=pass
    HEMLOCK_COUCH_SERVER=192.168.1.20
    HEMLOCK_COUCH_PW=pass
    ```
2. Create credential files for each client you intend to use ([examples](https://github.com/Lab41/Hemlock/tree/master/clients/)).


Currently supported data sources
================================

Technology | Parameter | Python Module Dependencies
---------- | --------- | ------------
MySQL      | mysql     | MySQLdb
MongoDB    | mongo     | pymongo
Redis      | redis     | redis
Local FileSystem | fs  | magic, pdfminer, xmltodict
RESTful API | rest     | 
Streams ( **experimental** )   | stream_odd |


Adding a new data source type
-----------------------------

Create a new class under the clients folder for each new data source type.  Most
classes will need two methods defined: ``connect_client`` and ``get_data``.

The following is a template that can be used to work from:

```python
class HMyclient:
    def connect_client(self, client_dict):
        # return a handle that can be used to get data from the data source
        return c_server
    def get_data(self, client_dict, c_server, h_server, client_uuid):
        # data_list is an array of arrays to contain the data
        data_list = [[]]
        # desc_list is an array that contains the schema (if exists or known)
        desc_list = []
        return data_list, desc_list
```

Usage examples
==============

- Create a tenant

    ```bash
    python hemlock.py tenant-create --name Project1
    ```
- Create a role

    ```bash
    python hemlock.py role-create --name User
    ```
- Create a user

    ```bash
    python hemlock.py user-create --name User1 \
                                  --username Username1 \
                                  --email user1@email.com \
                                  --rold_id 42ba73f9-0ab6-4a50-908c-1585955754f4 \
                                  --tenant_id 7d0f6b0d-334a-4d89-bd1a-70e8e1c04aa6
    ```
- Register a local system

    ```bash
    python hemlock.py register-local-system --name System1 \
                                            --data_type csv \
                                            --description "description" \
                                            --tenant_id 7d0f6b0d-334a-4d89-bd1a-70e8e1c04aa6 \
                                            --hostname system1.fqdn \
                                            --endpoint http://hemlock.server/ \
                                            --poc_name user1 \
                                            --poc_email user1@email.com
    ```
- List registered systems

    ```bash
    python hemlock.py system-list
    ```
- List created users

    ```bash
    python hemlock.py user-list
    ```
- Lists created tenants

    ```bash
    python hemlock.py tenant-list
    ```
- [Connecting to a client](https://github.com/Lab41/Hemlock/tree/master/clients/)
- [Full CLI API list](https://github.com/Lab41/Hemlock/blob/master/docs/CLI.md)


Related repositories
====================

[Hemlock-REST](https://lab41.github.io/Hemlock-REST/)

Tests
=====

The tests for this project use [py.test](http://pytest.org/latest/)

Travis CI Status
================

[![Build Status](https://travis-ci.org/Lab41/Hemlock.png?branch=master)](https://travis-ci.org/Lab41/Hemlock)


Contributing to Hemlock
=======================

What to contribute?  Awesome!  Issue a pull request or see more details [here](https://github.com/Lab41/Hemlock/blob/master/CONTRIBUTING.md).
