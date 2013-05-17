hemlock
=======

HEMLOCK

            deregister-local-system (from Hemlock remove a system)
                --uuid (uuid of system)
            

            deregister-remote-system (from a system remove it from Hemlock)
                --uuid (uuid of system)
            

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
            

            system-add-tenant (add a tenant to a system)
                --uuid (uuid of system)
                --tenant_id (uuid of tenant)
            

            system-get (get a specific system)
                --uuid (uuid of system)
            

            system-list (list all systems)
            

            system-remove-tenant (remove a tenant from a system)
                --uuid (uuid of system)
                --tenant_id (uuid of tenant)
            

            tenant-create (create new tenant)
                --name (name of tenant)
            

            tenant-delete (delete tenant)
                --uuid (uuid of tenant)
            

            tenant-get (get a specific tenant)
                --uuid (uuid of tenant)
            

            tenant-list (list all tenants)
            

            user-add-tenant (add a tenant to a user)
                --uuid (uuid of user)
                --tenant_id (uuid of tenant)
            

            user-create (create new user)
                --name (name of user)
                --email (email address of user)
            

            user-delete (delete user)
                --uuid (uuid of user)
            

            user-get (get a specific user)
                --uuid (uuid of user)
            

            user-list (list all users)
            

            user-remove-tenant (remove a tenant from a user)
                --uuid (uuid of user)
                --tenant_id (uuid of tenant)
            
