#!/usr/bin/python

import getpass, sys, time, uuid
import MySQLdb as mdb
import texttable as tt

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

def system_add_tenant(args, var_d):
    arg_d = [
        '--uuid'
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
        '--uuid'
        '--tenant_id'
    ]
    return check_args(args, arg_d, var_d) 

def tenant_create(args, var_d):
    # !! TODO need to flesh out the rest of the options
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

def user_add_tenant(args, var_d):
    arg_d = [
        '--uuid'
        '--tenant_id'
    ]
    return check_args(args, arg_d, var_d) 

def user_create(args, var_d):
    # !! TODO need to flesh out the rest of the options
    arg_d = [
        '--name',
        '--email'
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

def user_remove_tenant(args, var_d):
    arg_d = [
        '--uuid'
        '--tenant_id'
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
                --name
                --data_type
                --description
                --tenant_id
                --hostname
                --endpoint
                --poc_name
                --poc_email
            """,
            'register-remote-system' : """
            register-remote-system (add a system from Hemlock)
                --name
                --data_type
                --description
                --tenant_id
                --hostname
                --port
                --remote_uri
                --poc_name
                --poc_email
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
            'user-add-tenant' : """
            user-add-tenant (add a tenant to a user)
                --uuid (uuid of user)
                --tenant_id (uuid of tenant)
            """,
            'user-create' : """
            user-create (create new user)
                --name (name of user)
                --email (email address of user)
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
            'user-remove-tenant' : """
            user-remove-tenant (remove a tenant from a user)
                --uuid (uuid of user)
                --tenant_id (uuid of tenant)
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
    arg_actions = {
        'deregister-local-system' : deregister_local_system,
        'deregister-remote-system' : deregister_remote_system,
        'register-local-system' : register_local_system,
        'register-remote-system' : register_remote_system,
        'system-add-tenant' : system_add_tenant,
        'system-get' : system_get,
        'system-list' : system_list,
        'system-remove-tenant' : system_remove_tenant,
        'tenant-create' : tenant_create,
        'tenant-delete' : tenant_delete,
        'tenant-get' : tenant_get,
        'tenant-list' : tenant_list,
        'user-add-tenant' : user_add_tenant,
        'user-create' : user_create,
        'user-delete' : user_delete,
        'user-get' : user_get,
        'user-list' : user_list,
        'user-remove-tenant' : user_remove_tenant
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
    server = raw_input("MySQL Server (default is localhost):")
    if server == "":
        server = "localhost"
    db = raw_input("MySQL DB (default is hemlock):")
    if db == "":
        db = "hemlock"
    user = raw_input("Username:")
    pw = getpass.getpass("Password:")
    return user, pw, db, server

def mysql_server(server, user, pw, db):
    # connect to the mysql server
    try:
        m_server = mdb.connect(server, user, pw, db)
    except:
        print "MySQL server failure"
        sys.exit(0)
    return m_server

def process_action(action, var_d, m_server):
    # !! TODO save stuff to a db
    # !! TODO do calls to and from couch
    # !! TODO tie in with frontend stuff
    # !! TODO try/except

    cur = m_server.cursor()
    # ensure mysql tables exist
    # !! TODO this needs to be fleshed out
    user_table = "CREATE TABLE IF NOT EXISTS users(id INT PRIMARY KEY AUTO_INCREMENT, uuid VARCHAR(36), name VARCHAR(50), email VARCHAR(50), created DATETIME)"

    system_table = "CREATE TABLE IF NOT EXISTS systems(id INT PRIMARY KEY AUTO_INCREMENT, uuid VARCHAR(36), name VARCHAR(50), data_type VARCHAR(50), description VARCHAR(200), tenant_id VARCHAR(36), endpoint VARCHAR(100), hostname VARCHAR(50), port VARCHAR(5), remote_uri VARCHAR(100), poc_name VARCHAR(50), poc_email VARCHAR(50), remote BOOL, created DATETIME, updated_data DATETIME)"
    tenant_table = "CREATE TABLE IF NOT EXISTS tenants(id INT PRIMARY KEY AUTO_INCREMENT, uuid VARCHAR(36), name VARCHAR(50), created DATETIME)"

    cur.execute(user_table)
    cur.execute(system_table)
    cur.execute(tenant_table)

    # perform action with args against mysql table
    uid = str(uuid.uuid4())
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    action_a = action.split("-")
    data_action = ""
    # used to ensure that the properties and values line up correctly
    props = []
    vals = []
    for key in var_d:
        props.append(key[2:])
        vals.append(var_d[key])
    props.append("uuid")
    props.append("created")
    vals.append(uid)
    vals.append(timestamp)

    if "system" in action_a:
        # update to systems table
        if "deregister" in action_a: 
            # delete
            # !! TODO
            print
        elif "register" in action_a:
            # write
            props.append("remote")
            if "remote" in action_a:
                vals.append("1")
            else:
                vals.append("0")
            data_action = "INSERT INTO systems("
            for prop in props:
                data_action += prop+", "
            data_action = data_action[:-2]+") VALUES("
            for val in vals:
                data_action += "\""+val+"\", "
            data_action = data_action[:-2]+")"
        else:
            # read only
            # !! TODO
            # list/get for systems
            data_action = "SELECT * FROM systems"
            if "get" in action_a:
                data_action += " WHERE uuid = '"+var_d['--uuid']+"'"
            print data_action
        cur.execute(data_action)

    else:
        # update to tenants table
        if "add" in action_a: 
            # write
            # !! TODO
            print

        elif "create" in action_a:
            # write
            if "user" in action_a:
                data_action = "INSERT INTO users("
            else: # tenant
                data_action = "INSERT INTO tenants("
            for prop in props:
                data_action += prop+", "
            data_action = data_action[:-2]+") VALUES("
            for val in vals:
                data_action += "\""+val+"\", "
            data_action = data_action[:-2]+")"
        elif "delete" in action_a:
            # delete
            # !! TODO
            print
        else:
            # read only
            # !! TODO
            # list/get for users and tenants
            print
        cur.execute(data_action)

    results = cur.fetchall()
    print results

    m_server.commit()
    m_server.close()
    
    # !! TODO testing pretty printing tables
    tab = tt.Texttable()

    x = [[]] # The empty row will have the header

    if results:
        i = 0
        while i < len(props):
            x.append([props[i],vals[i]])
            i += 1
    else:
        for result in results:
            # !! TODO cut up results tuple
            print        

    tab.add_rows(x)
    tab.set_cols_align(['c','c'])
    tab.set_deco(tab.HEADER | tab.VLINES | tab.BORDER)
    tab.set_chars(['-','|','+','-'])
    tab.header(['Property', 'Value'])
    print tab.draw()

if __name__ == "__main__":
    start_time = time.time()
    args = get_args()
    var_d, action = process_args(args)
    user, pw, db, server = get_auth()
    m_server = mysql_server(server, user, pw, db)
    process_action(action, var_d, m_server)
    print "Took",time.time() - start_time,"seconds to complete."
