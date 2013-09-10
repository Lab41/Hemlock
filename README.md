Hemlock
=======
[![PyPI version](https://badge.fury.io/py/hemlock.png)](http://badge.fury.io/py/hemlock) [![Build Status](https://travis-ci.org/Lab41/Hemlock.png?branch=master)](https://travis-ci.org/Lab41/Hemlock) [![downloads](https://pypip.in/d/hemlock/badge.png)](http://crate.io/packages/hemlock/) [![Coverage Status](https://coveralls.io/repos/Lab41/Hemlock/badge.png?branch=master)](https://coveralls.io/r/Lab41/Hemlock?branch=master)

Hemlock is an open-source project exploring ways to create a common data access
layer that eliminates the need to understand underlying data topologies but
still preserving the requirements of each data source such as access control,
performance, and formats.

![Hemlock L](https://raw.github.com/Lab41/Hemlock/master/docs/images/overview_hemlock.png "Hemlock")

Install instructions
====================

Option A, install using pip:

```bash
sudo pip install hemlock
```

Option B, build from source:

```bash
git clone https://github.com/Lab41/Hemlock.git
cd Hemlock
sudo python setup.py install
```

Required Dependencies
---------------------

Python modules:
- [MySQLdb](http://mysql-python.sourceforge.net/MySQLdb.html)
- [texttable](https://pypi.python.org/pypi/texttable)
- [couchbase](http://www.couchbase.com/communities/python/getting-started) >= 1.0
- [APScheduler](https://pypi.python.org/pypi/APScheduler)

Build a server running [MySQL](http://www.mysql.com/) to store user accounts, tenants, and registered 
systems.


Build a [Couchbase 2.0](http://www.couchbase.com/) cluster to store metadata and data of registered systems.

Build an [ElasticSearch 0.90.2](http://www.elasticsearch.org/) cluster to store the index of Couchbase.

Add XDCR one-way replication from Couchbase to ElasticSearch using this [plugin](https://github.com/couchbaselabs/elasticsearch-transport-couchbase) (Note, grab version 1.1.0).

Once the plugin is installed, be sure and update the couchbase_template.json under plugins/transport-couchbase/ to have the following:

```json
{
    "template" : "*",
    "order" : 10,
    "mappings" : {
        "couchbaseCheckpoint" : {
            "_source" : {
                "includes" : ["doc.*"]
            },
            "date_detection" : false,
            "dynamic_templates": [
                {
                    "store_no_index": {
                        "match": "*",
                        "mapping": {
                            "store" : "no",
                            "index" : "no",
                            "include_in_all" : false
                        }
                    }
                }
            ]
        },
        "_default_" : {
            "_source" : {
                "includes" : ["meta.*"]
            },
            "date_detection" : false,
            "properties" : {
                "meta" : {
                    "type" : "object",
                    "include_in_all" : false
                }
            }
        }
    }
}
```

Once that is added, start up ElasticSearch with ``bin/elasticsearch`` and then perform the following the first time:

```bash
curl -XPUT http://localhost:9200/_template/couchbase -d @plugins/transport-couchbase/couchbase_template.json
```

Installing required databases
-----------------------------

1. Create database ``hemlock`` in [MySQL](http://www.mysql.com/).
2. Create bucket ``hemlock`` in [Couchbase](http://www.couchbase.com/).
3. Create index ``hemlock`` in [ElasticSearch](http://www.elasticsearch.org/).


Getting started
----------------

1. Create Hemlock credentials (see 'Credential files')
   ```bash
   HEMLOCK_MYSQL_SERVER=192.168.1.10
   HEMLOCK_MYSQL_USERNAME=user
   HEMLOCK_MYSQL_DB=hemlock
   HEMLOCK_MYSQL_PW=pass
   HEMLOCK_COUCHBASE_SERVER=192.168.1.20
   HEMLOCK_COUCHBASE_BUCKET=hemlock
   HEMLOCK_COUCHBASE_USERNAME=hemlock
   HEMLOCK_COUCHBASE_PW=pass
   ```

   (if you'd like these to persist, consider adding export before each line and performing ``source`` on the file)
2. Create a tenant, role, user, and data source system
   ```bash
   hemlock tenant-create --name Project1

   hemlock tenant-list
   
   hemlock role-create --name User
   
   hemlock role-list
   
   hemlock user-create --name User1 \
                        --username Username1 \
                        --email user1@email.com \
                        --rold_id 42ba73f9-0ab6-4a50-908c-1585955754f4 \
                        --tenant_id 7d0f6b0d-334a-4d89-bd1a-70e8e1c04aa6
   
   hemlock user-list
   
   hemlock register-local-system --name System1 \
                                  --data_type csv \
                                  --description "description" \
                                  --tenant_id 7d0f6b0d-334a-4d89-bd1a-70e8e1c04aa6 \
                                  --hostname system1.fqdn \
                                  --endpoint http://hemlock.server/ \
                                  --poc_name user1 \
                                  --poc_email user1@email.com
   
   hemlock system-list
   ```
3. Add credentials for data source system, for example: mysql_creds
   ```bash
   MYSQL_SERVER=192.168.1.30
   MYSQL_DB=db1
   #MYSQL_TABLE=table1
   MYSQL_USERNAME=user
   MYSQL_PW=pass
   ```
4. Store a client
   ```bash
   hemlock client-store --name mysql_client_1 --type mysql --system_id 7d0f6b0d-334a-4d89-bd1a-70e8e1c04aa6 --credential_file /path/to/mysql_creds 

   hemlock client-list
   ```
5. Add credentials for hemlock
   ```bash
   hemlock hemlock-server-store --credential_file /path/to/hemlock_creds
   ```
6. Add a schedule for the data source system to run (optional)
   ```bash
   hemlock client-schedule --name schedule1 \
                          --minute "54" \
                          --hour "12" \
                          --day_of_month "*" \
                          --month "*" \
                          --day_of_week "*" \
                          --client_id 7d0f6b0d-334a-4d89-bd1a-70e8e1c04aa6

   hemlock schedule-list

   ```
7. Perform a test run for pulling data from the data source system
   ```bash
   hemlock client-run --uuid 7d0f6b0d-334a-4d89-bd1a-70e8e1c04aa6
   ```
8. Search for data that has been loaded into Hemlock
   ```bash
   Full text search with elasticsearch:

   http://elasticsearch.fqdn:9200/hemlock/_search?q=foo

   Which returns something the following:
   
   {
    "took": 14,
    "timed_out": false,
    "_shards": {
        "total": 20,
        "successful": 20,
        "failed": 0
    },
    "hits": {
        "total": 1,
        "max_score": 3.6582048,
        "hits": [
            {
                "_index": "hemlock",
                "_type": "couchbaseDocument",
                "_id": "865f458b4421ae5fd758e3c81aca9f8d8b4696b6",
                "_score": 3.6582048,
                "_source": {
                    "meta": {
                        "id": "865f458b4421ae5fd758e3c81aca9f8d8b4696b6",
                        "rev": "1-0010f1ac6045ccf40000000000000000",
                        "flags": 0,
                        "expiration": 0
                    }
                }
            }
        ]
    }
   }

   Now we can feed the 'id' into Couchbase to return the full document:
   
   http://couchbase.fqdn:8092/hemlock/865f458b4421ae5fd758e3c81aca9f8d8b4696b6
   
   Which returns something like the following:
   
   {
    "hemlock-system": "a50b86c2-59f7-42a3-aa67-3367579189fe",
    "hemlock-date": "2013-09-03 16:10:20",
    "stream": "DOYLIE"
   }
   ```
   
Credential files
----------------

1. Create a ``hemlock_creds`` file (see hemlock_creds_sample for an example): 

   ```bash
   HEMLOCK_MYSQL_SERVER=192.168.1.10
   HEMLOCK_MYSQL_USERNAME=user
   HEMLOCK_MYSQL_DB=hemlock
   HEMLOCK_MYSQL_PW=pass
   HEMLOCK_COUCHBASE_SERVER=192.168.1.20
   HEMLOCK_COUCHBASE_BUCKET=hemlock
   HEMLOCK_COUCHBASE_USERNAME=hemlock
   HEMLOCK_COUCHBASE_PW=pass
   ```
   
2. Create credential files for each client you intend to use ([examples](https://github.com/Lab41/Hemlock/tree/master/hemlock/clients/)).


Currently supported data sources
================================

Technology | Parameter | Python Module Dependencies
---------- | --------- | ------------
MySQL      | mysql     | MySQLdb
MongoDB    | mongo     | pymongo
Redis      | redis     | redis
Local FileSystem | fs  | magic, pdfminer, xmltodict
RESTful API | rest     | 
Streams    | stream_odd |


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
    hemlock tenant-create --name Project1
    ```
- Create a role

    ```bash
    hemlock role-create --name User
    ```
- Create a user

    ```bash
    hemlock user-create --name User1 \
                        --username Username1 \
                        --email user1@email.com \
                        --rold_id 42ba73f9-0ab6-4a50-908c-1585955754f4 \
                        --tenant_id 7d0f6b0d-334a-4d89-bd1a-70e8e1c04aa6
    ```
- Register a local system

    ```bash
    hemlock register-local-system --name System1 \
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
    hemlock system-list
    ```
- List created users

    ```bash
    hemlock user-list
    ```
- Lists created tenants

    ```bash
    hemlock tenant-list
    ```
- [Connecting to a client](https://github.com/Lab41/Hemlock/tree/master/hemlock/clients/)
- [Full CLI API list](https://github.com/Lab41/Hemlock/blob/master/docs/CLI.md)


Related repositories
====================

 - [Hemlock-REST](http://lab41.github.io/Hemlock-REST/)
 - [Hemlock-Frontend](http://lab41.github.io/Hemlock-Frontend/)

Documentation
=============

 - [Docs](http://lab41.github.io/Hemlock/docs/_build/html/index.html)

Tests
=====

The tests for this project use [py.test](http://pytest.org/latest/)


Contributing to Hemlock
=======================

What to contribute?  Awesome!  Issue a pull request or see more details [here](https://github.com/Lab41/Hemlock/blob/master/CONTRIBUTING.md).
