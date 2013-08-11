Hemlock
=======

Hemlock is an open-source project exploring ways to create a common data access
layer that eliminates the need to understand underlying data topologies but
still preserving the requirements of each data source such as access control,
performance, and formats.

![Hemlock L](docs/images/logo.png "Hemlock")

Install instructions
====================

```bash
git clone https://github.com/Lab41/Hemlock.git
```

Required Dependencies
------------

Python modules:
- [MySQLdb](http://mysql-python.sourceforge.net/MySQLdb.html)
- [texttable](https://pypi.python.org/pypi/texttable)
- [couchbase](http://www.couchbase.com/communities/python/getting-started) >= 1.0

Build a server running [MySQL](http://www.mysql.com/) to store user accounts, tenants, and registered 
systems.

Build a [Couchbase](http://www.couchbase.com/) cluster to store metadata and data of registered systems.

Build an [ElasticSearch](http://www.elasticsearch.org/) cluster to store the index of Couchbase.

Architecture
------------

Installing
----------

1. Create database ``hemlock`` in MySQL.


Credential files
----------------

Currently supported data sources
================================

Technology | Parameter | Python Module Dependencies
---------- | --------- | ------------
MySQL      | mysql     | MySQLdb
MongoDB    | mongo     | pymongo
Redis      | redis     | redis
Local FileSystem | fs  | magic, pdfminer, xmltodict
RESTful API | rest     | 
Streams (**experimental**)   | stream_odd |


Adding a new data source type
-----------------------------

Usage examples
==============

- Create a tenant
- Create a user
- Register a system


Related repositories
====================

Tests
=====

The tests for this project use [py.test](http://pytest.org/latest/)

Contributing to Hemlock
=======================

