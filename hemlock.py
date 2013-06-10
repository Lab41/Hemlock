#!/usr/bin/python

import getpass, os, sys, time, uuid
import MySQLdb as mdb
import texttable as tt
from couchbase.client import Couchbase

HELP_COUNTER = 0

def deregister_local_system(args, var_d):
    arg_d = [
        '--uuid'
    ]
    return check_args(args, arg_d, var_d) 

def deregister_remote_system(args, var_d):
    arg_d = [
        '--uuid'
    ]
    return check_args(args, arg_d, var_d) 

def register_local_system(args, var_d):
    arg_d = [
        '--name'
        '--data_type',
        '--description',
        '--tenant_id',
        '--hostname',
        '--endpoint',
        '--poc_name',
        '--poc_email'
    ]
    return check_args(args, arg_d, var_d) 

def register_remote_system(args, var_d):
    # !! TODO add map of operation vocabulary
    #         is this needed?
    arg_d = [
        '--name',
        '--data_type',
        '--description',
        '--tenant_id',
        '--hostname',
        '--port',
        '--remote_uri',
        '--poc_name',
        '--poc_email'
    ]
    return check_args(args, arg_d, var_d) 

def role_create(args, var_d):
    arg_d = [
        '--name'
    ]
    return check_args(args, arg_d, var_d) 

def role_delete(args, var_d):
    arg_d = [
        '--uuid'
    ]
    return check_args(args, arg_d, var_d) 

def role_list(args, var_d):
    arg_d = [
    ]
    return check_args(args, arg_d, var_d) 

def role_users_list(args, var_d):
    arg_d = [
        '--uuid'
    ]
    return check_args(args, arg_d, var_d) 

def system_add_tenant(args, var_d):
    arg_d = [
        '--uuid',
        '--tenant_id'
    ]
    return check_args(args, arg_d, var_d) 

def system_get(args, var_d):
    arg_d = [
        '--uuid'
    ]
    return check_args(args, arg_d, var_d) 

def system_list(args, var_d):
    arg_d = [
    ]
    return check_args(args, arg_d, var_d) 

def system_remove_tenant(args, var_d):
    arg_d = [
        '--uuid',
        '--tenant_id'
    ]
    return check_args(args, arg_d, var_d) 

def system_tenants_list(args, var_d):
    arg_d = [
        '--uuid'
    ]
    return check_args(args, arg_d, var_d) 

def tenant_create(args, var_d):
    arg_d = [
        '--name'
    ]
    return check_args(args, arg_d, var_d) 

def tenant_delete(args, var_d):
    arg_d = [
        '--uuid'
    ]
    return check_args(args, arg_d, var_d) 

def tenant_get(args, var_d):
    arg_d = [
        '--uuid'
    ]
    return check_args(args, arg_d, var_d) 

def tenant_list(args, var_d):
    arg_d = [
    ]
    return check_args(args, arg_d, var_d) 

def tenant_systems_list(args, var_d):
    arg_d = [
        '--uuid'
    ]
    return check_args(args, arg_d, var_d) 

def tenant_users_list(args, var_d):
    arg_d = [
        '--uuid'
    ]
    return check_args(args, arg_d, var_d) 

def user_add_role(args, var_d):
    arg_d = [
        '--uuid',
        '--role_id'
    ]
    return check_args(args, arg_d, var_d) 

def user_add_tenant(args, var_d):
    arg_d = [
        '--uuid',
        '--tenant_id'
    ]
    return check_args(args, arg_d, var_d) 

def user_create(args, var_d):
    # !! TODO add role
    arg_d = [
        '--name',
        '--username',
        '--email',
        '--role_id',
        '--tenant_id'
    ]
    return check_args(args, arg_d, var_d) 

def user_delete(args, var_d):
    arg_d = [
        '--uuid'
    ]
    return check_args(args, arg_d, var_d) 

def user_get(args, var_d):
    arg_d = [
        '--uuid'
    ]
    return check_args(args, arg_d, var_d) 

def user_list(args, var_d):
    arg_d = [
    ]
    return check_args(args, arg_d, var_d) 

def user_remove_role(args, var_d):
    arg_d = [
        '--uuid',
        '--role_id'
    ]
    return check_args(args, arg_d, var_d) 

def user_remove_tenant(args, var_d):
    arg_d = [
        '--uuid',
        '--tenant_id'
    ]
    return check_args(args, arg_d, var_d) 

def user_roles_list(args, var_d):
    arg_d = [
        '--uuid'
    ]
    return check_args(args, arg_d, var_d) 

def user_tenants_list(args, var_d):
    arg_d = [
        '--uuid'
    ]
    return check_args(args, arg_d, var_d) 

def check_args(args, arg_d, var_d):
    global HELP_COUNTER
    i = 0
    while i < len(args):
        try:
            if args[i] in arg_d:
                var_d[args[i]] = args[i+1]
                arg_d.remove(args[i])
            else:
                HELP_COUNTER += 1
                i = len(args)
            i += 2
        except:
            HELP_COUNTER += 1
    if arg_d:
        HELP_COUNTER += 1
    return var_d

def print_help(action):
    global HELP_COUNTER
    if HELP_COUNTER >= 1:
        help_dict = {
            'deregister-local-system' : """
            deregister-local-system (from Hemlock remove a system)
                --uuid (uuid of system)
            """,
            'deregister-remote-system' : """
            deregister-remote-system (from a system remove it from Hemlock)
                --uuid (uuid of system)
            """,
            'register-local-system' : """
            register-local-system (from a system add it to Hemlock)
                --name (name of system)
                --data_type (type of data stored in the system, i.e. csv, txt, doc, etc.)
                --description (description of what the data source is)
                --tenant_id (uuid of the tenant this system belongs in)
                --hostname (hostname of the system)
                --endpoint (endpoint of hemlock server, i.e. http://hemlock.server/)
                --poc_name (point of contact name for this system)
                --poc_email (point of contact email for this system)
            """,
            'register-remote-system' : """
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
            """,
            'role-create' : """
            role-create (create new role)
                --name (name of role)
            """,
            'role-delete' : """
            role-delete (delete role)
                --uuid (uuid of role)
            """,
            'role-list' : """
            role-list (list all roles)
            """,
            'role-users-list' : """
            role-users-list (list users a role belongs to)
                --uuid (uuid of role)
            """,
            'system-add-tenant' : """
            system-add-tenant (add a tenant to a system)
                --uuid (uuid of system)
                --tenant_id (uuid of tenant)
            """,
            'system-get' : """
            system-get (get a specific system)
                --uuid (uuid of system)
            """,
            'system-list' : """
            system-list (list all systems)
            """,
            'system-remove-tenant' : """
            system-remove-tenant (remove a tenant from a system)
                --uuid (uuid of system)
                --tenant_id (uuid of tenant)
            """,
            'system-tenants-list' : """
            system-tenants-list (list tenants a system belongs to)
                --uuid (uuid of system)
            """,
            'tenant-create' : """
            tenant-create (create new tenant)
                --name (name of tenant)
            """,
            'tenant-delete' : """
            tenant-delete (delete tenant)
                --uuid (uuid of tenant)
            """,
            'tenant-get' : """
            tenant-get (get a specific tenant)
                --uuid (uuid of tenant)
            """,
            'tenant-list' : """
            tenant-list (list all tenants)
            """,
            'tenant-systems-list' : """
            tenant-systems-list (list systems in a tenant)
                --uuid (uuid of tenant)
            """,
            'tenant-users-list' : """
            tenant-users-list (list users in a tenant)
                --uuid (uuid of tenant)
            """,
            'user-add-role' : """
            user-add-role (add a role to a user)
                --uuid (uuid of user)
                --role_id (uuid of role)
            """,
            'user-add-tenant' : """
            user-add-tenant (add a tenant to a user)
                --uuid (uuid of user)
                --tenant_id (uuid of tenant)
            """,
            'user-create' : """
            user-create (create new user)
                --name (name of user)
                --username (username to login with)
                --email (email address of user)
                --role_id (uuid of role)
                --tenant_id (uuid of tenant)
            """,
            'user-delete' : """
            user-delete (delete user)
                --uuid (uuid of user)
            """,
            'user-get' : """
            user-get (get a specific user)
                --uuid (uuid of user)
            """,
            'user-list' : """
            user-list (list all users)
            """,
            'user-remove-role' : """
            user-remove-role (remove a role from a user)
                --uuid (uuid of user)
                --tenant_id (uuid of role)
            """,
            'user-remove-tenant' : """
            user-remove-tenant (remove a tenant from a user)
                --uuid (uuid of user)
                --tenant_id (uuid of tenant)
            """,
            'user-roles-list' : """
            user-roles-list (list roles a user belongs to)
                --uuid (uuid of user)
            """,
            'user-tenants-list' : """
            user-tenants-list (list tenants a user belongs to)
                --uuid (uuid of user)
            """
        }
        print "HEMLOCK"
        if action in help_dict:
            print help_dict[action]
        else:
            for key in sorted(help_dict.iterkeys()):
                print help_dict[key]
        
        sys.exit()

def process_args(args):
    global HELP_COUNTER
    var_d = {}

    # !! TODO add load data actions
    #         is this needed?
    arg_actions = {
        'deregister-local-system' : deregister_local_system,
        'deregister-remote-system' : deregister_remote_system,
        'register-local-system' : register_local_system,
        'register-remote-system' : register_remote_system,
        'role-create' : role_create,
        'role-delete' : role_delete,
        'role-list' : role_list,
        'role-users-list' : role_users_list,
        'system-add-tenant' : system_add_tenant,
        'system-get' : system_get,
        'system-list' : system_list,
        'system-remove-tenant' : system_remove_tenant,
        'system-tenants-list' : system_tenants_list,
        'tenant-create' : tenant_create,
        'tenant-delete' : tenant_delete,
        'tenant-get' : tenant_get,
        'tenant-list' : tenant_list,
        'tenant-systems-list' : tenant_systems_list,
        'tenant-users-list' : tenant_users_list,
        'user-add-role' : user_add_role,
        'user-add-tenant' : user_add_tenant,
        'user-create' : user_create,
        'user-delete' : user_delete,
        'user-get' : user_get,
        'user-list' : user_list,
        'user-remove-role' : user_remove_role,
        'user-remove-tenant' : user_remove_tenant,
        'user-roles-list' : user_roles_list,
        'user-tenants-list' : user_tenants_list
    }

    # get action
    action = ""
    try:
        action = args[0]
        arg_actions[action](args[1:], var_d)
    except:
        HELP_COUNTER += 1

    print_help(action)

    return var_d, args[0]

def get_args():
    args = []
    for arg in sys.argv:
        args.append(arg)
    return args[1:]

def get_auth():
    try:
        server = os.environ['HEMLOCK_MYSQL_SERVER']
    except:
        server = raw_input("MySQL Server (default is localhost):")
        if server == "":
            server = "localhost"
    try:
        db = os.environ['HEMLOCK_MYSQL_DB']
    except:
        db = raw_input("MySQL DB (default is hemlock):")
        if db == "":
            db = "hemlock"
    try:
        user = os.environ['HEMLOCK_MYSQL_USER']
    except:
        user = raw_input("Username:")
    try:
        pw = os.environ['HEMLOCK_MYSQL_PW']
    except:
        pw = getpass.getpass("Password:")
    try:
        c_server = os.environ['HEMLOCK_COUCHBASE_SERVER']
    except:
        c_server = raw_input("Couchbase Server (default is localhost):")
        if c_server == "":
            c_server = "localhost"
    try:
        bucket = os.environ['HEMLOCK_COUCHBASE_BUCKET']
    except:
        bucket = raw_input("Couchbase Bucket (default is hemlock):")
        if bucket == "":
            bucket = "hemlock"
    try:
        c_pw = os.environ['HEMLOCK_COUCHBASE_PW']
    except:
        c_pw = getpass.getpass("Password:")
    return user, pw, db, server, c_server, bucket, c_pw

def mysql_server(server, user, pw, db):
    # connect to the mysql server
    try:
        m_server = mdb.connect(server, user, pw, db)
    except:
        print "MySQL server failure"
        sys.exit(0)
    return m_server

def process_action(action, var_d, m_server):
    # !! TODO tie in with frontend stuff
    # !! TODO try/except

    # !! TODO FIX THIS!!!!!!
    aes_key = "test"

    cur = m_server.cursor()

    # ensure mysql tables exist
    cur.execute("show tables")
    results = cur.fetchall()
    tables = []
    i = 0
    while i < len(results):
        tables.append(results[i][0])
        i += 1

    if "roles" not in tables:
        role_table = "CREATE TABLE IF NOT EXISTS roles(id INT PRIMARY KEY AUTO_INCREMENT, uuid VARCHAR(36), name VARCHAR(50), created DATETIME, INDEX (uuid)) ENGINE = INNODB"
        cur.execute(role_table)
    if "tenants" not in tables:
        tenant_table = "CREATE TABLE IF NOT EXISTS tenants(id INT PRIMARY KEY AUTO_INCREMENT, uuid VARCHAR(36), name VARCHAR(50), created DATETIME, INDEX (uuid)) ENGINE = INNODB"
        cur.execute(tenant_table)
    if "users" not in tables:
        user_table = "CREATE TABLE IF NOT EXISTS users(id INT PRIMARY KEY AUTO_INCREMENT, uuid VARCHAR(36), name VARCHAR(50), username VARCHAR(50), password VARBINARY(200), email VARCHAR(50), created DATETIME, INDEX (uuid)) ENGINE = INNODB"
        cur.execute(user_table)
    if "systems" not in tables:
        system_table = "CREATE TABLE IF NOT EXISTS systems(id INT PRIMARY KEY AUTO_INCREMENT, uuid VARCHAR(36), name VARCHAR(50), data_type VARCHAR(50), description VARCHAR(200), endpoint VARCHAR(100), hostname VARCHAR(50), port VARCHAR(5), remote_uri VARCHAR(100), poc_name VARCHAR(50), poc_email VARCHAR(50), remote BOOL, created DATETIME, updated_data DATETIME, INDEX (uuid)) ENGINE = INNODB"
        cur.execute(system_table)
    if "users_roles" not in tables:
        users_roles_table = "CREATE TABLE IF NOT EXISTS users_roles(user_id VARCHAR(36), role_id VARCHAR(36), INDEX (user_id), CONSTRAINT fkur_roles FOREIGN KEY (role_id) REFERENCES tenants(uuid), CONSTRAINT fkur_users FOREIGN KEY (user_id) REFERENCES users(uuid)) ENGINE = INNODB" 
        cur.execute(users_roles_table)
    if "users_tenants" not in tables:
        users_tenants_table = "CREATE TABLE IF NOT EXISTS users_tenants(user_id VARCHAR(36), tenant_id VARCHAR(36), INDEX (user_id), CONSTRAINT fkut_tenants FOREIGN KEY (tenant_id) REFERENCES tenants(uuid), CONSTRAINT fkut_users FOREIGN KEY (user_id) REFERENCES users(uuid)) ENGINE = INNODB" 
        cur.execute(users_tenants_table)
    if "systems_tenants" not in tables:
        systems_tenants_table = "CREATE TABLE IF NOT EXISTS systems_tenants(system_id VARCHAR(36), tenant_id VARCHAR(36), INDEX (system_id), CONSTRAINT fkst_tenants FOREIGN KEY (tenant_id) REFERENCES tenants(uuid), CONSTRAINT fkst_systems FOREIGN KEY (system_id) REFERENCES systems(uuid)) ENGINE = INNODB" 
        cur.execute(systems_tenants_table)

    # perform action with args against mysql table
    uid = str(uuid.uuid4())
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    action_a = action.split("-")
    data_action = ""
    data_action2 = ""
    # used to ensure that the properties and values line up correctly
    props = []
    vals = []
    for key in var_d:
        props.append(key[2:])
        vals.append(var_d[key])
    if "user" in action_a and "create" in action_a:
        props.append("password")
        pw = getpass.getpass("Password:")
        vals.append(pw)
    if "add" not in action_a:
        props.append("uuid")
        props.append("created")
        vals.append(uid)
        vals.append(timestamp)

    if "system" in action_a:
        # update to systems table
        if "deregister" in action_a: 
            # delete
            data_action = "DELETE FROM systems_tenants WHERE system_id = '"+var_d['--uuid']+"'"
            data_action2 = "DELETE FROM systems WHERE uuid = '"+var_d['--uuid']+"'"
        elif "register" in action_a:
            # write
            props.append("remote")
            if "remote" in action_a:
                vals.append("1")
            else:
                vals.append("0")
            data_action = "INSERT INTO systems("
            data_action2 = "INSERT INTO systems_tenants("
            i = 0
            k = -1
            for prop in props:
                if prop == "tenant_id":
                    data_action2 += prop+", system_id) VALUES("
                    k = i
                else:
                    data_action += prop+", "
                i += 1
            data_action = data_action[:-2]+") VALUES("
            i = 0
            for val in vals:
                if k == i:
                    data_action2 += "\""+val+"\", \""+uid+"\")" 
                else:
                    data_action += "\""+val+"\", "
                i += 1
            if k == -1:
                data_action2 = ""
            data_action = data_action[:-2]+")"
        elif "add" in action_a:
            # write
            data_action = "INSERT INTO systems_tenants(system_id, tenant_id) VALUES(\""+var_d['--uuid']+"\", \""+var_d['--tenant_id']+"\")"
            print
        elif "remove" in action_a:
            # delete
            remove_action = "SELECT * FROM users_tenants WHERE user_id = '"+var_d['--uuid']+"'"
            cur.execute(remove_action)
            remove_results = cur.fetchall()
            if len(remove_results) > 1:
                data_action = "DELETE FROM systems_tenants WHERE system_id = '"+var_d['--uuid']+"' and tenant_id = '"+var_d['--tenant_id']+"'"
            else:
                print "You can not remove the last tenant from a system."
                sys.exit(0)
        else:
            # read only
            if "tenants" in action_a:
                data_action = "SELECT * FROM systems_tenants WHERE system_id = '"+var_d['--uuid']+"'"
            else:
                data_action = "SELECT * FROM systems"
                if "get" in action_a:
                    data_action += " WHERE uuid = '"+var_d['--uuid']+"'"
        cur.execute(data_action)
        if data_action2:
            cur.execute(data_action2)

    else:
        # update to roles/tenants/users tables
        if "add" in action_a: 
            # write
            if "tenant" in action_a:
                data_action = "INSERT INTO users_tenants(user_id, tenant_id) VALUES(\""+var_d['--uuid']+"\", \""+var_d['--tenant_id']+"\")"
            else: # roles
                data_action = "INSERT INTO users_roles(user_id, role_id) VALUES(\""+var_d['--uuid']+"\", \""+var_d['--role_id']+"\")"
            print
        elif "remove" in action_a:
            # delete
            if "tenant" in action_a:
                remove_action = "SELECT * FROM users_tenants WHERE user_id = '"+var_d['--uuid']+"'"
            else: # roles
                remove_action = "SELECT * FROM users_roles WHERE user_id = '"+var_d['--uuid']+"'"
            cur.execute(remove_action)
            remove_results = cur.fetchall()
            if len(remove_results) > 1:
                if "tenant" in action_a:
                    data_action = "DELETE FROM users_tenants WHERE user_id = '"+var_d['--uuid']+"' and tenant_id = '"+var_d['--tenant_id']+"'"
                else: # roles
                    data_action = "DELETE FROM users_roles WHERE user_id = '"+var_d['--uuid']+"' and role_id = '"+var_d['--role_id']+"'"
            else:
                print "You can not remove the last tenant or role from a user."
                sys.exit(0)
        elif "create" in action_a:
            # write
            data_action = "INSERT INTO "+action_a[0]+"s("
            if "tenants" in action_a:
                data_action2 = "INSERT INTO "+action_a[0]+"s_tenants("
            else: # roles
                data_action2 = "INSERT INTO "+action_a[0]+"s_roles("
            i = 0
            j = -1
            k = -1
            for prop in props:
                if prop == "password":
                    j = i
                if prop == "tenant_id":
                    data_action2 += prop+", user_id) VALUES("
                    k = i
                if prop == "role_id":
                    data_action2 += prop+", user_id) VALUES("
                    k = i
                else:
                    data_action += prop+", "
                i += 1
            data_action = data_action[:-2]+") VALUES("
            i = 0
            for val in vals:
                if j == i:
                    data_action += "AES_ENCRYPT(\""+val+"\", \""+aes_key+"\"), "
                elif k == i:
                    data_action2 += "\""+val+"\", \""+uid+"\")" 
                else:
                    data_action += "\""+val+"\", "
                i += 1
            if k == -1:
                data_action2 = ""
            data_action = data_action[:-2]+")"
        elif "delete" in action_a:
            # delete
            if "tenants" in action_a:
                data_action = "DELETE FROM "+action_a[0]+"s_tenants WHERE "+action_a[0]+"_id = '"+var_d['--uuid']+"'"
            else: # roles
                data_action = "DELETE FROM "+action_a[0]+"s_roles WHERE "+action_a[0]+"_id = '"+var_d['--uuid']+"'"
            data_action2 = "DELETE FROM "+action_a[0]+"s WHERE uuid = '"+var_d['--uuid']+"'"
        else:
            # read only
            if "roles" in action_a:
                data_action = "SELECT * FROM users_roles WHERE user_id = '"+var_d['--uuid']+"'"
            elif "tenants" in action_a:
                data_action = "SELECT * FROM users_tenants WHERE user_id = '"+var_d['--uuid']+"'"
            elif "users" in action_a:
                data_action = "SELECT * FROM users_tenants WHERE tenant_id = '"+var_d['--uuid']+"'"
            elif "systems" in action_a:
                data_action = "SELECT * FROM systems_tenants WHERE tenant_id = '"+var_d['--uuid']+"'"
            else:
                data_action = "SELECT * FROM "+action_a[0]+"s"
                if "get" in action_a:
                    data_action += " WHERE uuid = '"+var_d['--uuid']+"'"
        cur.execute(data_action)
        if data_action2:
            cur.execute(data_action2)

    results = cur.fetchall()
    
    tab = tt.Texttable()
    x = [[]]
    tab_header = ['Property', 'Value']
    tab_align = ['c','c']
    
    if "get" not in action_a and "list" not in action_a:
        i = 0
        while i < len(props):
            x.append([props[i],vals[i]])
            i += 1
    else:
        if results:
            if "roles" in action_a:
                data_action = "desc users_roles"
            elif "tenants" in action_a:
                data_action = "desc "+action_a[0]+"s_tenants"
            elif "users" in action_a:
                if "tenant" in action_a:
                    data_action = "desc "+action_a[1]+"_tenants"
                else: # role
                    data_action = "desc "+action_a[1]+"_roles"
            elif "systems" in action_a:
                data_action = "desc "+action_a[1]+"_tenants"
            else:
                data_action = "desc "+action_a[0]+"s"
            cur.execute(data_action)
            desc_results = cur.fetchall()
            if len(results) == 1:
                vals = list(results[0])
                i = 0
                while i < len(desc_results):
                    if desc_results[i][0] != "password":
                        x.append([desc_results[i][0],vals[i]])
                    i += 1
            else:
                if "roles" in action_a:
                    tab_header = ['Role ID']
                    tab_align = ['c']
                    i = 0
                    a = -1
                    while i < len(desc_results):
                        print desc_results[i][0]
                        if desc_results[i][0] == 'role_id':
                            a = i
                        i += 1
                    i = 0
                    while i < len(results):
                        x.append([results[i][a]])
                        i += 1
                elif "tenants" in action_a:
                    tab_header = ['Tenant ID']
                    tab_align = ['c']
                    i = 0
                    a = -1
                    while i < len(desc_results):
                        print desc_results[i][0]
                        if desc_results[i][0] == 'tenant_id':
                            a = i
                        i += 1
                    i = 0
                    while i < len(results):
                        x.append([results[i][a]])
                        i += 1
                elif "users" in action_a:
                    tab_header = ['User ID']
                    tab_align = ['c']
                    i = 0
                    a = -1
                    while i < len(desc_results):
                        print desc_results[i][0]
                        if desc_results[i][0] == 'user_id':
                            a = i
                        i += 1
                    i = 0
                    while i < len(results):
                        x.append([results[i][a]])
                        i += 1
                elif "systems" in action_a:
                    tab_header = ['System ID']
                    tab_align = ['c']
                    i = 0
                    a = -1
                    while i < len(desc_results):
                        print desc_results[i][0]
                        if desc_results[i][0] == 'system_id':
                            a = i
                        i += 1
                    i = 0
                    while i < len(results):
                        x.append([results[i][a]])
                        i += 1
                else:
                    tab_header = ['Name', 'UUID']
                    i = 0
                    a = b = -1
                    while i < len(desc_results):
                        if desc_results[i][0] == 'name':
                            a = i
                        if desc_results[i][0] == 'uuid':
                            b = i 
                        i += 1
                    i = 0
                    while i < len(results):
                        x.append([results[i][a],results[i][b]])
                        i += 1
        
    m_server.commit()
    m_server.close()

    tab.add_rows(x)
    tab.set_deco(tab.HEADER | tab.VLINES | tab.BORDER)
    tab.set_chars(['-','|','+','-'])
    tab.set_cols_align(tab_align)
    tab.header(tab_header)
    
    if "remove" not in action_a and "delete" not in action_a and "deregister" not in action_a:    
        print tab.draw()

if __name__ == "__main__":
    start_time = time.time()
    args = get_args()
    var_d, action = process_args(args)
    user, pw, db, server, c_server, bucket, c_pw = get_auth()
    m_server = mysql_server(server, user, pw, db)
    process_action(action, var_d, m_server)
    print "Took",time.time() - start_time,"seconds to complete."
