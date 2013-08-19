#!/usr/bin/env python
#
#   Copyright (c) 2013 In-Q-Tel, Inc/Lab41, All Rights Reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import hemlock_options_parser
import getpass, json, os, sys, time, uuid
import MySQLdb as mdb
import texttable as tt
from couchbase import Couchbase

HELP_COUNTER = 0

class Hemlock():
    def deregister_local_system(self, args, var_d):
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def deregister_remote_system(self, args, var_d):
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def list_all(self, args, var_d):
        arg_d = [
        ]
        return self.check_args(args, arg_d, var_d)

    def register_local_system(self, args, var_d):
        arg_d = [
            '--name',
            '--data_type',
            '--description',
            '--tenant_id',
            '--hostname',
            '--endpoint',
            '--poc_name',
            '--poc_email'
        ]
        return self.check_args(args, arg_d, var_d)

    def register_remote_system(self, args, var_d):
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
        return self.check_args(args, arg_d, var_d)

    def role_create(self, args, var_d):
        arg_d = [
            '--name'
        ]
        return self.check_args(args, arg_d, var_d)

    def role_delete(self, args, var_d):
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def role_get(self, args, var_d):
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def role_list(self, args, var_d):
        arg_d = [
        ]
        return self.check_args(args, arg_d, var_d)

    def role_users_list(self, args, var_d):
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def system_add_tenant(self, args, var_d):
        arg_d = [
            '--uuid',
            '--tenant_id'
        ]
        return self.check_args(args, arg_d, var_d)

    def system_get(self, args, var_d):
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def system_list(self, args, var_d):
        arg_d = [
        ]
        return self.check_args(args, arg_d, var_d)

    def system_remove_tenant(self, args, var_d):
        arg_d = [
            '--uuid',
            '--tenant_id'
        ]
        return self.check_args(args, arg_d, var_d)

    def system_tenants_list(self, args, var_d):
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def tenant_create(self, args, var_d):
        arg_d = [
            '--name'
        ]
        return self.check_args(args, arg_d, var_d)

    def tenant_delete(self, args, var_d):
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def tenant_get(self, args, var_d):
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def tenant_list(self, args, var_d):
        arg_d = [
        ]
        return self.check_args(args, arg_d, var_d)

    def tenant_systems_list(self, args, var_d):
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def tenant_users_list(self, args, var_d):
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def user_add_role(self, args, var_d):
        arg_d = [
            '--uuid',
            '--role_id'
        ]
        return self.check_args(args, arg_d, var_d)

    def user_add_tenant(self, args, var_d):
        arg_d = [
            '--uuid',
            '--tenant_id'
        ]
        return self.check_args(args, arg_d, var_d)

    def user_create(self, args, var_d):
        arg_d = [
            '--name',
            '--username',
            '--email',
            '--role_id',
            '--tenant_id'
        ]
        return self.check_args(args, arg_d, var_d)

    def user_delete(self, args, var_d):
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def user_get(self, args, var_d):
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def user_list(self, args, var_d):
        arg_d = [
        ]
        return self.check_args(args, arg_d, var_d)

    def user_remove_role(self, args, var_d):
        arg_d = [
            '--uuid',
            '--role_id'
        ]
        return self.check_args(args, arg_d, var_d)

    def user_remove_tenant(self, args, var_d):
        arg_d = [
            '--uuid',
            '--tenant_id'
        ]
        return self.check_args(args, arg_d, var_d)

    def user_roles_list(self, args, var_d):
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def user_tenants_list(self, args, var_d):
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def check_args(self, args, arg_d, var_d):
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

    def print_help(self, action):
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
            'list-all' : """
            list-all (list everything)
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
            'role-get' : """
            role-get (get a specific role)
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

    def process_args(self, args):
        global HELP_COUNTER
        var_d = {}

        # !! TODO add load data actions
        #         is this needed?
        arg_actions = {
            'deregister-local-system' : self.deregister_local_system,
            'deregister-remote-system' : self.deregister_remote_system,
            'list-all' : self.list_all,
            'register-local-system' : self.register_local_system,
            'register-remote-system' : self.register_remote_system,
            'role-create' : self.role_create,
            'role-delete' : self.role_delete,
            'role-get' : self.role_get,
            'role-list' : self.role_list,
            'role-users-list' : self.role_users_list,
            'system-add-tenant' : self.system_add_tenant,
            'system-get' : self.system_get,
            'system-list' : self.system_list,
            'system-remove-tenant' : self.system_remove_tenant,
            'system-tenants-list' : self.system_tenants_list,
            'tenant-create' : self.tenant_create,
            'tenant-delete' : self.tenant_delete,
            'tenant-get' : self.tenant_get,
            'tenant-list' : self.tenant_list,
            'tenant-systems-list' : self.tenant_systems_list,
            'tenant-users-list' : self.tenant_users_list,
            'user-add-role' : self.user_add_role,
            'user-add-tenant' : self.user_add_tenant,
            'user-create' : self.user_create,
            'user-delete' : self.user_delete,
            'user-get' : self.user_get,
            'user-list' : self.user_list,
            'user-remove-role' : self.user_remove_role,
            'user-remove-tenant' : self.user_remove_tenant,
            'user-roles-list' : self.user_roles_list,
            'user-tenants-list' : self.user_tenants_list
        }

        # get action
        action = ""
        try:
            action = args[0]
            var_d = arg_actions[action](args[1:], var_d)
        except:
            HELP_COUNTER += 1

        self.print_help(action)

        return var_d, args[0]

    # use OptionParser to parse command-line switches for authentication variables
    # return variables in options array, as well as leftover args that don't have switches
    def parse_auth(self):  
        parser = hemlock_options_parser.PassThroughOptionParser()
        parser.add_option("-s", "--server-mysql", action="store", dest="server",help="MySQL Server") #, default="localhost"
        parser.add_option("-d", "--database", action="store", dest="db", help="MySQL DB")
        parser.add_option("-u", "--mysql-username", action="store", dest="user", help="MySQL Username")
        parser.add_option("-p", "--mysql-password", action="store", dest="pw", help="MySQL Password")
        parser.add_option("-c", "--couchbase-server", action="store", dest="c_server", help="Couchbase Server")
        parser.add_option("-b", "--couchbase-bucket", action="store", dest="bucket", help="Couchbase Bucket")
        parser.add_option("-w", "--couchbase-password", action="store", dest="c_pw", help="Couchbase Password")
        return parser.parse_args()

    def get_auth(self):
        # extract command-line switches
        (options, args_leftover) = Hemlock().parse_auth()

        # use environment variables and CLI as fallbacks for unspecified variables
        try:
            if options.server == None:
                options.server = os.environ['HEMLOCK_MYSQL_SERVER']
        except:
            options.server = raw_input("MySQL Server (default is localhost):")
            if options.server == "":
                options.server = "localhost"

        try:
            if options.db == None:
                options.db = os.environ['HEMLOCK_MYSQL_DB']
        except:
            options.db = raw_input("MySQL DB (default is hemlock):")
            if options.db == "":
                options.db = "hemlock"

        try:
            if options.user == None:
                options.user = os.environ['HEMLOCK_MYSQL_USER']
        except:
            options.user = raw_input("Username:")

        try:
            if options.pw == None:
                options.pw = os.environ['HEMLOCK_MYSQL_PW']
        except:
            options.pw = getpass.getpass("MySQL Password:")

        try:
            if options.c_server == None:
                options.c_server = os.environ['HEMLOCK_COUCHBASE_SERVER']
        except:
            options.c_server = raw_input("Couchbase Server (default is localhost):")
            if options.c_server == "":
                options.c_server = "localhost"

        try:
            if options.bucket == None:
                options.bucket = os.environ['HEMLOCK_COUCHBASE_BUCKET']
        except:
            options.bucket = raw_input("Couchbase Bucket (default is hemlock):")
            if options.bucket == "":
                options.bucket = "hemlock"

        try:
            if options.c_pw == None:
                options.c_pw = os.environ['HEMLOCK_COUCHBASE_PW']
        except:
            options.c_pw = getpass.getpass("Couchbase Password:")

        return args_leftover, options.user, options.pw, options.db, options.server, options.c_server, options.bucket, options.c_pw

    def mysql_server(self, server, user, pw, db):
        # connect to the mysql server
        try:
            m_server = mdb.connect(server, user, pw, db)
        except:
            print "MySQL server failure"
            sys.exit(0)
        return m_server

    def process_action(self, action, var_d, m_server):
        error = 0
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
            users_roles_table = "CREATE TABLE IF NOT EXISTS users_roles(user_id VARCHAR(36), role_id VARCHAR(36), INDEX (user_id), CONSTRAINT fkur_roles FOREIGN KEY (role_id) REFERENCES roles(uuid), CONSTRAINT fkur_users FOREIGN KEY (user_id) REFERENCES users(uuid) ON DELETE CASCADE) ENGINE = INNODB"
            cur.execute(users_roles_table)
        if "users_tenants" not in tables:
            users_tenants_table = "CREATE TABLE IF NOT EXISTS users_tenants(user_id VARCHAR(36), tenant_id VARCHAR(36), INDEX (user_id), CONSTRAINT fkut_tenants FOREIGN KEY (tenant_id) REFERENCES tenants(uuid), CONSTRAINT fkut_users FOREIGN KEY (user_id) REFERENCES users(uuid) ON DELETE CASCADE) ENGINE = INNODB"
            cur.execute(users_tenants_table)
        if "systems_tenants" not in tables:
            systems_tenants_table = "CREATE TABLE IF NOT EXISTS systems_tenants(system_id VARCHAR(36), tenant_id VARCHAR(36), INDEX (system_id), CONSTRAINT fkst_tenants FOREIGN KEY (tenant_id) REFERENCES tenants(uuid), CONSTRAINT fkst_systems FOREIGN KEY (system_id) REFERENCES systems(uuid) ON DELETE CASCADE) ENGINE = INNODB"
            cur.execute(systems_tenants_table)

        # perform action with args against mysql table
        uid = str(uuid.uuid4())
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        action_a = action.split("-")
        data_action = ""
        data_action2 = ""
        data_action3 = ""
        # used to ensure that the properties and values line up correctly
        props = []
        vals = []
        for key in var_d:
            props.append(key[2:])
            vals.append(var_d[key])
        if "user" in action_a and "create" in action_a:
            props.append("password")
            pw = getpass.getpass("User Password:")
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
            elif "remove" in action_a:
                # delete
                remove_action = "SELECT * FROM systems_tenants WHERE system_id = '"+var_d['--uuid']+"'"
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
                data_action2 = "INSERT INTO "+action_a[0]+"s_tenants("
                data_action3 = "INSERT INTO "+action_a[0]+"s_roles("
                i = 0
                j = -1
                k = -1
                l = -1
                for prop in props:
                    if prop == "password":
                        j = i
                    if prop == "tenant_id":
                        data_action2 += prop+", user_id) VALUES("
                        k = i
                    elif prop == "role_id":
                        data_action3 += prop+", user_id) VALUES("
                        l = i
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
                    elif l == i:
                        data_action3 += "\""+val+"\", \""+uid+"\")"
                    else:
                        data_action += "\""+val+"\", "
                    i += 1
                if k == -1:
                    data_action2 = ""
                if l == -1:
                    data_action3 = ""
                data_action = data_action[:-2]+")"
            elif "delete" in action_a:
                # delete
                if "tenants" in action_a:
                    data_action = "DELETE FROM "+action_a[0]+"s_tenants WHERE "+action_a[0]+"_id = '"+var_d['--uuid']+"'"
                elif "roles" in action_a:
                    data_action = "DELETE FROM "+action_a[0]+"s_roles WHERE "+action_a[0]+"_id = '"+var_d['--uuid']+"'"
                data_action2 = "DELETE FROM "+action_a[0]+"s WHERE uuid = '"+var_d['--uuid']+"'"
            else:
                # read only
                if "roles" in action_a:
                    data_action = "SELECT * FROM users_roles WHERE user_id = '"+var_d['--uuid']+"'"
                elif "tenants" in action_a and "user" in action_a:
                    data_action = "SELECT * FROM users_tenants WHERE user_id = '"+var_d['--uuid']+"'"
                elif "tenants" in action_a and "system" in action_a:
                    data_action = "SELECT * FROM systems_tenants WHERE system_id = '"+var_d['--uuid']+"'"
                elif "users" in action_a and "tenant" in action_a:
                    data_action = "SELECT * FROM users_tenants WHERE tenant_id = '"+var_d['--uuid']+"'"
                elif "users" in action_a and "role" in action_a:
                    data_action = "SELECT * FROM users_roles WHERE role_id = '"+var_d['--uuid']+"'"
                elif "systems" in action_a:
                    data_action = "SELECT * FROM systems_tenants WHERE tenant_id = '"+var_d['--uuid']+"'"
                elif "all" in action_a:
                    # since this one returns all data and 
                    # descriptions in one payload, it will 
                    # be structured as a json object for 
                    # ease of consumability
                    # 
                    # example:
                    # 
                    # {
                    #    "users_tenants": [
                    #        {
                    #            "tenant_id": "602d5b58-cce9-4040-91dd-a2b2f0e954af",
                    #            "user_id": "c8e6cbcc-c657-4de9-a02a-c8121f1a11a1"
                    #        },
                    #        {
                    #            "tenant_id": "602d5b58-cce9-4040-91dd-a2b2f0e954af",
                    #            "user_id": "91e7c621-ba88-4f2c-a78e-8f6a8a79105c"
                    #        }
                    #    ],
                    #    "users": [
                    #        {
                    #            "username": "lkberj",
                    #            "name": "asdf",
                    #            "created": "2013-08-13 23:29:29",
                    #            "id": "1",
                    #            "email": "asdlkfj@aldskfj.com",
                    #            "uuid": "c8e6cbcc-c657-4de9-a02a-c8121f1a11a1"
                    #        },
                    #        {
                    #            "username": "lkberj",
                    #            "name": "asdf",
                    #            "created": "2013-08-13 23:44:47",
                    #            "id": "2",
                    #            "email": "asdlkfj@aldskfj.com",
                    #            "uuid": "91e7c621-ba88-4f2c-a78e-8f6a8a79105c"
                    #        }
                    #    ],
                    #    "roles": [
                    #        {
                    #            "created": "2013-08-13 23:25:12",
                    #            "id": "1",
                    #            "name": "role1",
                    #            "uuid": "e39d6ac4-dfc7-46de-b048-7ff4884d3018"
                    #        },
                    #        {
                    #            "created": "2013-08-13 23:44:19",
                    #            "id": "2",
                    #            "name": "role2",
                    #            "uuid": "c7eb6f3b-9277-46e7-89e3-f3d59ab7e561"
                    #        }
                    #    ],
                    #    "users_roles": [
                    #        {
                    #            "user_id": "c8e6cbcc-c657-4de9-a02a-c8121f1a11a1",
                    #            "role_id": "e39d6ac4-dfc7-46de-b048-7ff4884d3018"
                    #        },
                    #        {
                    #            "user_id": "91e7c621-ba88-4f2c-a78e-8f6a8a79105c",
                    #            "role_id": "c7eb6f3b-9277-46e7-89e3-f3d59ab7e561"
                    #        }
                    #    ],
                    #    "systems": [
                    #        {
                    #            "endpoint": "None",
                    #            "poc_email": "asdf@alkdfj.com",
                    #            "description": "desc",
                    #            "data_type": "data",
                    #            "created": "2013-08-13 23:27:03",
                    #            "hostname": "asdf",
                    #            "poc_name": "foo bar",
                    #            "uuid": "4991f644-e94d-472e-8526-c7f08a656735",
                    #            "port": "123",
                    #            "remote": "1",
                    #            "remote_uri": "http://localhost/",
                    #            "updated_data": "2013-08-16 21:16:01",
                    #            "id": "1",
                    #            "name": "system4"
                    #        }
                    #    ],
                    #    "tenants": [
                    #        {
                    #            "created": "2013-08-13 23:25:06",
                    #            "id": "1",
                    #            "name": "tenant1",
                    #            "uuid": "602d5b58-cce9-4040-91dd-a2b2f0e954af"
                    #        },
                    #        {
                    #            "created": "2013-08-13 23:46:50",
                    #            "id": "2",
                    #            "name": "tenant2",
                    #            "uuid": "b92c03bc-ab3f-4994-8148-5d5eb3e7cc65"
                    #        }
                    #    ],
                    #    "systems_tenants": [
                    #        {
                    #            "tenant_id": "602d5b58-cce9-4040-91dd-a2b2f0e954af",
                    #            "system_id": "4991f644-e94d-472e-8526-c7f08a656735"
                    #        }
                    #    ]
                    # }
                    #
                    data_dict = {}

                    # get all tables
                    data_action = "show tables"
                    cur.execute(data_action)
                    results = cur.fetchall()
                    tables =  [x[0] for x in results]

                    # for each table, get data and field names
                    for table in tables:
                        table_array = []
                        # get field names of each table
                        data_action = "DESC "+table
                        cur.execute(data_action)
                        results = cur.fetchall()
                        # get data from each table
                        data_action = "SELECT * FROM "+table
                        cur.execute(data_action)
                        results2 = cur.fetchall()
                        # match up field names and data into a dictionary
                        for entry in results2:
                            item_dict = {}
                            for field, item in zip([x[0] for x in results], entry):
                                # do not return user's passwords
                                if field != "password":
                                    item_dict[field] = str(item)
                            table_array.append(item_dict)
                        data_dict[table] = table_array
                    # this print will get consumed by CLI and REST APIs
                    print json.dumps(data_dict)
                    # reset data_action so that nothing extra is fetched
                    data_action = ""
                else:
                    data_action = "SELECT * FROM "+action_a[0]+"s"
                    if "get" in action_a:
                        data_action += " WHERE uuid = '"+var_d['--uuid']+"'"
            try:
                if data_action:
                    cur.execute(data_action)
                if data_action2:
                    cur.execute(data_action2)
                if data_action3:
                    cur.execute(data_action3)
            except:
                error = 1
                print "not valid"

        results = cur.fetchall()
        desc_results = ""

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

                if len(results) == 1 and "list" not in action_a:
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

        tab.add_rows(x)
        tab.set_deco(tab.HEADER | tab.VLINES | tab.BORDER)
        tab.set_chars(['-','|','+','-'])
        tab.set_cols_align(tab_align)
        tab.header(tab_header)

        if "remove" not in action_a and "delete" not in action_a and "deregister" not in action_a and "all" not in action_a:
            print tab.draw()
        return x, error

if __name__ == "__main__":
    start_time = time.time()
    args, user, pw, db, server, c_server, bucket, c_pw = Hemlock().get_auth()
    var_d, action = Hemlock().process_args(args)
    m_server = Hemlock().mysql_server(server, user, pw, db)
    x, error = Hemlock().process_action(action, var_d, m_server)
    m_server.commit()
    m_server.close()
    print "Took",time.time() - start_time,"seconds to complete."
