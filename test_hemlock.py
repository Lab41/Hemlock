import hemlock, re
import MySQLdb as mdb

class TestClass:
    def process_role_create(self):
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql("localhost", "testUser", "password", "test_hemlock")
        x, error1 = a.process_action("role-create", {'--name':'role1'}, m_server)
        error.append(error1)
        cur = m_server.cursor()
        str = "select * from roles where uuid = '"+x[2][1]+"'"
        cur.execute(str)
        y = cur.fetchall()
        return x, y, error

    def process_tenant_create(self):
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql("localhost", "testUser", "password", "test_hemlock")
        x, error1 = a.process_action("tenant-create", {'--name':'tenant1'}, m_server)
        error.append(error1)
        cur = m_server.cursor()
        str = "select * from tenants where uuid = '"+x[2][1]+"'"
        cur.execute(str)
        y = cur.fetchall()
        return x, y, error

    def process_user_create(self):
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql("localhost", "testUser", "password", "test_hemlock")
        b, error1 = a.process_action("role-create", {'--name':'role1'}, m_server)
        error.append(error1)
        c, error2 = a.process_action("tenant-create", {'--name':'tenant1'}, m_server)
        error.append(error2)
        x, error3 = a.process_action("user-create", {'--name':'user1', '--username':'username1', '--email':'email@dot.com', '--role_id':b[2][1], '--tenant_id':c[2][1]}, m_server)
        error.append(error3)
        cur = m_server.cursor()
        str = "select * from users where uuid = '"+x[7][1]+"'"
        cur.execute(str)
        y = cur.fetchall()
        return x, y, error

    def process_register_local_system(self):
        a = hemlock.Hemlock()
        m_server = self.connect_mysql("localhost", "testUser", "password", "test_hemlock")
        # !! TODO need to properly fill {}
        # !! TODO need to first create a tenant, get the uuid, then deregister that uuid
        x, error = a.process_action("tenant-create", {'--name':'tenant1'}, m_server)
        x, error = a.process_action("register-local-system", {'--name':'local-system1', '--data_type':'data-type1', '--description': 'description1', '--tenant_id':'asdf', '--hostname':'hostname1', '--endpoint':'http://endpoint.com/', '--poc_name':'poc-name1', '--poc_email':'poc-email@dot.com'}, m_server)
        cur = m_server.cursor()
        str = "select * from systems where uuid = '"+x[2][1]+"'"
        cur.execute(str)
        y = cur.fetchall()
        return x, y, error

    def process_register_remote_system(self):
        a = hemlock.Hemlock()
        m_server = self.connect_mysql("localhost", "testUser", "password", "test_hemlock")
        # !! TODO need to properly fill {}
        # !! TODO need to first create a tenant, get the uuid, then deregister that uuid
        x, error = a.process_action("tenant-create", {'--name':'tenant1'}, m_server)
        x, error = a.process_action("register-remote-system", {'--name':'remote-system1', '--data_type':'data-type1', '--description': 'description1', '--tenant_id':'asdf', '--hostname':'hostname1', '--port':'80', '--remote_uri':'http://remote.uri/', '--poc_name':'poc-name1', '--poc_email':'poc-email@dot.com'}, m_server)
        cur = m_server.cursor()
        str = "select * from systems where uuid = '"+x[2][1]+"'"
        cur.execute(str)
        y = cur.fetchall()
        return x, y, error

    def process_role_list(self):
        a = hemlock.Hemlock()
        m_server = self.connect_mysql("localhost", "testUser", "password", "test_hemlock")
        x, error = a.process_action("role-list", {}, m_server)
        x, error = a.process_action("role-create", {'--name':'role1'}, m_server)
        x, error = a.process_action("role-list", {}, m_server)
        x, error = a.process_action("role-create", {'--name':'role1'}, m_server)
        x, error = a.process_action("role-list", {}, m_server)
        return x, error

    def process_tenant_list(self):
        a = hemlock.Hemlock()
        m_server = self.connect_mysql("localhost", "testUser", "password", "test_hemlock")
        x, error = a.process_action("tenant-list", {}, m_server)
        x, error = a.process_action("tenant-create", {'--name':'tenant1'}, m_server)
        x, error = a.process_action("tenant-list", {}, m_server)
        x, error = a.process_action("tenant-create", {'--name':'tenant1'}, m_server)
        x, error = a.process_action("tenant-list", {}, m_server)
        return x, error

    def process_user_list(self):
        a = hemlock.Hemlock()
        m_server = self.connect_mysql("localhost", "testUser", "password", "test_hemlock")
        x, error = a.process_action("user-list", {}, m_server)
        x, error = a.process_action("role-create", {'--name':'role1'}, m_server)
        x, error = a.process_action("tenant-create", {'--name':'tenant1'}, m_server)
        x, error = a.process_action("user-create", {'--name':'user1', '--username':'username1', '--email':'email@dot.com', '--role_id':'asdf', '--tenant_id':'asdf'}, m_server)
        x, error = a.process_action("user-list", {}, m_server)
        x, error = a.process_action("role-create", {'--name':'role1'}, m_server)
        x, error = a.process_action("tenant-create", {'--name':'tenant1'}, m_server)
        x, error = a.process_action("user-create", {'--name':'user1', '--username':'username1', '--email':'email@dot.com', '--role_id':'asdf', '--tenant_id':'asdf'}, m_server)
        x, error = a.process_action("user-list", {}, m_server)
        return x, error

    def process_system_list(self):
        a = hemlock.Hemlock()
        m_server = self.connect_mysql("localhost", "testUser", "password", "test_hemlock")
        x, error = a.process_action("system-list", {}, m_server)
        x, error = a.process_action("tenant-create", {'--name':'tenant1'}, m_server)
        x, error = a.process_action("register-local-system", {'--name':'local-system1', '--data_type':'data-type1', '--description': 'description1', '--tenant_id':'asdf', '--hostname':'hostname1', '--endpoint':'http://endpoint.com/', '--poc_name':'poc-name1', '--poc_email':'poc-email@dot.com'}, m_server)
        x, error = a.process_action("system-list", {}, m_server)
        x, error = a.process_action("tenant-create", {'--name':'tenant1'}, m_server)
        x, error = a.process_action("register-local-system", {'--name':'local-system1', '--data_type':'data-type1', '--description': 'description1', '--tenant_id':'asdf', '--hostname':'hostname1', '--endpoint':'http://endpoint.com/', '--poc_name':'poc-name1', '--poc_email':'poc-email@dot.com'}, m_server)
        x, error = a.process_action("system-list", {}, m_server)
        return x, error

    def process_role_users_list(self):
        a = hemlock.Hemlock()
        m_server = self.connect_mysql("localhost", "testUser", "password", "test_hemlock")
        # !! TODO need to properly fill {}
        # !! TODO need to first create a role, get the uuid, then use that uuid
        x, error = a.process_action("role-create", {'--name':'role1'}, m_server)
        x, error = a.process_action("role-users-list", {'--uuid':'asdf'}, m_server)
        x, error = a.process_action("tenant-create", {'--name':'tenant1'}, m_server)
        x, error = a.process_action("user-create", {'--name':'user1', '--username':'username1', '--email':'email@dot.com', '--role_id':'asdf', '--tenant_id':'asdf'}, m_server)
        x, error = a.process_action("role-users-list", {'--uuid':'asdf'}, m_server)
        x, error = a.process_action("tenant-create", {'--name':'tenant2'}, m_server)
        x, error = a.process_action("user-create", {'--name':'user2', '--username':'username2', '--email':'email@dot.com', '--role_id':'asdf', '--tenant_id':'asdf'}, m_server)
        x, error = a.process_action("role-users-list", {'--uuid':'asdf'}, m_server)
        return x, error

    def process_system_tenants_list(self):
        a = hemlock.Hemlock()
        m_server = self.connect_mysql("localhost", "testUser", "password", "test_hemlock")
        # !! TODO need to properly fill {}
        # !! TODO need to first create a system, get the uuid, then use that uuid
        x, error = a.process_action("tenant-create", {'--name':'tenant1'}, m_server)
        x, error = a.process_action("register-local-system", {'--name':'local-system1', '--data_type':'data-type1', '--description': 'description1', '--tenant_id':'asdf', '--hostname':'hostname1', '--endpoint':'http://endpoint.com/', '--poc_name':'poc-name1', '--poc_email':'poc-email@dot.com'}, m_server)
        x, error = a.process_action("system-tenants-list", {'--uuid':'asdf'}, m_server)
        x, error = a.process_action("tenant-create", {'--name':'tenant1'}, m_server)
        x, error = a.process_action("system-add-tenant", {'--uuid':'asdf', '--tenant_id':'asdf'}, m_server)
        x, error = a.process_action("system-tenants-list", {'--uuid':'asdf'}, m_server)
        return x, error

    def process_tenant_systems_list(self):
        a = hemlock.Hemlock()
        m_server = self.connect_mysql("localhost", "testUser", "password", "test_hemlock")
        # !! TODO need to properly fill {}
        # !! TODO need to first create a tenant, get the uuid, then use that uuid
        x, error = a.process_action("tenant-create", {'--name':'tenant1'}, m_server)
        x, error = a.process_action("tenant-systems-list", {'--uuid':'asdf'}, m_server)
        x, error = a.process_action("register-local-system", {'--name':'local-system1', '--data_type':'data-type1', '--description': 'description1', '--tenant_id':'asdf', '--hostname':'hostname1', '--endpoint':'http://endpoint.com/', '--poc_name':'poc-name1', '--poc_email':'poc-email@dot.com'}, m_server)
        x, error = a.process_action("tenant-systems-list", {'--uuid':'asdf'}, m_server)
        x, error = a.process_action("register-local-system", {'--name':'local-system2', '--data_type':'data-type1', '--description': 'description1', '--tenant_id':'asdf', '--hostname':'hostname1', '--endpoint':'http://endpoint.com/', '--poc_name':'poc-name1', '--poc_email':'poc-email@dot.com'}, m_server)
        x, error = a.process_action("tenant-systems-list", {'--uuid':'asdf'}, m_server)
        return x, error

    def process_tenant_users_list(self):
        a = hemlock.Hemlock()
        m_server = self.connect_mysql("localhost", "testUser", "password", "test_hemlock")
        # !! TODO need to properly fill {}
        # !! TODO need to first create a tenant, get the uuid, then use that uuid
        x, error = a.process_action("tenant-create", {'--name':'tenant1'}, m_server)
        x, error = a.process_action("tenant-users-list", {'--uuid':'asdf'}, m_server)
        x, error = a.process_action("role-create", {'--name':'role1'}, m_server)
        x, error = a.process_action("user-create", {'--name':'user1', '--username':'username1', '--email':'email@dot.com', '--role_id':'asdf', '--tenant_id':'asdf'}, m_server)
        x, error = a.process_action("tenant-users-list", {'--uuid':'asdf'}, m_server)
        x, error = a.process_action("role-create", {'--name':'role2'}, m_server)
        x, error = a.process_action("user-create", {'--name':'user2', '--username':'username2', '--email':'email@dot.com', '--role_id':'asdf', '--tenant_id':'asdf'}, m_server)
        x, error = a.process_action("tenant-users-list", {'--uuid':'asdf'}, m_server)
        return x, error

    def process_user_roles_list(self):
        a = hemlock.Hemlock()
        m_server = self.connect_mysql("localhost", "testUser", "password", "test_hemlock")
        # !! TODO need to properly fill {}
        # !! TODO need to first create a user, get the uuid, then use that uuid
        x, error = a.process_action("tenant-create", {'--name':'tenant1'}, m_server)
        x, error = a.process_action("role-create", {'--name':'role1'}, m_server)
        x, error = a.process_action("user-create", {'--name':'user1', '--username':'username1', '--email':'email@dot.com', '--role_id':'asdf', '--tenant_id':'asdf'}, m_server)
        x, error = a.process_action("user-roles-list", {'--uuid':'asdf'}, m_server)
        x, error = a.process_action("role-create", {'--name':'role1'}, m_server)
        x, error = a.process_action("user-add-role", {'--uuid':'asdf', '--role_id':'asdf'}, m_server)
        x, error = a.process_action("user-roles-list", {'--uuid':'asdf'}, m_server)
        return x, error

    def process_user_tenants_list(self):
        a = hemlock.Hemlock()
        m_server = self.connect_mysql("localhost", "testUser", "password", "test_hemlock")
        # !! TODO need to properly fill {}
        # !! TODO need to first create a user, get the uuid, then use that uuid
        x, error = a.process_action("tenant-create", {'--name':'tenant1'}, m_server)
        x, error = a.process_action("role-create", {'--name':'role1'}, m_server)
        x, error = a.process_action("user-create", {'--name':'user1', '--username':'username1', '--email':'email@dot.com', '--role_id':'asdf', '--tenant_id':'asdf'}, m_server)
        x, error = a.process_action("user-tenants-list", {'--uuid':'asdf'}, m_server)
        x, error = a.process_action("tenant-create", {'--name':'tenant1'}, m_server)
        x, error = a.process_action("user-add-tenant", {'--uuid':'asdf', '--tenant_id':'asdf'}, m_server)
        x, error = a.process_action("user-tenants-list", {'--uuid':'asdf'}, m_server)
        return x, error

    def process_deregister_local_system(self):
        a = hemlock.Hemlock()
        m_server = self.connect_mysql("localhost", "testUser", "password", "test_hemlock")
        # !! TODO need to properly fill {}
        # !! TODO need to first create a system, get the uuid, then deregister that uuid
        x, error = a.process_action("tenant-create", {'--name':'tenant1'}, m_server)
        x, error = a.process_action("register-local-system", {'--name':'local-system1', '--data_type':'data-type1', '--description': 'description1', '--tenant_id':'asdf', '--hostname':'hostname1', '--endpoint':'http://endpoint.com/', '--poc_name':'poc-name1', '--poc_email':'poc-email@dot.com'}, m_server)
        x, error = a.process_action("deregister-local-system", {'--uuid':'asdf'}, m_server)
        return x, error

    def process_deregister_remote_system(self):
        a = hemlock.Hemlock()
        m_server = self.connect_mysql("localhost", "testUser", "password", "test_hemlock")
        # !! TODO need to properly fill {}
        # !! TODO need to first create a system, get the uuid, then deregister that uuid
        x, error = a.process_action("tenant-create", {'--name':'tenant1'}, m_server)
        x, error = a.process_action("register-local-system", {'--name':'local-system1', '--data_type':'data-type1', '--description': 'description1', '--tenant_id':'asdf', '--hostname':'hostname1', '--endpoint':'http://endpoint.com/', '--poc_name':'poc-name1', '--poc_email':'poc-email@dot.com'}, m_server)
        x, error = a.process_action("deregister-remote-system", {'--uuid':'asdf'}, m_server)
        return x, error

    def process_role_delete(self):
        a = hemlock.Hemlock()
        m_server = self.connect_mysql("localhost", "testUser", "password", "test_hemlock")
        # !! TODO need to properly fill {}
        # !! TODO need to first create a role, get the uuid, then delete that uuid
        x, error = a.process_action("role-create", {'--name':'role1'}, m_server)
        x, error = a.process_action("role-delete", {'--uuid':'asdf'}, m_server)
        return x, error

    def process_system_add_tenant(self):
        a = hemlock.Hemlock()
        m_server = self.connect_mysql("localhost", "testUser", "password", "test_hemlock")
        # !! TODO need to properly fill {}
        # !! TODO need to first create a system and tenant, get the uuids, then use those uuids
        x, error = a.process_action("tenant-create", {'--name':'tenant1'}, m_server)
        x, error = a.process_action("register-local-system", {'--name':'local-system1', '--data_type':'data-type1', '--description': 'description1', '--tenant_id':'asdf', '--hostname':'hostname1', '--endpoint':'http://endpoint.com/', '--poc_name':'poc-name1', '--poc_email':'poc-email@dot.com'}, m_server)
        x, error = a.process_action("system-add-tenant", {'--uuid':'asdf', '--tenant_id':'asdf'}, m_server)
        return x, error

    def process_system_get(self):
        a = hemlock.Hemlock()
        m_server = self.connect_mysql("localhost", "testUser", "password", "test_hemlock")
        # !! TODO need to properly fill {}
        # !! TODO need to first create a system, get the uuid, then use that uuid
        x, error = a.process_action("tenant-create", {'--name':'tenant1'}, m_server)
        x, error = a.process_action("register-local-system", {'--name':'local-system1', '--data_type':'data-type1', '--description': 'description1', '--tenant_id':'asdf', '--hostname':'hostname1', '--endpoint':'http://endpoint.com/', '--poc_name':'poc-name1', '--poc_email':'poc-email@dot.com'}, m_server)
        x, error = a.process_action("system-get", {'--uuid':'asdf'}, m_server)
        return x, error

    def process_system_remove_tenant(self):
        a = hemlock.Hemlock()
        m_server = self.connect_mysql("localhost", "testUser", "password", "test_hemlock")
        # !! TODO need to properly fill {}
        # !! TODO need to first create a system and tenant, get the uuids, then use those uuids
        x, error = a.process_action("tenant-create", {'--name':'tenant1'}, m_server)
        x, error = a.process_action("register-local-system", {'--name':'local-system1', '--data_type':'data-type1', '--description': 'description1', '--tenant_id':'asdf', '--hostname':'hostname1', '--endpoint':'http://endpoint.com/', '--poc_name':'poc-name1', '--poc_email':'poc-email@dot.com'}, m_server)
        x, error = a.process_action("system-remove-tenant", {'--uuid':'asdf', '--tenant_id':'asdf'}, m_server)
        return x, error

    def process_tenant_delete(self):
        a = hemlock.Hemlock()
        m_server = self.connect_mysql("localhost", "testUser", "password", "test_hemlock")
        # !! TODO need to properly fill {}
        # !! TODO need to first create a tenant, get the uuid, then use that uuid
        x, error = a.process_action("tenant-delete", {'--uuid':'asdf'}, m_server)
        return x, error

    def process_tenant_get(self):
        a = hemlock.Hemlock()
        m_server = self.connect_mysql("localhost", "testUser", "password", "test_hemlock")
        # !! TODO need to properly fill {}
        # !! TODO need to first create a tenant, get the uuid, then use that uuid
        x, error = a.process_action("tenant-create", {'--name':'tenant1'}, m_server)
        x, error = a.process_action("tenant-get", {'--uuid':'asdf'}, m_server)
        return x, error

    def process_user_add_role(self):
        a = hemlock.Hemlock()
        m_server = self.connect_mysql("localhost", "testUser", "password", "test_hemlock")
        # !! TODO need to properly fill {}
        # !! TODO need to first create a user and role, get the uuids, then use those uuids
        x, error = a.process_action("tenant-create", {'--name':'tenant1'}, m_server)
        x, error = a.process_action("role-create", {'--name':'role1'}, m_server)
        x, error = a.process_action("user-create", {'--name':'user1', '--username':'username1', '--email':'email@dot.com', '--role_id':'asdf', '--tenant_id':'asdf'}, m_server)
        x, error = a.process_action("user-add-role", {'--uuid':'asdf', '--role_id':'asdf'}, m_server)
        return x, error

    def process_user_add_tenant(self):
        a = hemlock.Hemlock()
        m_server = self.connect_mysql("localhost", "testUser", "password", "test_hemlock")
        # !! TODO need to properly fill {}
        # !! TODO need to first create a user and tenant, get the uuids, then use those uuids
        x, error = a.process_action("role-create", {'--name':'role1'}, m_server)
        x, error = a.process_action("tenant-create", {'--name':'tenant1'}, m_server)
        x, error = a.process_action("user-create", {'--name':'user1', '--username':'username1', '--email':'email@dot.com', '--role_id':'asdf', '--tenant_id':'asdf'}, m_server)
        x, error = a.process_action("user-add-tenant", {'--uuid':'asdf', '--tenant_id':'asdf'}, m_server)
        return x, error

    def process_user_delete(self):
        a = hemlock.Hemlock()
        m_server = self.connect_mysql("localhost", "testUser", "password", "test_hemlock")
        # !! TODO need to properly fill {}
        # !! TODO need to first create a user, get the uuid, then use that uuid
        x, error = a.process_action("tenant-create", {'--name':'tenant1'}, m_server)
        x, error = a.process_action("role-create", {'--name':'role1'}, m_server)
        x, error = a.process_action("user-create", {'--name':'user1', '--username':'username1', '--email':'email@dot.com', '--role_id':'asdf', '--tenant_id':'asdf'}, m_server)
        x, error = a.process_action("user-delete", {'--uuid':'asdf'}, m_server)
        return x, error

    def process_user_get(self):
        a = hemlock.Hemlock()
        m_server = self.connect_mysql("localhost", "testUser", "password", "test_hemlock")
        # !! TODO need to properly fill {}
        # !! TODO need to first create a user, get the uuid, then use that uuid
        x, error = a.process_action("tenant-create", {'--name':'tenant1'}, m_server)
        x, error = a.process_action("role-create", {'--name':'role1'}, m_server)
        x, error = a.process_action("user-create", {'--name':'user1', '--username':'username1', '--email':'email@dot.com', '--role_id':'asdf', '--tenant_id':'asdf'}, m_server)
        x, error = a.process_action("user-get", {'--uuid':'asdf'}, m_server)
        return x, error

    def process_user_remove_role(self):
        a = hemlock.Hemlock()
        m_server = self.connect_mysql("localhost", "testUser", "password", "test_hemlock")
        # !! TODO need to properly fill {}
        # !! TODO need to first create a user and role, get the uuids, then use those uuids
        x, error = a.process_action("tenant-create", {'--name':'tenant1'}, m_server)
        x, error = a.process_action("role-create", {'--name':'role1'}, m_server)
        x, error = a.process_action("user-create", {'--name':'user1', '--username':'username1', '--email':'email@dot.com', '--role_id':'asdf', '--tenant_id':'asdf'}, m_server)
        x, error = a.process_action("user-remove-role", {'--uuid':'asdf', 'rold_id':'asdf'}, m_server)
        return x, error

    def process_user_remove_tenant(self):
        a = hemlock.Hemlock()
        m_server = self.connect_mysql("localhost", "testUser", "password", "test_hemlock")
        # !! TODO need to properly fill {}
        # !! TODO need to first create a user and tenant, get the uuids, then use those uuids
        x, error = a.process_action("role-create", {'--name':'role1'}, m_server)
        x, error = a.process_action("tenant-create", {'--name':'tenant1'}, m_server)
        x, error = a.process_action("user-create", {'--name':'user1', '--username':'username1', '--email':'email@dot.com', '--role_id':'asdf', '--tenant_id':'asdf'}, m_server)
        x, error = a.process_action("user-remove-tenant", {'--uuid':'asdf', '--tenant_id':'asdf'}, m_server)
        return x, error

    def connect_mysql(self, server, user, pw, db):
        a = hemlock.Hemlock()
        m_server = a.mysql_server(server, user, pw, db)
        return m_server

    # call tests
    def test_connect_mysql(self):
        m_server = self.connect_mysql("localhost", "testUser", "password", "test_hemlock")
        cur = m_server.cursor()
        cur.execute("DROP TABLE IF EXISTS users_tenants")
        cur.execute("DROP TABLE IF EXISTS users_roles")
        cur.execute("DROP TABLE IF EXISTS systems_tenants")
        cur.execute("DROP TABLE IF EXISTS users")
        cur.execute("DROP TABLE IF EXISTS tenants")
        cur.execute("DROP TABLE IF EXISTS systems")
        cur.execute("DROP TABLE IF EXISTS roles")
        m_server.commit()
        m_server.close()
        assert 1

    def test_process_role_create(self):
        x, y, error = self.process_role_create()
        for err in error:
            assert err == 0
        assert x[1][1] == 'role1'
        a = re.match('[0-f]{8}-[0-f]{4}-[0-f]{4}-[0-f]{4}-[0-f]{12}',x[2][1])
        assert a
        assert len(y)

    def test_process_tenant_create(self):
        x, y, error = self.process_tenant_create()
        for err in error:
            assert err == 0
        assert x[1][1] == 'tenant1'
        a = re.match('[0-f]{8}-[0-f]{4}-[0-f]{4}-[0-f]{4}-[0-f]{12}',x[2][1])
        assert a
        assert len(y)

    def test_process_user_create(self):
        x, y, error = self.process_user_create()
        for err in error:
            assert err == 0
        assert x[1][1] == 'user1'
        assert x[4][1] == 'username1'
        assert x[5][1] == 'email@dot.com'
        a = re.match('[0-f]{8}-[0-f]{4}-[0-f]{4}-[0-f]{4}-[0-f]{12}',x[7][1])
        assert a
        assert len(y)

    def test_process_register_local_system(self):
        #x, y, error = self.process_register_local_system()
        #assert error == 0
        #print "TODO",x
        #print y
        assert 1

    def test_process_register_remote_system(self):
        #x, error = self.process_register_remote_system()
        #assert error == 0
        #print "TODO",x
        assert 1

    def test_process_role_list(self):
        #x, error = self.process_role_list()
        #assert error == 0
        # !! TODO - handle case with nothing, one, and more than one
        #print "TODO",x
        assert 1

    def test_process_tenant_list(self):
        #x, error = self.process_tenant_list()
        #assert error == 0
        # !! TODO - handle case with nothing, one, and more than one
        #print "TODO",x
        assert 1

    def test_process_system_list(self):
        #x, error = self.process_system_list()
        #assert error == 0
        # !! TODO - handle case with nothing, one, and more than one
        #print "TODO",x
        assert 1

    def test_process_user_list(self):
        #x, error = self.process_user_list()
        #assert error == 0
        # !! TODO - handle case with nothing, one, and more than one
        #print "TODO",x
        assert 1

    def test_process_tenant_systems_list(self):
        #x, error = self.process_tenant_systems_list()
        #assert error == 0
        # !! TODO - handle case with nothing, one, and more than one
        #print "TODO",x
        assert 1

    def test_process_tenant_users_list(self):
        #x, error = self.process_tenant_users_list()
        #assert error == 0
        # !! TODO - handle case with nothing, one, and more than one
        #print "TODO",x
        assert 1

    def test_process_system_tenants_list(self):
        #x, error = self.process_system_tenants_list()
        #assert error == 0
        # !! TODO - handle case with nothing, one, and more than one
        #print "TODO",x
        assert 1

    def test_process_role_users_list(self):
        #x, error = self.process_role_users_list()
        #assert error == 0
        # !! TODO - handle case with nothing, one, and more than one
        #print "TODO",x
        assert 1

    def test_process_user_roles_list(self):
        #x, error = self.process_user_roles_list()
        #assert error == 0
        # !! TODO - handle case with nothing, one, and more than one
        #print "TODO",x
        assert 1

    def test_process_user_tenants_list(self):
        #x, error = self.process_user_tenants_list()
        #assert error == 0
        # !! TODO - handle case with nothing, one, and more than one
        #print "TODO",x
        assert 1

    def test_process_deregister_local_system(self):
        #x, error = self.process_deregister_local_system()
        #assert error == 0
        #print "TODO",x
        assert 1

    def test_process_deregister_remote_system(self):
        #x, error = self.process_deregister_remote_system()
        #assert error == 0
        #print "TODO",x
        assert 1

    def test_process_role_delete(self):
        #x, error = self.process_role_delete()
        #assert error == 0
        #print "TODO",x
        assert 1

    def test_process_system_add_tenant(self):
        #x, error = self.process_system_add_tenant()
        #assert error == 0
        #print "TODO",x
        assert 1

    def test_process_system_get(self):
        #x, error = self.process_system_get()
        #assert error == 0
        #print "TODO",x
        assert 1

    def test_process_system_remove_tenant(self):
        #x, error = self.process_system_remove_tenant()
        #assert error == 0
        #print "TODO",x
        assert 1

    def test_process_tenant_delete(self):
        #x, error = self.process_tenant_delete()
        #assert error == 0
        #print "TODO",x
        assert 1

    def test_process_tenant_get(self):
        #x, error = self.process_tenant_get()
        #assert error == 0
        #print "TODO",x
        assert 1

    def test_process_user_add_role(self):
        #x, error = self.process_user_add_role()
        #assert error == 0
        #print "TODO",x
        assert 1

    def test_process_user_add_tenant(self):
        #x, error = self.process_user_add_tenant()
        #assert error == 0
        #print "TODO",x
        assert 1

    def test_process_user_delete(self):
        #x, error = self.process_user_delete()
        #assert error == 0
        #print "TODO",x
        assert 1

    def test_process_user_get(self):
        #x, error = self.process_user_get()
        #assert error == 0
        #print "TODO",x
        assert 1

    def test_process_user_remove_role(self):
        #x, error = self.process_user_remove_role()
        #assert error == 0
        #print "TODO",x
        assert 1

    def test_process_user_remove_tenant(self):
        #x, error = self.process_user_remove_tenant()
        #assert error == 0
        #print "TODO",x
        assert 1
