Hemlock
=======

[Hemlock](https://github.com/Lab41/Hemlock/)

Client usage examples
=====================

- Connect to a MySQL database
    Create a MySQL credential file:
    ```bash
    SAMPLE mysql_creds
    # note: MYSQL_TABLE is not required

    MYSQL_SERVER=192.168.1.30
    MYSQL_DB=db1
    #MYSQL_TABLE=table1
    MYSQL_USERNAME=user
    MYSQL_PW=pass
    ```

    Register the new system, if you haven't already:
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

    If your system is already registered, grab its UUID:
    ```bash
    hemlock system-list
    ```

    Store client type and credentials:
    ```bash
    hemlock client-store --name mysql_client_1 --type mysql --system_id 7d0f6b0d-334a-4d89-bd1a-70e8e1c04aa6 --credential_file /path/to/mysql_creds 
    ```

    Start grabbing data (can be run either locally or remotely)
    ```bash
    hemlock client-run --uuid 3565d4e2-6d81-488a-8c01-93c5421ad95d

    or

    python hemlock_base.py --uuid 3565d4e2-6d81-488a-8c01-93c5421ad95d --client mysql
    ```

- Connect to a Redis database
    Create a Redis credential file:
    ```bash
    SAMPLE redis_creds

    REDIS_SERVER=192.168.1.31
    ```

    Register the new system, if you haven't already:
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

    If your system is already registered, grab its UUID:
    ```bash
    hemlock system-list
    ```

    Store client type and credentials:
    ```bash
    hemlock client-store --name redis_client_1 --type redis --system_id 7d0f6b0d-334a-4d89-bd1a-70e8e1c04aa6 --credential_file /path/to/redis_creds 
    ```

    Start grabbing data (can be run either locally or remotely)
    ```bash
    hemlock client-run --uuid da917588-f63a-47f1-98e2-33fce24a7a0a

    or

    python hemlock_base.py --uuid da917588-f63a-47f1-98e2-33fce24a7a0a --client redis
    ```


- See other sample cred files in this folder for other available supported 
  clients
