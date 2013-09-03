hemlock.py
=======

HEMLOCK

            client-add-schedule (add a schedule to a client)
                --uuid (uuid of client)
                --schedule_id (uuid of schedule)
            

            client-get (get a specific client)
                --uuid (uuid of client)
            

            client-list (list all clients)
            

            client-purge (purge a specific client)
                --uuid (uuid of client)
            

            client-remove-schedule (remove a schedule from a client)
                --uuid (uuid of client)
                --schedule_id (uuid of schedule)
            

            client-run (run a specific client)
                --uuid (uuid of client)
            

            client-schedule (schedule a specific client)
                --name (name of the schedule)
                --minute (cron minute)
                --hour (cron hour)
                --day_of_month (cron day of month)
                --month (cron month)
                --day_of_week (cron day of week)
                --client_id (uuid of the client this schedule will run on)
            

            client-schedules-list (list schedules a client belongs to)
                --uuid (uuid of client)
            

            client-store (store a specific client)
                --name (name of client)
                --type (type of client, i.e. mysql)
                --system_id (uuid of system associated with the client)
                --credential_file (path to file that contains the credentials for the client)
            

            client-systems-list (list systems a client belongs to)
                --uuid (uuid of client)
            

            deregister-local-system (from Hemlock remove a system)
                --uuid (uuid of system)
            

            deregister-remote-system (from a system remove it from Hemlock)
                --uuid (uuid of system)
            

            hemlock-server-store (store credentials for the hemlock server)
                --credential_file (path to file that contains the credentials for the hemlock server)


            list-all (list everything)


            register-local-system (from a system add it to Hemlock)
                --name (name of system)
                --data_type (type of data stored in the system, i.e. csv, txt, doc, etc.)
                --description (description of what the data source is)
                --tenant_id (uuid of the tenant this system belongs in)
                --hostname (hostname of the system)
                --endpoint (endpoint of hemlock server, i.e. http://hemlock.server/)
                --poc_name (point of contact name for this system)
                --poc_email (point of contact email for this system)
            

            register-remote-system (add a system from Hemlock)
                --name (name of system)
                --data_type (type of data stored in the system, i.e. csv, txt, doc, etc.)
                --description (description of what the data source is)
                --tenant_id (uuidof the tenant this system belongs in)
                --hostname (hostname of the system)
                --port (port that the system has open to allow hemlock to get data from it)
                --remote_uri (uri of the system that hemlock and use to get data from, i.e. http://system.server:8080/my/data/feed/)
                --poc_name (point of contact name for this system)
                --poc_email (point of contact email for this system)
            

            role-create (create new role)
                --name (name of role)
            

            role-delete (delete role)
                --uuid (uuid of role)
            

            role-get (get a specific role)
                --uuid (uuid of role)
            

            role-list (list all roles)
            

            role-users-list (list users a role belongs to)
                --uuid (uuid of role)
            

            schedule-add-client (add a client to a schedule)
                --uuid (uuid of schedule)
                --client_id (uuid of client)
            

            schedule-clients-list (list client a schedule belongs to)
                --uuid (uuid of schedule)
            

            schedule-delete (delete a specific schedule)
                --uuid (uuid of schedule)
            

            schedule-get (get a specific schedule)
                --uuid (uuid of client)
            

            schedule-list (list all schedules)
            

            schedule-remove-client (remove a client from a schedule)
                --uuid (uuid of schedule)
                --client_id (uuid of client)
            

            start-scheduler (start the scheduler)
                --hemlock_creds_path (file path to the hemlock_creds file)
            

            system-add-tenant (add a tenant to a system)
                --uuid (uuid of system)
                --tenant_id (uuid of tenant)
            

            system-clients-list (list clients a system belongs to)
                --uuid (uuid of system)
            

            system-get (get a specific system)
                --uuid (uuid of system)
            

            system-list (list all systems)
            

            system-remove-tenant (remove a tenant from a system)
                --uuid (uuid of system)
                --tenant_id (uuid of tenant)
            

            system-tenants-list (list tenants a system belongs to)
                --uuid (uuid of system)
            

            tenant-create (create new tenant)
                --name (name of tenant)
            

            tenant-delete (delete tenant)
                --uuid (uuid of tenant)
            

            tenant-get (get a specific tenant)
                --uuid (uuid of tenant)
            

            tenant-list (list all tenants)
            

            tenant-systems-list (list systems in a tenant)
                --uuid (uuid of tenant)
            

            tenant-users-list (list users in a tenant)
                --uuid (uuid of tenant)
            

            user-add-role (add a role to a user)
                --uuid (uuid of user)
                --role_id (uuid of role)
            

            user-add-tenant (add a tenant to a user)
                --uuid (uuid of user)
                --tenant_id (uuid of tenant)
            

            user-create (create new user)
                --name (name of user)
                --username (username to login with)
                --email (email address of user)
                --role_id (uuid of role)
                --tenant_id (uuid of tenant)
            

            user-delete (delete user)
                --uuid (uuid of user)
            

            user-get (get a specific user)
                --uuid (uuid of user)
            

            user-list (list all users)
            

            user-remove-role (remove a role from a user)
                --uuid (uuid of user)
                --tenant_id (uuid of role)
            

            user-remove-tenant (remove a tenant from a user)
                --uuid (uuid of user)
                --tenant_id (uuid of tenant)
            

            user-roles-list (list roles a user belongs to)
                --uuid (uuid of user)
            

            user-tenants-list (list tenants a user belongs to)
                --uuid (uuid of user)

