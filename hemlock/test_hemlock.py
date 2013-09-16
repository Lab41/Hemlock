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

"""
Test module for hemlock.py

Created on 19 August 2013
@author: Charlie Lewis
"""

import hemlock, re
import MySQLdb as mdb

class TestClass:
    """
    Test class for hemlock.py
    """
    def process_client_get(self):
        """
        Tests client-get action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        c, error2 = a.process_action(0, "tenant-create", {'--name':'tenant1'}, m_server, "localhost")
        error.append(error2)
        d, error3 = a.process_action(0, "register-local-system", {'--name':'local-system1', '--data_type':'data-type1', '--description': 'description1', '--tenant_id':c[2][1], '--hostname':'hostname1', '--endpoint':'http://endpoint.com/', '--poc_name':'poc-name1', '--poc_email':'poc-email@dot.com'}, m_server, "localhost")
        error.append(error3)
        e, error4 = a.process_action(0, "client-store", {'--name':'client1', '--type':'mysql', '--system_id':d[9][1], '--credential_file':'hemlock/clients/mysql_creds_sample'}, m_server, "localhost")
        error.append(error4)
        x, error5 = a.process_action(0, "client-get", {'--uuid':e[5][1]}, m_server, "localhost")
        error.append(error5)
        return x, error

    def process_client_list(self):
        """
        Tests client-list action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        b, error1 = a.process_action(0, "client-list", {}, m_server, "localhost")
        error.append(error1)
        c, error2 = a.process_action(0, "tenant-create", {'--name':'tenant1'}, m_server, "localhost")
        error.append(error2)
        d, error3 = a.process_action(0, "register-local-system", {'--name':'local-system1', '--data_type':'data-type1', '--description': 'description1', '--tenant_id':c[2][1], '--hostname':'hostname1', '--endpoint':'http://endpoint.com/', '--poc_name':'poc-name1', '--poc_email':'poc-email@dot.com'}, m_server, "localhost")
        error.append(error3)
        e, error4 = a.process_action(0, "client-store", {'--name':'client1', '--type':'mysql', '--system_id':d[9][1], '--credential_file':'hemlock/clients/mysql_creds_sample'}, m_server, "localhost")
        error.append(error4)
        x, error5 = a.process_action(0, "client-list", {}, m_server, "localhost")
        error.append(error5)
        return x, error

    def process_client_purge(self):
        """
        Tests client-purge action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        c, error2 = a.process_action(0, "tenant-create", {'--name':'tenant1'}, m_server, "localhost")
        error.append(error2)
        d, error3 = a.process_action(0, "register-local-system", {'--name':'local-system1', '--data_type':'data-type1', '--description': 'description1', '--tenant_id':c[2][1], '--hostname':'hostname1', '--endpoint':'http://endpoint.com/', '--poc_name':'poc-name1', '--poc_email':'poc-email@dot.com'}, m_server, "localhost")
        error.append(error3)
        e, error4 = a.process_action(0, "client-store", {'--name':'client1', '--type':'mysql', '--system_id':d[9][1], '--credential_file':'hemlock/clients/mysql_creds_sample'}, m_server, "localhost")
        error.append(error4)
        x, error5 = a.process_action(0, "client-purge", {'--uuid':e[5][1]}, m_server, "localhost")
        error.append(error5)
        return x, error

    def process_client_run(self):
        """
        Tests client-run action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        # !! TODO
        x = ""
        return x, error

    def process_client_schedule(self):
        """
        Tests client-schedule action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        # !! TODO
        x = ""
        return x, error

    def process_client_store(self):
        """
        Tests client-store action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        b, error1 = a.process_action(0, "tenant-create", {'--name':'tenant1'}, m_server, "localhost")
        error.append(error1)
        c, error2 = a.process_action(0, "register-local-system", {'--name':'local-system1', '--data_type':'data-type1', '--description': 'description1', '--tenant_id':b[2][1], '--hostname':'hostname1', '--endpoint':'http://endpoint.com/', '--poc_name':'poc-name1', '--poc_email':'poc-email@dot.com'}, m_server, "localhost")
        error.append(error2)
        x, error3 = a.process_action(0, "client-store", {'--name':'client1', '--type':'mysql', '--system_id':c[9][1], '--credential_file':'hemlock/clients/mysql_creds_sample'}, m_server, "localhost")
        error.append(error3)
        cur = m_server.cursor()
        str = "select * from clients where uuid = '"+x[2][1]+"'"
        cur.execute(str)
        y = cur.fetchall()
        return x, y, error

    def process_schedule_get(self):
        """
        Tests schedule-get action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        # !! TODO
        x = ""
        return x, error

    def process_schedule_list(self):
        """
        Tests schedule-list action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        # !! TODO
        x = ""
        return x, error

    def process_role_create(self):
        """
        Tests role-create action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        x, error1 = a.process_action(0, "role-create", {'--name':'role1'}, m_server, "localhost")
        error.append(error1)
        cur = m_server.cursor()
        str = "select * from roles where uuid = '"+x[2][1]+"'"
        cur.execute(str)
        y = cur.fetchall()
        return x, y, error

    def process_tenant_create(self):
        """
        Tests tenant-create action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        x, error1 = a.process_action(0, "tenant-create", {'--name':'tenant1'}, m_server, "localhost")
        error.append(error1)
        cur = m_server.cursor()
        str = "select * from tenants where uuid = '"+x[2][1]+"'"
        cur.execute(str)
        y = cur.fetchall()
        return x, y, error

    def process_user_create(self):
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        b, error1 = a.process_action(0, "role-create", {'--name':'role1'}, m_server, "localhost")
        error.append(error1)
        c, error2 = a.process_action(0, "tenant-create", {'--name':'tenant1'}, m_server, "localhost")
        error.append(error2)
        hemlock.getpass.getpass = lambda _: 'boguspw'
        x, error3 = a.process_action(0, "user-create", {'--name':'user1', '--username':'username1', '--email':'email@dot.com', '--role_id':b[2][1], '--tenant_id':c[2][1]}, m_server, "localhost")
        error.append(error3)
        cur = m_server.cursor()
        str = "select * from users where uuid = '"+x[7][1]+"'"
        cur.execute(str)
        y = cur.fetchall()
        return x, y, error

    def process_register_local_system(self):
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        b, error1 = a.process_action(0, "tenant-create", {'--name':'tenant1'}, m_server, "localhost")
        error.append(error1)
        x, error2 = a.process_action(0, "register-local-system", {'--name':'local-system1', '--data_type':'data-type1', '--description': 'description1', '--tenant_id':b[2][1], '--hostname':'hostname1', '--endpoint':'http://endpoint.com/', '--poc_name':'poc-name1', '--poc_email':'poc-email@dot.com'}, m_server, "localhost")
        error.append(error2)
        cur = m_server.cursor()
        str = "select * from systems where uuid = '"+x[9][1]+"'"
        cur.execute(str)
        y = cur.fetchall()
        return x, y, error

    def process_register_remote_system(self):
        """
        Tests register-remote-system action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        b, error1 = a.process_action(0, "tenant-create", {'--name':'tenant1'}, m_server, "localhost")
        error.append(error1)
        x, error2 = a.process_action(0, "register-remote-system", {'--name':'remote-system1', '--data_type':'data-type1', '--description': 'description1', '--tenant_id':b[2][1], '--hostname':'hostname1', '--port':'80', '--remote_uri':'http://remote.uri/', '--poc_name':'poc-name1', '--poc_email':'poc-email@dot.com'}, m_server, "localhost")
        error.append(error2)
        cur = m_server.cursor()
        str = "select * from systems where uuid = '"+x[10][1]+"'"
        cur.execute(str)
        y = cur.fetchall()
        return x, y, error

    def process_role_list(self):
        """
        Tests role-list action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        b, error1 = a.process_action(0, "role-list", {}, m_server, "localhost")
        error.append(error1)
        c, error2 = a.process_action(0, "role-create", {'--name':'role1'}, m_server, "localhost")
        error.append(error2)
        d, error3 = a.process_action(0, "role-list", {}, m_server, "localhost")
        error.append(error3)
        e, error4 = a.process_action(0, "role-create", {'--name':'role2'}, m_server, "localhost")
        error.append(error4)
        x, error5 = a.process_action(0, "role-list", {}, m_server, "localhost")
        error.append(error5)
        # !! TODO fix what is returned
        return x, error

    def process_tenant_list(self):
        """
        Tests tenant-list action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        b, error1 = a.process_action(0, "tenant-list", {}, m_server, "localhost")
        error.append(error1)
        c, error2 = a.process_action(0, "tenant-create", {'--name':'tenant1'}, m_server, "localhost")
        error.append(error2)
        d, error3 = a.process_action(0, "tenant-list", {}, m_server, "localhost")
        error.append(error3)
        e, error4 = a.process_action(0, "tenant-create", {'--name':'tenant2'}, m_server, "localhost")
        error.append(error4)
        x, error5 = a.process_action(0, "tenant-list", {}, m_server, "localhost")
        error.append(error5)
        # !! TODO fix what is returned
        return x, error

    def process_user_list(self):
        """
        Tests user-list action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        b, error1 = a.process_action(0, "user-list", {}, m_server, "localhost")
        error.append(error1)
        c, error2 = a.process_action(0, "role-create", {'--name':'role1'}, m_server, "localhost")
        error.append(error2)
        d, error3 = a.process_action(0, "tenant-create", {'--name':'tenant1'}, m_server, "localhost")
        error.append(error3)
        hemlock.getpass.getpass = lambda _: 'boguspw'
        e, error4 = a.process_action(0, "user-create", {'--name':'user1', '--username':'username1', '--email':'email@dot.com', '--role_id':c[2][1], '--tenant_id':d[2][1]}, m_server, "localhost")
        error.append(error4)
        f, error5 = a.process_action(0, "user-list", {}, m_server, "localhost")
        error.append(error5)
        g, error6 = a.process_action(0, "role-create", {'--name':'role2'}, m_server, "localhost")
        error.append(error6)
        h, error7 = a.process_action(0, "tenant-create", {'--name':'tenant2'}, m_server, "localhost")
        error.append(error7)
        hemlock.getpass.getpass = lambda _: 'boguspw'
        i, error8 = a.process_action(0, "user-create", {'--name':'user1', '--username':'username1', '--email':'email@dot.com', '--role_id':g[2][1], '--tenant_id':h[2][1]}, m_server, "localhost")
        error.append(error8)
        x, error9 = a.process_action(0, "user-list", {}, m_server, "localhost")
        error.append(error9)
        # !! TODO fix what is returned
        return x, error

    def process_system_list(self):
        """
        Tests system-list action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        b, error1 = a.process_action(0, "system-list", {}, m_server, "localhost")
        error.append(error1)
        c, error2 = a.process_action(0, "tenant-create", {'--name':'tenant1'}, m_server, "localhost")
        error.append(error2)
        d, error3 = a.process_action(0, "register-local-system", {'--name':'local-system1', '--data_type':'data-type1', '--description': 'description1', '--tenant_id':c[2][1], '--hostname':'hostname1', '--endpoint':'http://endpoint.com/', '--poc_name':'poc-name1', '--poc_email':'poc-email@dot.com'}, m_server, "localhost")
        error.append(error3)
        e, error4 = a.process_action(0, "system-list", {}, m_server, "localhost")
        error.append(error4)
        f, error5 = a.process_action(0, "tenant-create", {'--name':'tenant2'}, m_server, "localhost")
        error.append(error5)
        g, error6 = a.process_action(0, "register-local-system", {'--name':'local-system1', '--data_type':'data-type1', '--description': 'description1', '--tenant_id':f[2][1], '--hostname':'hostname1', '--endpoint':'http://endpoint.com/', '--poc_name':'poc-name1', '--poc_email':'poc-email@dot.com'}, m_server, "localhost")
        error.append(error6)
        x, error7 = a.process_action(0, "system-list", {}, m_server, "localhost")
        error.append(error7)
        # !! TODO fix what is returned
        return x, error

    def process_list_all(self):
        """
        Tests list-all action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        b, error1 = a.process_action(0, "list-all", {}, m_server, "localhost")
        error.append(error1)
        c, error2 = a.process_action(0, "role-create", {'--name':'role1'}, m_server, "localhost")
        error.append(error2)
        d, error3 = a.process_action(0, "tenant-create", {'--name':'tenant1'}, m_server, "localhost")
        error.append(error3)
        hemlock.getpass.getpass = lambda _: 'boguspw'
        e, error4 = a.process_action(0, "user-create", {'--name':'user1', '--username':'username1', '--email':'email@dot.com', '--role_id':c[2][1], '--tenant_id':d[2][1]}, m_server, "localhost")
        error.append(error4)
        f, error5 = a.process_action(0, "tenant-create", {'--name':'tenant2'}, m_server, "localhost")
        error.append(error5)
        x, error6 = a.process_action(0, "register-local-system", {'--name':'local-system1', '--data_type':'data-type1', '--description': 'description1', '--tenant_id':f[2][1], '--hostname':'hostname1', '--endpoint':'http://endpoint.com/', '--poc_name':'poc-name1', '--poc_email':'poc-email@dot.com'}, m_server, "localhost")
        error.append(error6)
        # !! TODO fix what is returned
        return x, error

    def process_role_users_list(self):
        """
        Tests role-users-list action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        b, error1 = a.process_action(0, "role-create", {'--name':'role1'}, m_server, "localhost")
        error.append(error1)
        c, error2 = a.process_action(0, "role-users-list", {'--uuid':b[2][1]}, m_server, "localhost")
        error.append(error2)
        d, error3 = a.process_action(0, "tenant-create", {'--name':'tenant1'}, m_server, "localhost")
        error.append(error3)
        hemlock.getpass.getpass = lambda _: 'boguspw'
        e, error4 = a.process_action(0, "user-create", {'--name':'user1', '--username':'username1', '--email':'email@dot.com', '--role_id':b[2][1], '--tenant_id':d[2][1]}, m_server, "localhost")
        error.append(error4)
        f, error5 = a.process_action(0, "role-users-list", {'--uuid':b[2][1]}, m_server, "localhost")
        error.append(error5)
        g, error6 = a.process_action(0, "tenant-create", {'--name':'tenant2'}, m_server, "localhost")
        error.append(error6)
        hemlock.getpass.getpass = lambda _: 'boguspw'
        h, error7 = a.process_action(0, "user-create", {'--name':'user2', '--username':'username2', '--email':'email@dot.com', '--role_id':b[2][1], '--tenant_id':g[2][1]}, m_server, "localhost")
        error.append(error7)
        x, error8 = a.process_action(0, "role-users-list", {'--uuid':b[2][1]}, m_server, "localhost")
        error.append(error8)
        # !! TODO fix what is returned
        return x, error

    def process_system_tenants_list(self):
        """
        Tests system-tenants-list action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        b, error1 = a.process_action(0, "tenant-create", {'--name':'tenant1'}, m_server, "localhost")
        error.append(error1)
        c, error2 = a.process_action(0, "register-local-system", {'--name':'local-system1', '--data_type':'data-type1', '--description': 'description1', '--tenant_id':b[2][1], '--hostname':'hostname1', '--endpoint':'http://endpoint.com/', '--poc_name':'poc-name1', '--poc_email':'poc-email@dot.com'}, m_server, "localhost")
        error.append(error2)
        d, error3 = a.process_action(0, "system-tenants-list", {'--uuid':c[9][1]}, m_server, "localhost")
        error.append(error3)
        e, error4 = a.process_action(0, "tenant-create", {'--name':'tenant2'}, m_server, "localhost")
        error.append(error4)
        f, error5 = a.process_action(0, "system-add-tenant", {'--uuid':c[9][1], '--tenant_id':e[2][1]}, m_server, "localhost")
        error.append(error5)
        x, error6 = a.process_action(0, "system-tenants-list", {'--uuid':c[9][1]}, m_server, "localhost")
        error.append(error6)
        # !! TODO fix what is returned
        return x, error

    def process_tenant_systems_list(self):
        """
        Tests tenant-systems-list action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        b, error1 = a.process_action(0, "tenant-create", {'--name':'tenant1'}, m_server, "localhost")
        error.append(error1)
        c, error2 = a.process_action(0, "tenant-systems-list", {'--uuid':b[2][1]}, m_server, "localhost")
        error.append(error2)
        d, error3 = a.process_action(0, "register-local-system", {'--name':'local-system1', '--data_type':'data-type1', '--description': 'description1', '--tenant_id':b[2][1], '--hostname':'hostname1', '--endpoint':'http://endpoint.com/', '--poc_name':'poc-name1', '--poc_email':'poc-email@dot.com'}, m_server, "localhost")
        error.append(error3)
        e, error4 = a.process_action(0, "tenant-systems-list", {'--uuid':b[2][1]}, m_server, "localhost")
        error.append(error4)
        f, error5 = a.process_action(0, "register-local-system", {'--name':'local-system2', '--data_type':'data-type1', '--description': 'description1', '--tenant_id':b[2][1], '--hostname':'hostname1', '--endpoint':'http://endpoint.com/', '--poc_name':'poc-name1', '--poc_email':'poc-email@dot.com'}, m_server, "localhost")
        error.append(error5)
        x, error6 = a.process_action(0, "tenant-systems-list", {'--uuid':b[2][1]}, m_server, "localhost")
        error.append(error6)
        # !! TODO fix what is returned
        return x, error

    def process_tenant_users_list(self):
        """
        Tests tenant-users-list action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        b, error1 = a.process_action(0, "tenant-create", {'--name':'tenant1'}, m_server, "localhost")
        error.append(error1)
        c, error2 = a.process_action(0, "tenant-users-list", {'--uuid':b[2][1]}, m_server, "localhost")
        error.append(error2)
        d, error3 = a.process_action(0, "role-create", {'--name':'role1'}, m_server, "localhost")
        error.append(error3)
        hemlock.getpass.getpass = lambda _: 'boguspw'
        e, error4 = a.process_action(0, "user-create", {'--name':'user1', '--username':'username1', '--email':'email@dot.com', '--role_id':d[2][1], '--tenant_id':b[2][1]}, m_server, "localhost")
        error.append(error4)
        f, error5 = a.process_action(0, "tenant-users-list", {'--uuid':b[2][1]}, m_server, "localhost")
        error.append(error5)
        g, error6 = a.process_action(0, "role-create", {'--name':'role2'}, m_server, "localhost")
        error.append(error6)
        hemlock.getpass.getpass = lambda _: 'boguspw'
        h, error7 = a.process_action(0, "user-create", {'--name':'user2', '--username':'username2', '--email':'email@dot.com', '--role_id':g[2][1], '--tenant_id':b[2][1]}, m_server, "localhost")
        error.append(error7)
        x, error8 = a.process_action(0, "tenant-users-list", {'--uuid':b[2][1]}, m_server, "localhost")
        error.append(error8)
        # !! TODO fix what is returned
        return x, error

    def process_user_roles_list(self):
        """
        Tests user-roles-list action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        b, error1 = a.process_action(0, "tenant-create", {'--name':'tenant1'}, m_server, "localhost")
        error.append(error1)
        c, error2 = a.process_action(0, "role-create", {'--name':'role1'}, m_server, "localhost")
        error.append(error2)
        hemlock.getpass.getpass = lambda _: 'boguspw'
        d, error3 = a.process_action(0, "user-create", {'--name':'user1', '--username':'username1', '--email':'email@dot.com', '--role_id':c[2][1], '--tenant_id':b[2][1]}, m_server, "localhost")
        error.append(error3)
        e, error4 = a.process_action(0, "user-roles-list", {'--uuid':d[7][1]}, m_server, "localhost")
        error.append(error4)
        f, error5 = a.process_action(0, "role-create", {'--name':'role2'}, m_server, "localhost")
        error.append(error5)
        g, error6 = a.process_action(0, "user-add-role", {'--uuid':d[7][1], '--role_id':f[2][1]}, m_server, "localhost")
        error.append(error6)
        x, error7 = a.process_action(0, "user-roles-list", {'--uuid':d[7][1]}, m_server, "localhost")
        error.append(error7)
        # !! TODO fix what is returned
        return x, error

    def process_user_tenants_list(self):
        """
        Tests user-tenants-list action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        b, error1 = a.process_action(0, "tenant-create", {'--name':'tenant1'}, m_server, "localhost")
        error.append(error1)
        c, error2 = a.process_action(0, "role-create", {'--name':'role1'}, m_server, "localhost")
        error.append(error2)
        hemlock.getpass.getpass = lambda _: 'boguspw'
        d, error3 = a.process_action(0, "user-create", {'--name':'user1', '--username':'username1', '--email':'email@dot.com', '--role_id':c[2][1], '--tenant_id':b[2][1]}, m_server, "localhost")
        error.append(error3)
        e, error4 = a.process_action(0, "user-tenants-list", {'--uuid':d[7][1]}, m_server, "localhost")
        error.append(error4)
        f, error5 = a.process_action(0, "tenant-create", {'--name':'tenant2'}, m_server, "localhost")
        error.append(error5)
        g, error6 = a.process_action(0, "user-add-tenant", {'--uuid':d[7][1], '--tenant_id':f[2][1]}, m_server, "localhost")
        error.append(error6)
        x, error7 = a.process_action(0, "user-tenants-list", {'--uuid':d[7][1]}, m_server, "localhost")
        error.append(error7)
        # !! TODO fix what is returned
        return x, error

    def process_deregister_local_system(self):
        """
        Tests deregister-local-system action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        b, error1 = a.process_action(0, "tenant-create", {'--name':'tenant1'}, m_server, "localhost")
        error.append(error1)
        c, error2 = a.process_action(0, "register-local-system", {'--name':'local-system1', '--data_type':'data-type1', '--description': 'description1', '--tenant_id':b[2][1], '--hostname':'hostname1', '--endpoint':'http://endpoint.com/', '--poc_name':'poc-name1', '--poc_email':'poc-email@dot.com'}, m_server, "localhost")
        error.append(error2)
        x, error3 = a.process_action(0, "deregister-local-system", {'--uuid':c[9][1]}, m_server, "localhost")
        error.append(error3)
        # !! TODO fix what is returned
        return x, error

    def process_deregister_remote_system(self):
        """
        Tests deregister-remote-system action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        b, error1 = a.process_action(0, "tenant-create", {'--name':'tenant1'}, m_server, "localhost")
        error.append(error1)
        c, error2 = a.process_action(0, "register-local-system", {'--name':'local-system1', '--data_type':'data-type1', '--description': 'description1', '--tenant_id':b[2][1], '--hostname':'hostname1', '--endpoint':'http://endpoint.com/', '--poc_name':'poc-name1', '--poc_email':'poc-email@dot.com'}, m_server, "localhost")
        error.append(error2)
        x, error3 = a.process_action(0, "deregister-remote-system", {'--uuid':c[9][1]}, m_server, "localhost")
        error.append(error3)
        # !! TODO fix what is returned
        return x, error

    def process_role_delete(self):
        """
        Tests role-delete action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        b, error1 = a.process_action(0, "role-create", {'--name':'role1'}, m_server, "localhost")
        error.append(error1)
        x, error2 = a.process_action(0, "role-delete", {'--uuid':b[2][1]}, m_server, "localhost")
        error.append(error2)
        # !! TODO fix what is returned
        return x, error

    def process_system_add_tenant(self):
        """
        Tests system-add-tenant action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        b, error1 = a.process_action(0, "tenant-create", {'--name':'tenant1'}, m_server, "localhost")
        error.append(error1)
        c, error2 = a.process_action(0, "register-local-system", {'--name':'local-system1', '--data_type':'data-type1', '--description': 'description1', '--tenant_id':b[2][1], '--hostname':'hostname1', '--endpoint':'http://endpoint.com/', '--poc_name':'poc-name1', '--poc_email':'poc-email@dot.com'}, m_server, "localhost")
        error.append(error2)
        d, error3 = a.process_action(0, "tenant-create", {'--name':'tenant2'}, m_server, "localhost")
        error.append(error3)
        x, error4 = a.process_action(0, "system-add-tenant", {'--uuid':c[9][1], '--tenant_id':d[2][1]}, m_server, "localhost")
        error.append(error4)
        # !! TODO fix what is returned
        return x, error

    def process_system_get(self):
        """
        Tests system-get action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        b, error1 = a.process_action(0, "tenant-create", {'--name':'tenant1'}, m_server, "localhost")
        error.append(error1)
        c, error2 = a.process_action(0, "register-local-system", {'--name':'local-system1', '--data_type':'data-type1', '--description': 'description1', '--tenant_id':b[2][1], '--hostname':'hostname1', '--endpoint':'http://endpoint.com/', '--poc_name':'poc-name1', '--poc_email':'poc-email@dot.com'}, m_server, "localhost")
        error.append(error2)
        x, error3 = a.process_action(0, "system-get", {'--uuid':c[9][1]}, m_server, "localhost")
        error.append(error3)
        # !! TODO fix what is returned
        return x, error

    def process_system_remove_tenant(self):
        """
        Tests system-remove-tenant action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        b, error1 = a.process_action(0, "tenant-create", {'--name':'tenant1'}, m_server, "localhost")
        error.append(error1)
        c, error2 = a.process_action(0, "register-local-system", {'--name':'local-system1', '--data_type':'data-type1', '--description': 'description1', '--tenant_id':b[2][1], '--hostname':'hostname1', '--endpoint':'http://endpoint.com/', '--poc_name':'poc-name1', '--poc_email':'poc-email@dot.com'}, m_server, "localhost")
        error.append(error2)
        #d, error3 = a.process_action(0, "system-remove-tenant", {'--uuid':c[9][1], '--tenant_id':b[2][1]}, m_server)
        #error.append(error3)
        e, error4 = a.process_action(0, "tenant-create", {'--name':'tenant2'}, m_server, "localhost")
        error.append(error4)
        f, error5 = a.process_action(0, "system-add-tenant", {'--uuid':c[9][1], '--tenant_id':e[2][1]}, m_server, "localhost")
        error.append(error5)
        x, error6 = a.process_action(0, "system-remove-tenant", {'--uuid':c[9][1], '--tenant_id':e[2][1]}, m_server, "localhost")
        error.append(error6)
        # !! TODO fix what is returned
        return x, error

    def process_tenant_delete(self):
        """
        Tests tenant-delete action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        b, error1 = a.process_action(0, "tenant-create", {'--name':'tenant1'}, m_server, "localhost")
        error.append(error1)
        x, error2 = a.process_action(0, "tenant-delete", {'--uuid':b[2][1]}, m_server, "localhost")
        error.append(error2)
        # !! TODO fix what is returned
        return x, error

    def process_tenant_get(self):
        """
        Tests tenant-get action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        b, error1 = a.process_action(0, "tenant-create", {'--name':'tenant1'}, m_server, "localhost")
        error.append(error1)
        x, error2 = a.process_action(0, "tenant-get", {'--uuid':b[2][1]}, m_server, "localhost")
        error.append(error2)
        # !! TODO fix what is returned
        return x, error

    def process_user_add_role(self):
        """
        Tests user-add-role action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        b, error1 = a.process_action(0, "tenant-create", {'--name':'tenant1'}, m_server, "localhost")
        error.append(error1)
        c, error2 = a.process_action(0, "role-create", {'--name':'role1'}, m_server, "localhost")
        error.append(error2)
        hemlock.getpass.getpass = lambda _: 'boguspw'
        d, error3 = a.process_action(0, "user-create", {'--name':'user1', '--username':'username1', '--email':'email@dot.com', '--role_id':c[2][1], '--tenant_id':b[2][1]}, m_server, "localhost")
        error.append(error3)
        e, error4 = a.process_action(0, "role-create", {'--name':'role2'}, m_server, "localhost")
        error.append(error4)
        x, error5 = a.process_action(0, "user-add-role", {'--uuid':d[7][1], '--role_id':e[2][1]}, m_server, "localhost")
        error.append(error5)
        # !! TODO fix what is returned
        return x, error

    def process_user_add_tenant(self):
        """
        Tests user-add-tenant action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        b, error1 = a.process_action(0, "role-create", {'--name':'role1'}, m_server, "localhost")
        error.append(error1)
        c, error2 = a.process_action(0, "tenant-create", {'--name':'tenant1'}, m_server, "localhost")
        error.append(error2)
        hemlock.getpass.getpass = lambda _: 'boguspw'
        d, error3 = a.process_action(0, "user-create", {'--name':'user1', '--username':'username1', '--email':'email@dot.com', '--role_id':b[2][1], '--tenant_id':c[2][1]}, m_server, "localhost")
        error.append(error3)
        e, error4 = a.process_action(0, "tenant-create", {'--name':'tenant2'}, m_server, "localhost")
        error.append(error4)
        x, error5 = a.process_action(0, "user-add-tenant", {'--uuid':d[7][1], '--tenant_id':e[2][1]}, m_server, "localhost")
        error.append(error5)
        # !! TODO fix what is returned
        return x, error

    def process_user_delete(self):
        """
        Tests user-delete action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        b, error1 = a.process_action(0, "tenant-create", {'--name':'tenant1'}, m_server, "localhost")
        error.append(error1)
        c, error2 = a.process_action(0, "role-create", {'--name':'role1'}, m_server, "localhost")
        error.append(error2)
        hemlock.getpass.getpass = lambda _: 'boguspw'
        d, error3 = a.process_action(0, "user-create", {'--name':'user1', '--username':'username1', '--email':'email@dot.com', '--role_id':c[2][1], '--tenant_id':b[2][1]}, m_server, "localhost")
        error.append(error3)
        x, error4 = a.process_action(0, "user-delete", {'--uuid':d[7][1]}, m_server, "localhost")
        error.append(error4)
        # !! TODO fix what is returned
        return x, error

    def process_user_get(self):
        """
        Tests user-get action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        b, error1 = a.process_action(0, "tenant-create", {'--name':'tenant1'}, m_server, "localhost")
        error.append(error1)
        c, error2 = a.process_action(0, "role-create", {'--name':'role1'}, m_server, "localhost")
        error.append(error2)
        hemlock.getpass.getpass = lambda _: 'boguspw'
        d, error3 = a.process_action(0, "user-create", {'--name':'user1', '--username':'username1', '--email':'email@dot.com', '--role_id':c[2][1], '--tenant_id':b[2][1]}, m_server, "localhost")
        error.append(error3)
        x, error4 = a.process_action(0, "user-get", {'--uuid':d[7][1]}, m_server, "localhost")
        error.append(error4)
        # !! TODO fix what is returned
        return x, error

    def process_user_remove_role(self):
        """
        Tests user-remove-role action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        b, error1 = a.process_action(0, "tenant-create", {'--name':'tenant1'}, m_server, "localhost")
        error.append(error1)
        c, error2 = a.process_action(0, "role-create", {'--name':'role1'}, m_server, "localhost")
        error.append(error2)
        hemlock.getpass.getpass = lambda _: 'boguspw'
        d, error3 = a.process_action(0, "user-create", {'--name':'user1', '--username':'username1', '--email':'email@dot.com', '--role_id':c[2][1], '--tenant_id':b[2][1]}, m_server, "localhost")
        error.append(error3)
        #e, error4 = a.process_action(0, "user-remove-role", {'--uuid':d[7][1], '--role_id':c[2][1]}, m_server)
        #error.append(error4)
        f, error5 = a.process_action(0, "role-create", {'--name':'role2'}, m_server, "localhost")
        error.append(error5)
        g, error6 = a.process_action(0, "user-add-role", {'--uuid':d[7][1], '--role_id':f[2][1]}, m_server, "localhost")
        error.append(error6)
        x, error7 = a.process_action(0, "user-remove-role", {'--uuid':d[7][1], '--role_id':f[2][1]}, m_server, "localhost")
        error.append(error7)
        # !! TODO fix what is returned
        return x, error

    def process_user_remove_tenant(self):
        """
        Tests user-remove-tenant action.

        :return: returns any data and a list of any errors
        """
        error = []
        a = hemlock.Hemlock()
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        b, error1 = a.process_action(0, "role-create", {'--name':'role1'}, m_server, "localhost")
        error.append(error1)
        c, error2 = a.process_action(0, "tenant-create", {'--name':'tenant1'}, m_server, "localhost")
        error.append(error2)
        hemlock.getpass.getpass = lambda _: 'boguspw'
        d, error3 = a.process_action(0, "user-create", {'--name':'user1', '--username':'username1', '--email':'email@dot.com', '--role_id':b[2][1], '--tenant_id':c[2][1]}, m_server, "localhost")
        error.append(error3)
        #e, error4 = a.process_action(0, "user-remove-tenant", {'--uuid':d[7][1], '--tenant_id':c[2][1]}, m_server)
        #error.append(error4)
        f, error5 = a.process_action(0, "tenant-create", {'--name':'tenant2'}, m_server, "localhost")
        error.append(error5)
        g, error6 = a.process_action(0, "user-add-tenant", {'--uuid':d[7][1], '--tenant_id':f[2][1]}, m_server, "localhost")
        error.append(error6)
        x, error7 = a.process_action(0, "user-remove-tenant", {'--uuid':d[7][1], '--tenant_id':f[2][1]}, m_server, "localhost")
        error.append(error7)
        # !! TODO fix what is returned
        return x, error

    def process_start_scheduler(self):
        """
        Tests start-scheduler action.

        :return: returns any data and a list of any errors
        """
        x = ""
        error = ""
        return x, error

    def process_query_data(self):
        """
        Tests query-data action.

        :return: returns any data and a list of any errors
        """
        x = ""
        error = ""
        return x, error

    def connect_mysql(self, debug, server, user, pw, db):
        """
        Makes a connection to the test Hemlock MySQL server.

        :return: returns an instance of the MySQL connection
        """
        a = hemlock.Hemlock()
        m_server = a.mysql_server(debug, server, user, pw, db)
        return m_server

    # call tests
    def test_connect_mysql(self):
        """
        Calls the test function for connecting to MySQL.
        """
        m_server = self.connect_mysql(0, "localhost", "travis", "", "hemlock_test")
        cur = m_server.cursor()
        cur.execute("DROP TABLE IF EXISTS users_tenants")
        cur.execute("DROP TABLE IF EXISTS users_roles")
        cur.execute("DROP TABLE IF EXISTS systems_tenants")
        cur.execute("DROP TABLE IF EXISTS systems_clients")
        cur.execute("DROP TABLE IF EXISTS schedules_clients")
        cur.execute("DROP TABLE IF EXISTS users")
        cur.execute("DROP TABLE IF EXISTS tenants")
        cur.execute("DROP TABLE IF EXISTS systems")
        cur.execute("DROP TABLE IF EXISTS roles")
        cur.execute("DROP TABLE IF EXISTS schedules")
        cur.execute("DROP TABLE IF EXISTS hemlock_server")
        cur.execute("DROP TABLE IF EXISTS clients")
        m_server.commit()
        m_server.close()
        assert 1

    def test_process_role_create(self):
        """
        Calls the test function for the role-create action.
        """
        x, y, error = self.process_role_create()
        for err in error:
            assert err == 0
        assert x[1][1] == 'role1'
        a = re.match('[0-f]{8}-[0-f]{4}-[0-f]{4}-[0-f]{4}-[0-f]{12}',x[2][1])
        assert a
        assert len(y)

    def test_process_tenant_create(self):
        """
        Calls the test function for the tenant-create action.
        """
        x, y, error = self.process_tenant_create()
        for err in error:
            assert err == 0
        assert x[1][1] == 'tenant1'
        a = re.match('[0-f]{8}-[0-f]{4}-[0-f]{4}-[0-f]{4}-[0-f]{12}',x[2][1])
        assert a
        assert len(y)

    def test_process_user_create(self):
        """
        Calls the test function for the user-create action.
        """
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
        """
        Calls the test function for the register-local-system action.
        """
        x, y, error = self.process_register_local_system()
        for err in error:
            assert err == 0
        assert x[2][1] == 'data-type1'
        assert x[3][1] == 'hostname1'
        assert x[4][1] == 'poc-name1'
        assert x[5][1] == 'local-system1'
        assert x[6][1] == 'poc-email@dot.com'
        assert x[7][1] == 'http://endpoint.com/'
        assert x[8][1] == 'description1'
        assert x[11][1] == '0'
        a = re.match('[0-f]{8}-[0-f]{4}-[0-f]{4}-[0-f]{4}-[0-f]{12}',x[9][1])
        assert a
        assert len(y)

    def test_process_register_remote_system(self):
        """
        Calls the test function for the register-remote-system action.
        """
        x, y, error = self.process_register_remote_system()
        for err in error:
            assert err == 0
        assert x[2][1] == 'data-type1'
        assert x[3][1] == 'hostname1'
        assert x[4][1] == 'poc-name1'
        assert x[5][1] == '80'
        assert x[6][1] == 'http://remote.uri/'
        assert x[7][1] == 'remote-system1'
        assert x[8][1] == 'poc-email@dot.com'
        assert x[9][1] == 'description1'
        assert x[12][1] == '1'
        a = re.match('[0-f]{8}-[0-f]{4}-[0-f]{4}-[0-f]{4}-[0-f]{12}',x[10][1])
        assert a
        assert len(y)

    def test_process_role_list(self):
        """
        Calls the test function for the role-list action.
        """
        x, error = self.process_role_list()
        # !! TODO - handle case with nothing, one, and more than one
        for err in error:
            assert err == 0

    def test_process_tenant_list(self):
        """
        Calls the test function for the tenant-list action.
        """
        x, error = self.process_tenant_list()
        # !! TODO - handle case with nothing, one, and more than one
        for err in error:
            assert err == 0

    def test_process_system_list(self):
        """
        Calls the test function for the system-list action.
        """
        x, error = self.process_system_list()
        # !! TODO - handle case with nothing, one, and more than one
        for err in error:
            assert err == 0

    def test_process_user_list(self):
        """
        Calls the test function for the user-list action.
        """
        x, error = self.process_user_list()
        # !! TODO - handle case with nothing, one, and more than one
        for err in error:
            assert err == 0

    def test_process_tenant_systems_list(self):
        """
        Calls the test function for the tenant-systems-list action.
        """
        x, error = self.process_tenant_systems_list()
        # !! TODO - handle case with nothing, one, and more than one
        for err in error:
            assert err == 0

    def test_process_tenant_users_list(self):
        """
        Calls the test function for the tenant-users-list action.
        """
        x, error = self.process_tenant_users_list()
        # !! TODO - handle case with nothing, one, and more than one
        for err in error:
            assert err == 0

    def test_process_system_tenants_list(self):
        """
        Calls the test function for the system-tenants-list action.
        """
        x, error = self.process_system_tenants_list()
        # !! TODO - handle case with nothing, one, and more than one
        for err in error:
            assert err == 0

    def test_process_role_users_list(self):
        """
        Calls the test function for the role-users-list action.
        """
        x, error = self.process_role_users_list()
        # !! TODO - handle case with nothing, one, and more than one
        for err in error:
            assert err == 0

    def test_process_user_roles_list(self):
        """
        Calls the test function for the user-roles-list action.
        """
        x, error = self.process_user_roles_list()
        # !! TODO - handle case with nothing, one, and more than one
        for err in error:
            assert err == 0

    def test_process_user_tenants_list(self):
        """
        Calls the test function for the user-tenants-list action.
        """
        x, error = self.process_user_tenants_list()
        # !! TODO - handle case with nothing, one, and more than one
        for err in error:
            assert err == 0

    def test_process_deregister_local_system(self):
        """
        Calls the test function for the deregister-local-system action.
        """
        x, error = self.process_deregister_local_system()
        for err in error:
            assert err == 0

    def test_process_deregister_remote_system(self):
        """
        Calls the test function for the deregister-remote-system action.
        """
        x, error = self.process_deregister_remote_system()
        for err in error:
            assert err == 0

    def test_process_role_delete(self):
        """
        Calls the test function for the role-delete action.
        """
        x, error = self.process_role_delete()
        for err in error:
            assert err == 0

    def test_process_system_add_tenant(self):
        """
        Calls the test function for the system-add-tenant action.
        """
        x, error = self.process_system_add_tenant()
        for err in error:
            assert err == 0

    def test_process_system_get(self):
        """
        Calls the test function for the system-get action.
        """
        x, error = self.process_system_get()
        for err in error:
            assert err == 0

    def test_process_system_remove_tenant(self):
        """
        Calls the test function for the system-remove-tenant action.
        """
        x, error = self.process_system_remove_tenant()
        for err in error:
            assert err == 0

    def test_process_tenant_delete(self):
        """
        Calls the test function for the tenant-delete action.
        """
        x, error = self.process_tenant_delete()
        for err in error:
            assert err == 0

    def test_process_tenant_get(self):
        """
        Calls the test function for the tenant-get action.
        """
        x, error = self.process_tenant_get()
        for err in error:
            assert err == 0

    def test_process_user_add_role(self):
        """
        Calls the test function for the user-add-role action.
        """
        x, error = self.process_user_add_role()
        for err in error:
            assert err == 0

    def test_process_user_add_tenant(self):
        """
        Calls the test function for the user-add-tenant action.
        """
        x, error = self.process_user_add_tenant()
        for err in error:
            assert err == 0

    def test_process_user_delete(self):
        """
        Calls the test function for the user-delete action.
        """
        x, error = self.process_user_delete()
        for err in error:
            assert err == 0

    def test_process_user_get(self):
        """
        Calls the test function for the user-get action.
        """
        x, error = self.process_user_get()
        for err in error:
            assert err == 0

    def test_process_user_remove_role(self):
        """
        Calls the test function for the user-remove-role action.
        """
        x, error = self.process_user_remove_role()
        for err in error:
           assert err == 0

    def test_process_user_remove_tenant(self):
        """
        Calls the test function for the user-remove-tenant action.
        """
        x, error = self.process_user_remove_tenant()
        for err in error:
            assert err == 0

    def test_process_list_all(self):
        """
        Calls the test function for list-all action.
        """
        x, error = self.process_list_all()
        for err in error:
            assert err == 0

    def test_process_client_get(self):
        """
        Calls the test function for the client-get action.
        """
        x, error = self.process_client_get()
        for err in error:
            assert err == 0

    def test_process_client_list(self):
        """
        Calls the test function for the client-list action.
        """
        x, error = self.process_client_list()
        for err in error:
            assert err == 0

    def test_process_client_purge(self):
        """
        Calls the test function for the client-purge action.
        """
        x, error = self.process_client_purge()
        for err in error:
            assert err == 0

    def test_process_client_run(self):
        """
        Calls the test function for the client-run action.
        """
        x, error = self.process_client_run()
        for err in error:
            assert err == 0

    def test_process_client_schedule(self):
        """
        Calls the test function for the client-schedule action.
        """
        x, error = self.process_client_schedule()
        for err in error:
            assert err == 0

    def test_process_client_store(self):
        """
        Calls the test function for the client-store action.
        """
        x, y, error = self.process_client_store()
        for err in error:
            assert err == 0

    def test_process_schedule_get(self):
        """
        Calls the test function for the schedule-get action.
        """
        x, error = self.process_schedule_get()
        for err in error:
            assert err == 0

    def test_process_schedule_list(self):
        """
        Calls the test function for the schedule-list action.
        """
        x, error = self.process_schedule_list()
        for err in error:
            assert err == 0

    def test_process_start_scheduler(self):
        """
        Calls the test function for the start-scheduler action.
        """
        x, error = self.process_start_scheduler()
        for err in error:
            assert err == 0

    def test_process_query_data(self):
        """
        Calls the test function for the query-data action.
        """
        x, error = self.process_query_data()
        for err in error:
            assert err == 0
