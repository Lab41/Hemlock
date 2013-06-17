import hemlock
import MySQLdb as mdb

class TestClass:
    def process_deregister_local_system(self):
        a = hemlock.Hemlock()
        return

    def process_deregister_remote_system(self):
        a = hemlock.Hemlock()
        return

    def process_register_local_system(self):
        a = hemlock.Hemlock()
        return

    def process_register_remote_system(self):
        a = hemlock.Hemlock()
        return

    def process_role_create(self):
        a = hemlock.Hemlock()
        return

    def process_role_delete(self):
        a = hemlock.Hemlock()
        return

    def process_role_list(self):
        a = hemlock.Hemlock()
        m_server = self.connect_mysql("localhost", "testUser", "password", "test_hemlock")
        x, error = a.process_action("role-list", {}, m_server)
        return

    def process_role_users_list(self):
        a = hemlock.Hemlock()
        return

    def process_system_add_tenant(self):
        a = hemlock.Hemlock()
        return

    def process_system_get(self):
        a = hemlock.Hemlock()
        return

    def process_system_list(self):
        a = hemlock.Hemlock()
        m_server = self.connect_mysql("localhost", "testUser", "password", "test_hemlock")
        x, error = a.process_action("system-list", {}, m_server)
        return

    def process_system_remove_tenant(self):
        a = hemlock.Hemlock()
        return

    def process_system_tenants_list(self):
        a = hemlock.Hemlock()
        return

    def process_tenant_create(self):
        a = hemlock.Hemlock()
        return

    def process_tenant_delete(self):
        a = hemlock.Hemlock()
        return

    def process_tenant_get(self):
        a = hemlock.Hemlock()
        return

    def process_tenant_list(self):
        a = hemlock.Hemlock()
        m_server = self.connect_mysql("localhost", "testUser", "password", "test_hemlock")
        x, error = a.process_action("tenant-list", {}, m_server)
        return

    def process_tenant_systems_list(self):
        a = hemlock.Hemlock()
        return

    def process_tenant_users_list(self):
        a = hemlock.Hemlock()
        return

    def process_user_add_role(self):
        a = hemlock.Hemlock()
        return

    def process_user_add_tenant(self):
        a = hemlock.Hemlock()
        return

    def process_user_create(self):
        a = hemlock.Hemlock()
        return

    def process_user_delete(self):
        a = hemlock.Hemlock()
        return

    def process_user_get(self):
        a = hemlock.Hemlock()
        return

    def process_user_list(self):
        a = hemlock.Hemlock()
        m_server = self.connect_mysql("localhost", "testUser", "password", "test_hemlock")
        x, error = a.process_action("user-list", {}, m_server)
        return x, error

    def process_user_remove_role(self):
        a = hemlock.Hemlock()
        return

    def process_user_remove_tenant(self):
        a = hemlock.Hemlock()
        return

    def process_user_roles_list(self):
        a = hemlock.Hemlock()
        return

    def process_user_tenants_list(self):
        a = hemlock.Hemlock()
        return

    def connect_mysql(self, server, user, pw, db):
        a = hemlock.Hemlock()
        m_server = a.mysql_server(server, user, pw, db)
        return m_server

    # !! TODO junk test, delete when no longer stubs
    def func(self, x):
        return x + 1

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

    def test_process_deregister_local_system(self):
        assert self.func(3) == 5

    def test_process_deregister_remote_system(self):
        assert self.func(3) == 5

    def test_process_register_local_system(self):
        assert self.func(3) == 5

    def test_process_register_remote_system(self):
        assert self.func(3) == 5

    def test_process_role_create(self):
        assert self.func(3) == 5

    def test_process_role_delete(self):
        assert self.func(3) == 5

    def test_process_role_list(self):
        x, error = self.process_user_list()
        assert error == 0
        # !! TODO - handle case with nothing, one, and more than one
        print "TODO",x
        assert 0

    def test_process_role_users_list(self):
        assert self.func(3) == 5

    def test_process_system_add_tenant(self):
        assert self.func(3) == 5

    def test_process_system_get(self):
        assert self.func(3) == 5

    def test_process_system_list(self):
        x, error = self.process_user_list()
        assert error == 0
        # !! TODO - handle case with nothing, one, and more than one
        print "TODO",x
        assert 0

    def test_process_system_remove_tenant(self):
        assert self.func(3) == 5

    def test_process_system_tenants_list(self):
        assert self.func(3) == 5

    def test_process_tenant_create(self):
        assert self.func(3) == 5

    def test_process_tenant_delete(self):
        assert self.func(3) == 5

    def test_process_tenant_get(self):
        assert self.func(3) == 5

    def test_process_tenant_list(self):
        x, error = self.process_user_list()
        assert error == 0
        # !! TODO - handle case with nothing, one, and more than one
        print "TODO",x
        assert 0

    def test_process_tenant_systems_list(self):
        assert self.func(3) == 5

    def test_process_tenant_users_list(self):
        assert self.func(3) == 5

    def test_process_user_add_role(self):
        assert self.func(3) == 5

    def test_process_user_add_tenant(self):
        assert self.func(3) == 5

    def test_process_user_create(self):
        assert self.func(3) == 5

    def test_process_user_delete(self):
        assert self.func(3) == 5

    def test_process_user_get(self):
        assert self.func(3) == 5

    def test_process_user_list(self):
        x, error = self.process_user_list()
        assert error == 0
        # !! TODO - handle case with nothing, one, and more than one
        print "TODO",x
        assert 0

    def test_process_user_remove_role(self):
        assert self.func(3) == 5

    def test_process_user_remove_tenant(self):
        assert self.func(3) == 5

    def test_process_user_roles_list(self):
        assert self.func(3) == 5

    def test_process_user_tenants_list(self):
        assert 1
