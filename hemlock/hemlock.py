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
This module is the main core of Hemlock and interfaces with and controls the
majority of other modules in this package.

Created on 19 August 2013
@author: Charlie Lewis
"""

from clients.hemlock_base import Hemlock_Base
from clients.hemlock_debugger import Hemlock_Debugger
from clients.hemlock_runner import Hemlock_Runner

import hemlock_options_parser

import getpass
import json
import MySQLdb as mdb
import os
import requests
import sys
import texttable as tt
import time
import uuid

class Hemlock():
    """
    This class is responsible for driving the API and the core functionality of
    Hemlock.
    """

    def __init__(self):
        self.log = Hemlock_Debugger()
        self.HELP_COUNTER = 0

    def client_add_schedule(self, args, var_d):
        """
        Adds a specific schedule to a specific client.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid',
            '--schedule_id'
        ]
        return self.check_args(args, arg_d, var_d)

    def client_get(self, args, var_d):
        """
        Gets a specific client.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def client_list(self, args, var_d):
        """
        Lists all clients.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
        ]
        return self.check_args(args, arg_d, var_d)

    def client_purge(self, args, var_d):
        """
        Purges a specific client.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def client_remove_schedule(self, args, var_d):
        """
        Removes a specific schedule from a specific client.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid',
            '--schedule_id'
        ]
        return self.check_args(args, arg_d, var_d)

    def client_run(self, args, var_d):
        """
        Runs a client.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def client_schedule(self, args, var_d):
        """
        Schedules a client.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        # !! TODO
        #    consider having a way to activate schedules for clients,
        #    perhaps one schedule to many clients, or many schedules
        #    to one client (only one active)
        arg_d = [
            '--name',
            '--minute',
            '--hour',
            '--day_of_month',
            '--month',
            '--day_of_week',
            '--client_id',
            '--schedule_server_id'
        ]
        return self.check_args(args, arg_d, var_d)

    def client_schedules_list(self, args, var_d):
        """
        Lists all schedules assigned to a specific client.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def client_store(self, args, var_d):
        """
        Stores a client.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--name',
            '--type',
            '--system_id',
            '--credential_file'
        ]
        return self.check_args(args, arg_d, var_d)

    def client_systems_list(self, args, var_d):
        """
        Lists all systems assigned to a specific client.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def deregister_local_system(self, args, var_d):
        """
        Deegisters a specific local system.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def deregister_remote_system(self, args, var_d):
        """
        Deregisters a specific remote system.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def hemlock_server_store(self, args, var_d):
        """
        Stores Hemlock server credentials.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--credential_file'
        ]
        return self.check_args(args, arg_d, var_d)

    def list_all(self, args, var_d):
        """
        Lists everything that is stored.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
        ]
        return self.check_args(args, arg_d, var_d)

    def query_data(self, args, var_d):
        """
        Queries data stored in Hemlock filtering based on the authenticated
        user.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--user',
            '--query'
        ]
        return self.check_args(args, arg_d, var_d)

    def register_local_system(self, args, var_d):
        """
        Registers a local system.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
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
        """
        Registers a remote system.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
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
        """
        Creates a role.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--name'
        ]
        return self.check_args(args, arg_d, var_d)

    def role_delete(self, args, var_d):
        """
        Deletes a specific role.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def role_get(self, args, var_d):
        """
        Gets a specific role.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def role_list(self, args, var_d):
        """
        Lists all roles.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
        ]
        return self.check_args(args, arg_d, var_d)

    def role_users_list(self, args, var_d):
        """
        Lists all users assigned to a specific role.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def schedule_add_client(self, args, var_d):
        """
        Adds a specific client to a specific schedule.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid',
            '--client_id'
        ]
        return self.check_args(args, arg_d, var_d)

    def schedule_clients_list(self, args, var_d):
        """
        Lists all clients assigned to a specific schedule.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def schedule_delete(self, args, var_d):
        """
        Deletes a specific schedule.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def schedule_get(self, args, var_d):
        """
        Gets a specific schedule.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def schedule_list(self, args, var_d):
        """
        Lists all schedules.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
        ]
        return self.check_args(args, arg_d, var_d)

    def schedule_remove_client(self, args, var_d):
        """
        Removes a specific client from a specific schedule.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid',
            '--client_id'
        ]
        return self.check_args(args, arg_d, var_d)

    def schedule_change_server(self, args, var_d):
        """
        Changes the server that a specific schedule runs on.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid',
            '--schedule_server_id'
        ]
        return self.check_args(args, arg_d, var_d)

    def schedule_server_create(self, args, var_d):
        """
        Creates a schedule server.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--name'
        ]
        return self.check_args(args, arg_d, var_d)

    def schedule_server_delete(self, args, var_d):
        """
        Deletes a specific schedule server.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def schedule_server_get(self, args, var_d):
        """
        Gets a specific scheduler server.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def schedule_server_list(self, args, var_d):
        """
        Lists all schedule servers.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
        ]
        return self.check_args(args, arg_d, var_d)

    def start_scheduler(self, args, var_d):
        """
        Starts the scheduler daemon.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        # !! TODO this should not be required, if the creds are already stored
        arg_d = [
            '--hemlock_creds_path',
            '--schedule_server_id'
        ]
        return self.check_args(args, arg_d, var_d)

    def system_add_tenant(self, args, var_d):
        """
        Adds a specific tenant to a specific system.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid',
            '--tenant_id'
        ]
        return self.check_args(args, arg_d, var_d)

    def system_clients_list(self, args, var_d):
        """
        Lists all clients assigned to a specific system.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def system_get(self, args, var_d):
        """
        Gets a specific system.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def system_list(self, args, var_d):
        """
        Lists all clients assigned to a specific system.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
        ]
        return self.check_args(args, arg_d, var_d)

    def system_remove_tenant(self, args, var_d):
        """
        Removes a specific tenant from a specific system.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid',
            '--tenant_id'
        ]
        return self.check_args(args, arg_d, var_d)

    def system_tenants_list(self, args, var_d):
        """
        Lists all tenants assigned to a specific system.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def tenant_create(self, args, var_d):
        """
        Creates a tenant.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--name'
        ]
        return self.check_args(args, arg_d, var_d)

    def tenant_delete(self, args, var_d):
        """
        Deletes a specific tenant.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def tenant_get(self, args, var_d):
        """
        Gets a specific tenant.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def tenant_list(self, args, var_d):
        """
        Lists all tenants.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
        ]
        return self.check_args(args, arg_d, var_d)

    def tenant_systems_list(self, args, var_d):
        """
        Lists all systems assigned to a specific tenant.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def tenant_users_list(self, args, var_d):
        """
        Lists all users assigned to a specific tenant.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def user_add_role(self, args, var_d):
        """
        Adds a specific role to a specific user.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid',
            '--role_id'
        ]
        return self.check_args(args, arg_d, var_d)

    def user_add_tenant(self, args, var_d):
        """
        Adds a specific tenant to a specific user.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid',
            '--tenant_id'
        ]
        return self.check_args(args, arg_d, var_d)

    def user_create(self, args, var_d):
        """
        Creates a user.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--name',
            '--username',
            '--email',
            '--role_id',
            '--tenant_id'
        ]
        return self.check_args(args, arg_d, var_d)

    def user_delete(self, args, var_d):
        """
        Deletes a specific user.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def user_get(self, args, var_d):
        """
        Gets a specific user.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def user_list(self, args, var_d):
        """
        Lists all users.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
        ]
        return self.check_args(args, arg_d, var_d)

    def user_remove_role(self, args, var_d):
        """
        Removes a specific role from a specific user.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid',
            '--role_id'
        ]
        return self.check_args(args, arg_d, var_d)

    def user_remove_tenant(self, args, var_d):
        """
        Removes a specific tenant from a specific user.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid',
            '--tenant_id'
        ]
        return self.check_args(args, arg_d, var_d)

    def user_roles_list(self, args, var_d):
        """
        Lists all roles assigned to a specific user.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def user_tenants_list(self, args, var_d):
        """
        Lists all tenants assigned to a specific user.

        :param args: arguments to pass in from API
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a list of the arguments supplied
        """
        arg_d = [
            '--uuid'
        ]
        return self.check_args(args, arg_d, var_d)

    def check_args(self, args, arg_d, var_d):
        """
        Checks arguments supplied.

        :param args: arguments to pass in from API
        :param arg_d: list of supplied arguments
        :param var_d: dictionary of key/values made from the arguments
        :return: returns a dictionary of the arguments supplied
        """
        i = 0
        while i < len(args):
            try:
                if args[i] in arg_d:
                    var_d[args[i]] = args[i+1]
                    arg_d.remove(args[i])
                else:
                    self.HELP_COUNTER += 1
                    i = len(args)
                i += 2
            except:
                self.HELP_COUNTER += 1
        if arg_d:
            self.HELP_COUNTER += 1
        return var_d

    def print_help(self, action):
        """
        Prints out help.

        :param action: list of API action parsed into elements
        """
        if self.HELP_COUNTER >= 1:
            help_dict = {
            'client-add-schedule' : """
            client-add-schedule (add a schedule to a client)
                --uuid (uuid of client)
                --schedule_id (uuid of schedule)
            """,
            'client-get' : """
            client-get (get a specific client)
                --uuid (uuid of client)
            """,
            'client-list' : """
            client-list (list all clients)
            """,
            'client-purge' : """
            client-purge (purge a specific client)
                --uuid (uuid of client)
            """,
            'client-remove-schedule' : """
            client-remove-schedule (remove a schedule from a client)
                --uuid (uuid of client)
                --schedule_id (uuid of schedule)
            """,
            'client-run' : """
            client-run (run a specific client)
                --uuid (uuid of client)
            """,
            'client-schedule' : """
            client-schedule (schedule a specific client)
                --name (name of the schedule)
                --minute (cron minute)
                --hour (cron hour)
                --day_of_month (cron day of month)
                --month (cron month)
                --day_of_week (cron day of week)
                --client_id (uuid of the client this schedule will run on)
                --schedule_server_id (uuid of the server that will run the schedule)
            """,
            'client-schedules-list' : """
            client-schedules-list (list schedules a client belongs to)
                --uuid (uuid of client)
            """,
            'client-store' : """
            client-store (store a specific client)
                --name (name of client)
                --type (type of client, i.e. mysql)
                --system_id (uuid of system associated with the client)
                --credential_file (path to file that contains the credentials for the client)
            """,
            'client-systems-list' : """
            client-systems-list (list systems a client belongs to)
                --uuid (uuid of client)
            """,
            'deregister-local-system' : """
            deregister-local-system (from Hemlock remove a system)
                --uuid (uuid of system)
            """,
            'deregister-remote-system' : """
            deregister-remote-system (from a system remove it from Hemlock)
                --uuid (uuid of system)
            """,
            'hemlock-server-store' : """
            hemlock-server-store (store credentials for the hemlock server)
                --credential_file (path to file that contains the credentials for the hemlock server)
            """,
            'list-all' : """
            list-all (list everything)
            """,
            'query-data' : """
            query-data (query data in hemlock)
                --user (uuid of user that is requesting the query)
                --query (elasticsearch query)
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
            role-delete (delete a specific role)
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
            'schedule-add-client' : """
            schedule-add-client (add a client to a schedule)
                --uuid (uuid of schedule)
                --client_id (uuid of client)
            """,
            'schedule-clients-list' : """
            schedule-clients-list (list client a schedule belongs to)
                --uuid (uuid of schedule)
            """,
            'schedule-delete' : """
            schedule-delete (delete a specific schedule)
                --uuid (uuid of schedule)
            """,
            'schedule-get' : """
            schedule-get (get a specific schedule)
                --uuid (uuid of schedule)
            """,
            'schedule-list' : """
            schedule-list (list all schedules)
            """,
            'schedule-remove-client' : """
            schedule-remove-client (remove a client from a schedule)
                --uuid (uuid of schedule)
                --client_id (uuid of client)
            """,
            'schedule-change-server' : """
            schedule-change-server (change schedule server a specific schedule runs on)
                --uuid (uuid of schedule)
                --schedule_server_id (uuid of schedule server)
            """,
            'schedule-server-create' : """
            schedule-server-create (create new schedule server)
                --name (name of schedule server)
            """,
            'schedule-server-delete' : """
            schedule-server-delete (delete a specific schedule server)
                --uuid (uuid of schedule server)
            """,
            'schedule-server-get' : """
            schedule-server-get (get a specific schedule server)
                --uuid (uuid of schedule server)
            """,
            'schedule-server-list' : """
            schedule-server-list (list all schedule servers)
            """,
            'start-scheduler' : """
            start-scheduler (start the scheduler)
                --hemlock_creds_path (file path to the hemlock_creds file)
                --schedule_server_id (uuid of the server that will run the scheduler)
            """,
            'system-add-tenant' : """
            system-add-tenant (add a tenant to a system)
                --uuid (uuid of system)
                --tenant_id (uuid of tenant)
            """,
            'system-clients-list' : """
            system-clients-list (list clients a system belongs to)
                --uuid (uuid of system)
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

    def process_args(self, debug, args):
        """
        Processes arguments by directing the supplied action to the
        proper function and ensure that all required fields are present.

        :param debug: instance of
            :class:`~hemlock.clients.hemlock_debugger.Hemlock_Debugger`
        :param args: list of supplied arguments
        :return: returns a dictionary of argument key/values and the API
            action
        """
        var_d = {}

        arg_actions = {
            'client-add-schedule' : self.client_add_schedule,
            'client-get' : self.client_get,
            'client-list' : self.client_list,
            'client-purge' : self.client_purge,
            'client-remove-schedule' : self.client_remove_schedule,
            'client-run' : self.client_run,
            'client-schedule' : self.client_schedule,
            'client-schedules-list' : self.client_schedules_list,
            'client-store' : self.client_store,
            'client-systems-list' : self.client_systems_list,
            'deregister-local-system' : self.deregister_local_system,
            'deregister-remote-system' : self.deregister_remote_system,
            'hemlock-server-store' : self.hemlock_server_store,
            'list-all' : self.list_all,
            'query-data' : self.query_data,
            'register-local-system' : self.register_local_system,
            'register-remote-system' : self.register_remote_system,
            'role-create' : self.role_create,
            'role-delete' : self.role_delete,
            'role-get' : self.role_get,
            'role-list' : self.role_list,
            'role-users-list' : self.role_users_list,
            'schedule-add-client' : self.schedule_add_client,
            'schedule-clients-list' : self.schedule_clients_list,
            'schedule-delete' : self.schedule_delete,
            'schedule-get' : self.schedule_get,
            'schedule-list' : self.schedule_list,
            'schedule-remove-client' : self.schedule_remove_client,
            'schedule-change-server' : self.schedule_change_server,
            'schedule-server-create' : self.schedule_server_create,
            'schedule-server-delete' : self.schedule_server_delete,
            'schedule-server-get' : self.schedule_server_get,
            'schedule-server-list' : self.schedule_server_list,
            'start-scheduler' : self.start_scheduler,
            'system-add-tenant' : self.system_add_tenant,
            'system-clients-list' : self.system_clients_list,
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
            self.HELP_COUNTER += 1

        self.print_help(action)

        return var_d, args[0]

    # use OptionParser to parse command-line switches for authentication variables
    # return variables in options array, as well as leftover args that don't have switches
    def parse_auth(self):  
        """
        Parses options for authentication if supplied as arguments.

        :return: returns an instance of
            :class:`~hemlock.hemlock_options_parser.PassThroughOptionParser`
        """
        parser = hemlock_options_parser.PassThroughOptionParser()
        parser.add_option("-s", "--server-mysql", action="store", dest="server",help="MySQL Server") #, default="localhost"
        parser.add_option("-d", "--database", action="store", dest="db", help="MySQL DB")
        parser.add_option("-u", "--mysql-username", action="store", dest="user", help="MySQL Username")
        parser.add_option("-p", "--mysql-password", action="store", dest="pw", help="MySQL Password")
        parser.add_option("-c", "--couchbase-server", action="store", dest="c_server", help="Couchbase Server")
        parser.add_option("-b", "--couchbase-bucket", action="store", dest="bucket", help="Couchbase Bucket")
        parser.add_option("-n", "--couchbase-username", action="store", dest="c_user", help="Couchbase Username")
        parser.add_option("-w", "--couchbase-password", action="store", dest="c_pw", help="Couchbase Password")
        parser.add_option("-e", "--elasticsearch-endpoint", action="store", dest="es", help="ElasticSearch Endpoint")
        parser.add_option("-D", "--debug", action="store_false", dest="debug", help="Debugging Mode")
        parser.add_option("-z", "--no-couchbase", action="store_false", dest="no_couchbase", help="Don't use Couchbase")
        parser.add_option("-v", "--version", action="store_false", dest="version", help="Version")
        return parser.parse_args()

    def read_creds(self, debug):
        """
        Reads in the credentials file for the Hemlock system and stores them in
        the local environment variables of the shell.

        :param debug: instance of
            :class:`~hemlock.clients.hemlock_debugger.Hemlock_Debugger`
        """
        # trying hemlock_creds in the current directory as a default, if that
        # fails, then ask for a file or parameters
        try:
            f = open('hemlock_creds', 'r')
            for line in f:
                self.log.debug(debug, line)
                if len(line) > 0 and line[0] != "#" and "=" in line:
                    # split each line on the first '='
                    line_a = line.split("=",1)
                    try:
                        os.environ[line_a[0]] = line_a[1].strip()
                    except:
                        print "Malformed Hemlock Creds file."
                        self.log.debug(debug, str(sys.exc_info()[0]))
            f.close()
        except:
            resp = ""
            while resp != 'y' and resp != 'n':
                resp = raw_input("Do you have a hemlock_creds file? (y/n)")
                resp = resp.lower()
            if resp == 'y':
                resp = raw_input("Path to hemlock_creds file: ")
                try:
                    f = open(resp, 'r')
                    for line in f:
                        self.log.debug(debug, line)
                        if len(line) > 0 and line[0] != "#" and "=" in line:
                            # split each line on the first '='
                            line_a = line.split("=",1)
                            try:
                                os.environ[line_a[0]] = line_a[1].strip()
                            except:
                                print "Malformed Hemlock Creds file."
                                self.log.debug(debug, str(sys.exc_info()[0]))
                    f.close()
                except:
                    print "Unable to open "+resp
                    self.log.debug(debug, str(sys.exc_info()[0]))
        return

    def get_auth(self):
        """
        Gets the authentication of supplied arguments, environment variables,
        or sets them to defaults.

        :return: returns each of the parsed out arguments
        """
        # extract command-line switches
        (options, args_leftover) = Hemlock().parse_auth()

        if options.version != None:
            print "Version: 0.1.5"
            sys.exit(0)

        if not args_leftover:
            return args_leftover, options.user, options.pw, options.db, options.server, options.c_server, options.c_user, options.bucket, options.c_pw, options.es, options.debug, options.no_couchbase

        if options.debug == None:
            options.debug = 0
        else:
            options.debug = 1

        if options.no_couchbase == None:
            options.no_couchbase = 0
        else:
            options.no_couchbase = 1

        asked_for_creds = 0

        # use environment variables and CLI as fallbacks for unspecified variables
        try:
            if options.server == None:
                options.server = os.environ['HEMLOCK_MYSQL_SERVER']
            self.log.debug(options.debug, "HEMLOCK_MYSQL_SERVER = "+str(options.server))
        except:
            if asked_for_creds == 0:
                self.read_creds(options.debug)
                asked_for_creds = 1
                try:
                    options.server = os.environ['HEMLOCK_MYSQL_SERVER']
                except:
                    options.server = raw_input("MySQL Server (default is localhost):")
                    if options.server == "":
                        options.server = "localhost"
                    self.log.debug(options.debug, "HEMLOCK_MYSQL_SERVER = "+str(options.server))
            else:
                options.server = raw_input("MySQL Server (default is localhost):")
                if options.server == "":
                    options.server = "localhost"
                self.log.debug(options.debug, "HEMLOCK_MYSQL_SERVER = "+str(options.server))

        try:
            if options.db == None:
                options.db = os.environ['HEMLOCK_MYSQL_DB']
            self.log.debug(options.debug, "HEMLOCK_MYSQL_DB = "+str(options.db))
        except:
            if asked_for_creds == 0:
                self.read_creds(options.debug)
                asked_for_creds = 1
                try:
                    options.db = os.environ['HEMLOCK_MYSQL_DB']
                except:
                    options.db = raw_input("MySQL DB (default is hemlock):")
                    if options.db == "":
                        options.db = "hemlock"
                    self.log.debug(options.debug, "HEMLOCK_MYSQL_DB = "+str(options.db))
            else:
                options.db = raw_input("MySQL DB (default is hemlock):")
                if options.db == "":
                    options.db = "hemlock"
                self.log.debug(options.debug, "HEMLOCK_MYSQL_DB = "+str(options.db))

        try:
            if options.user == None:
                options.user = os.environ['HEMLOCK_MYSQL_USERNAME']
            self.log.debug(options.debug, "HEMLOCK_MYSQL_USERNAME = "+str(options.user))
        except:
            if asked_for_creds == 0:
                self.read_creds(options.debug)
                asked_for_creds = 1
                try:
                    options.user = os.environ['HEMLOCK_MYSQL_USERNAME']
                except:
                    options.user = raw_input("Username:")
                    self.log.debug(options.debug, "HEMLOCK_MYSQL_USER = "+str(options.user))
            else:
                options.user = raw_input("Username:")
                self.log.debug(options.debug, "HEMLOCK_MYSQL_USER = "+str(options.user))

        try:
            if options.pw == None:
                options.pw = os.environ['HEMLOCK_MYSQL_PW']
            self.log.debug(options.debug, "HEMLOCK_MYSQL_PW = "+str(options.pw))
        except:
            if asked_for_creds == 0:
                self.read_creds(options.debug)
                asked_for_creds = 1
                try:
                    options.pw = os.environ['HEMLOCK_MYSQL_PW']
                except:
                    options.pw = getpass.getpass("MySQL Password:")
                    self.log.debug(options.debug, "HEMLOCK_MYSQL_PW = "+str(options.pw))
            else:
                options.pw = getpass.getpass("MySQL Password:")
                self.log.debug(options.debug, "HEMLOCK_MYSQL_PW = "+str(options.pw))

        # only need couchbase creds if options.no_couchbase isn't set
        if options.no_couchbase == 0:
            try:
                if options.c_server == None:
                    options.c_server = os.environ['HEMLOCK_COUCHBASE_SERVER']
                self.log.debug(options.debug, "HEMLOCK_COUCHBASE_SERVER = "+str(options.c_server))
            except:
                if asked_for_creds == 0:
                    self.read_creds(options.debug)
                    asked_for_creds = 1
                    try:
                        options.c_server = os.environ['HEMLOCK_COUCHBASE_SERVER']
                    except:
                        options.c_server = raw_input("Couchbase Server (default is localhost):")
                        if options.c_server == "":
                            options.c_server = "localhost"
                        self.log.debug(options.debug, "HEMLOCK_COUCHBASE_SERVER = "+str(options.c_server))
                else:
                    options.c_server = raw_input("Couchbase Server (default is localhost):")
                    if options.c_server == "":
                        options.c_server = "localhost"
                    self.log.debug(options.debug, "HEMLOCK_COUCHBASE_SERVER = "+str(options.c_server))

            try:
                if options.bucket == None:
                    options.bucket = os.environ['HEMLOCK_COUCHBASE_BUCKET']
                self.log.debug(options.debug, "HEMLOCK_COUCHBASE_BUCKET = "+str(options.bucket))
            except:
                if asked_for_creds == 0:
                    self.read_creds(options.debug)
                    asked_for_creds = 1
                    try:
                        options.bucket = os.environ['HEMLOCK_COUCHBASE_BUCKET']
                    except:
                        options.bucket = raw_input("Couchbase Bucket (default is hemlock):")
                        if options.bucket == "":
                            options.bucket = "hemlock"
                        self.log.debug(options.debug, "HEMLOCK_COUCHBASE_BUCKET = "+str(options.bucket))
                else:
                    options.bucket = raw_input("Couchbase Bucket (default is hemlock):")
                    if options.bucket == "":
                        options.bucket = "hemlock"
                    self.log.debug(options.debug, "HEMLOCK_COUCHBASE_BUCKET = "+str(options.bucket))

            try:
                if options.c_user == None:
                    options.c_user = os.environ['HEMLOCK_COUCHBASE_USERNAME']
                self.log.debug(options.debug, "HEMLOCK_COUCHBASE_USERNAME = "+str(options.c_user))
            except:
                if asked_for_creds == 0:
                    self.read_creds(options.debug)
                    asked_for_creds = 1
                    try:
                        options.c_user = os.environ['HEMLOCK_COUCHBASE_USERNAME']
                    except:
                        options.bucket = raw_input("Couchbase Username (default is hemlock):")
                        if options.bucket == "":
                            options.bucket = "hemlock"
                        self.log.debug(options.debug, "HEMLOCK_COUCHBASE_USERNAME = "+str(options.c_user))
                else:
                    options.bucket = raw_input("Couchbase Username (default is hemlock):")
                    if options.bucket == "":
                        options.bucket = "hemlock"
                    self.log.debug(options.debug, "HEMLOCK_COUCHBASE_USERNAME = "+str(options.c_user))

            try:
                if options.c_pw == None:
                    options.c_pw = os.environ['HEMLOCK_COUCHBASE_PW']
                self.log.debug(options.debug, "HEMLOCK_COUCHBASE_PW = "+str(options.c_pw))
            except:
                if asked_for_creds == 0:
                    self.read_creds(options.debug)
                    asked_for_creds = 1
                    try:
                        options.c_pw = os.environ['HEMLOCK_COUCHBASE_PW']
                    except:
                        options.c_pw = getpass.getpass("Couchbase Password:")
                        self.log.debug(options.debug, "HEMLOCK_COUCHBASE_PW = "+str(options.c_pw))
                else:
                    options.c_pw = getpass.getpass("Couchbase Password:")
                    self.log.debug(options.debug, "HEMLOCK_COUCHBASE_PW = "+str(options.c_pw))

        try:
            if options.es == None:
                options.es = os.environ['HEMLOCK_ELASTICSEARCH_ENDPOINT']
            self.log.debug(options.debug, "HEMLOCK_ELASTICSEARCH_ENDPOINT = "+str(options.es))
        except:
            if asked_for_creds == 0:
                self.read_creds(options.debug)
                asked_for_creds = 1
                try:
                    options.es = os.environ['HEMLOCK_ELASTICSEARCH_ENDPOINT']
                except:
                    options.es = getpass.getpass("ElasticSearch Endpoint:")
                    self.log.debug(options.debug, "HEMLOCK_ELASTICSEARCH_ENDPOINT = "+str(options.es))
            else:
                options.es = getpass.getpass("ElasticSearch Endpoint:")
                self.log.debug(options.debug, "HEMLOCK_ELASTICSEARCH_ENDPOINT = "+str(options.es))

        return args_leftover, options.user, options.pw, options.db, options.server, options.c_server, options.c_user, options.bucket, options.c_pw, options.es, options.debug, options.no_couchbase

    def mysql_server(self, debug, server, user, pw, db):
        """
        Connects to the Hemlock MySQL Server

        :param debug: instance of
            :class:`~hemlock.clients.hemlock_debugger.Hemlock_Debugger`
        :param server: server address of the Hemlock MySQL server
        :param user: user account to connect to the Hemlock MySQL server
        :param pw: password of the user account
        :param db: database to connect to in the Hemlock MySQL server
        :return: returns an instance of the mysql connection
        """
        # connect to the mysql server
        try:
            m_server = mdb.connect(server, user, pw, db)
            self.log.debug(debug, "MySQL Handle: "+str(m_server))
        except:
            self.log.debug(debug, str(sys.exc_info()[0]))
            print "MySQL server failure"
            sys.exit(0)
        return m_server

    def connect_server(self, debug, c_server, c_user, c_bucket, c_pw, es, no_couchbase):
        """
        Connects to the Hemlock couchbase server.

        :param debug: instance of
            :class:`~hemlock.clients.hemlock_debugger.Hemlock_Debugger`
        :param c_server: couchbase server ip address
        :param c_user: couchbase username
        :param c_bucket: couchbase bucket
        :param c_pw: couchbase password
        :param es: elasticsearch server ip address
        :param no_couchbase: flag of whether or not to use a couchbase
            connection or an elasticsearch connection
        :return: returns an instance of the couchbase or elasticsearch
            connection
        """
        h_server = ""
        if no_couchbase == 1:
            import pyes
            # connect to the elasticsearch server
            try:
                h_server = pyes.ES(("http", es, "9200"))
                self.log.debug(debug, "ElasticSearch connection handle: "+str(h_server))
            except:
                print "Failure connecting to the Hemlock server"
                self.log.debug(debug, str(sys.exc_info()[0]))
                sys.exit(0)
        else:
            import couchbase
            # connect to the couchbase server
            try:
                h_server = couchbase.Couchbase.connect(host=c_server,
                                     bucket=c_bucket,
                                     username=c_user,
                                     password=c_pw)
                self.log.debug(debug, "Couchbase connection handle: "+str(h_server))
            except:
                print "Failure connecting to the Hemlock server"
                self.log.debug(debug, str(sys.exc_info()[0]))
                sys.exit(0)
        return h_server

    def process_action(self, debug, action, var_d, m_server, c_server, c_user, bucket, c_pw, no_couchbase, es):
        """
        Processes the action that was supplied.

        :param debug: instance of
            :class:`~hemlock.clients.hemlock_debugger.Hemlock_Debugger`
        :param action: action to be performed
        :param var_d: dictionary of key/values that contain the parameters for
            the action
        :param m_server: instance of MySQL connection
        :param c_server: couchbase server ip address
        :param c_user: couchbase username
        :param bucket: couchbase bucket
        :param c_pw: couchbase password
        :param no_couchbase: flag of whether or not to use a couchbase
            connection or an elasticsearch connection
        :param es: elasticsearch server ip address
        :return: list of results and any errors that may have occurred.
        """
        error = 0

        # !! TODO try/except

        # !! TODO FIX THIS!!!!!!
        aes_key = "test"

        cur = m_server.cursor()
        self.log.debug(debug, "MySQL Cursor: "+str(cur))

        # ensure mysql tables exist
        cur.execute("show tables")
        results = cur.fetchall()
        tables = []
        i = 0
        while i < len(results):
            tables.append(results[i][0])
            i += 1
        self.log.debug(debug, "Tables: "+str(tables))

        # create mysql tables that don't already exist
        if "clients" not in tables:
            client_table = "CREATE TABLE IF NOT EXISTS clients(id INT PRIMARY KEY AUTO_INCREMENT, uuid VARCHAR(36), no_couchbase VARCHAR(1), name VARCHAR(50), type VARCHAR(50), credentials BLOB, created DATETIME, INDEX (uuid)) ENGINE = INNODB"
            cur.execute(client_table)
            self.log.debug(debug, "Created table: "+str(client_table))
        if "hemlock_server" not in tables:
            server_table = "CREATE TABLE IF NOT EXISTS hemlock_server(id INT PRIMARY KEY AUTO_INCREMENT, uuid VARCHAR(36), credentials BLOB, created DATETIME, INDEX (uuid)) ENGINE = INNODB"
            cur.execute(server_table)
            self.log.debug(debug, "Created table: "+str(server_table))
        if "roles" not in tables:
            role_table = "CREATE TABLE IF NOT EXISTS roles(id INT PRIMARY KEY AUTO_INCREMENT, uuid VARCHAR(36), name VARCHAR(50), created DATETIME, INDEX (uuid)) ENGINE = INNODB"
            cur.execute(role_table)
            self.log.debug(debug, "Created table: "+str(role_table))
        if "schedule_servers" not in tables:
            schedule_server_table = "CREATE TABLE IF NOT EXISTS schedule_servers(id INT PRIMARY KEY AUTO_INCREMENT, uuid VARCHAR(36), name VARCHAR(50), created DATETIME, INDEX (uuid)) ENGINE = INNODB"
            cur.execute(schedule_server_table)
            self.log.debug(debug, "Created table: "+str(schedule_server_table))
        if "schedules" not in tables:
            schedule_table = "CREATE TABLE IF NOT EXISTS schedules(id INT PRIMARY KEY AUTO_INCREMENT, uuid VARCHAR(36), name VARCHAR(50), minute VARCHAR(10), hour VARCHAR(10), day_of_month VARCHAR(10), month VARCHAR(10), day_of_week VARCHAR(10), schedule_server_id VARCHAR(36), created DATETIME, INDEX (uuid), CONSTRAINT fksch_server FOREIGN KEY (schedule_server_id) REFERENCES schedule_servers(uuid) ON DELETE CASCADE) ENGINE = INNODB"
            cur.execute(schedule_table)
            self.log.debug(debug, "Created table: "+str(schedule_table))
        if "tenants" not in tables:
            tenant_table = "CREATE TABLE IF NOT EXISTS tenants(id INT PRIMARY KEY AUTO_INCREMENT, uuid VARCHAR(36), name VARCHAR(50), created DATETIME, INDEX (uuid)) ENGINE = INNODB"
            cur.execute(tenant_table)
            self.log.debug(debug, "Created table: "+str(tenant_table))
        if "users" not in tables:
            user_table = "CREATE TABLE IF NOT EXISTS users(id INT PRIMARY KEY AUTO_INCREMENT, uuid VARCHAR(36), name VARCHAR(50), username VARCHAR(50), password VARBINARY(200), email VARCHAR(50), created DATETIME, INDEX (uuid)) ENGINE = INNODB"
            cur.execute(user_table)
            self.log.debug(debug, "Created table: "+str(user_table))
        if "systems" not in tables:
            system_table = "CREATE TABLE IF NOT EXISTS systems(id INT PRIMARY KEY AUTO_INCREMENT, uuid VARCHAR(36), name VARCHAR(50), data_type VARCHAR(50), description VARCHAR(200), endpoint VARCHAR(100), hostname VARCHAR(50), port VARCHAR(5), remote_uri VARCHAR(100), poc_name VARCHAR(50), poc_email VARCHAR(50), remote BOOL, created DATETIME, updated_data DATETIME, INDEX (uuid)) ENGINE = INNODB"
            cur.execute(system_table)
            self.log.debug(debug, "Created table: "+str(system_table))
        if "users_roles" not in tables:
            users_roles_table = "CREATE TABLE IF NOT EXISTS users_roles(user_id VARCHAR(36), role_id VARCHAR(36), INDEX (user_id), CONSTRAINT fkur_roles FOREIGN KEY (role_id) REFERENCES roles(uuid), CONSTRAINT fkur_users FOREIGN KEY (user_id) REFERENCES users(uuid) ON DELETE CASCADE) ENGINE = INNODB"
            cur.execute(users_roles_table)
            self.log.debug(debug, "Created table: "+str(users_roles_table))
        if "users_tenants" not in tables:
            users_tenants_table = "CREATE TABLE IF NOT EXISTS users_tenants(user_id VARCHAR(36), tenant_id VARCHAR(36), INDEX (user_id), CONSTRAINT fkut_tenants FOREIGN KEY (tenant_id) REFERENCES tenants(uuid), CONSTRAINT fkut_users FOREIGN KEY (user_id) REFERENCES users(uuid) ON DELETE CASCADE) ENGINE = INNODB"
            cur.execute(users_tenants_table)
            self.log.debug(debug, "Created table: "+str(users_tenants_table))
        if "systems_tenants" not in tables:
            systems_tenants_table = "CREATE TABLE IF NOT EXISTS systems_tenants(system_id VARCHAR(36), tenant_id VARCHAR(36), INDEX (system_id), CONSTRAINT fkst_tenants FOREIGN KEY (tenant_id) REFERENCES tenants(uuid), CONSTRAINT fkst_systems FOREIGN KEY (system_id) REFERENCES systems(uuid) ON DELETE CASCADE) ENGINE = INNODB"
            cur.execute(systems_tenants_table)
            self.log.debug(debug, "Created table: "+str(systems_tenants_table))
        if "schedules_clients" not in tables:
            schedules_clients_table = "CREATE TABLE IF NOT EXISTS schedules_clients(schedule_id VARCHAR(36), client_id VARCHAR(36), INDEX (schedule_id), CONSTRAINT fksc_clients FOREIGN KEY (client_id) REFERENCES clients(uuid), CONSTRAINT fksc_schedules FOREIGN KEY (schedule_id) REFERENCES schedules(uuid) ON DELETE CASCADE) ENGINE = INNODB"
            cur.execute(schedules_clients_table)
            self.log.debug(debug, "Created table: "+str(schedules_clients_table))
        if "systems_clients" not in tables:
            systems_clients_table = "CREATE TABLE IF NOT EXISTS systems_clients(system_id VARCHAR(36), client_id VARCHAR(36), INDEX (system_id), CONSTRAINT fksyc_clients FOREIGN KEY (client_id) REFERENCES clients(uuid), CONSTRAINT fksyc_systems FOREIGN KEY (system_id) REFERENCES systems(uuid) ON DELETE CASCADE) ENGINE = INNODB"
            cur.execute(systems_clients_table)
            self.log.debug(debug, "Created table: "+str(systems_clients_table))

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
        if "query" in action_a and "data" in action_a:
            pw = getpass.getpass("User Password:")
            # verify the user password
            decrypt_action = "SELECT AES_DECRYPT(password, '"+aes_key+"') from users where uuid = '"+var_d['--user']+"'"
            cur.execute(decrypt_action)
            results = cur.fetchall()
            if pw != results[0][0]:
                print "Invalid password."
                sys.exit(0)
        if "add" not in action_a:
            props.append("uuid")
            props.append("created")
            vals.append(uid)
            vals.append(timestamp)

        if "query" in action_a:
            # curl example:
            #
            # curl -XPOST "http://l41-vsrv-es01.b.internal:9200/hemlock/_search" -d'
            # {
            #    "size": 200,
            #    "query": {
            #       "bool": {
            #          "must": [
            #             {
            #                "match": {
            #                   "doc.hemlock-system": {
            #                      "query": "4991f644-e94d-472e-8526-c7f08a656735 59822f6b-4646-4dd8-9be9-038c2988375a",
            #                      "operator": "or"
            #                   }
            #                }
            #             }
            #          ],
            #          "should": [
            #             {
            #                "match": {
            #                   "_all": "foo"
            #                }
            #             }
            #          ]
            #       }
            #    }
            # }'

            h_server = self.connect_server(debug, c_server, c_user, bucket, c_pw, es, no_couchbase)

            payload = "{\"size\":100,\"query\":{\"bool\":{\"must\":[{\"match\":{\"doc.hemlock-system\":{\"query\":\""

            # get the list of tenants this user belongs to
            data_action = "SELECT * FROM users_tenants WHERE user_id = '"+var_d['--user']+"'"
            cur.execute(data_action)
            results = cur.fetchall()
            system_flag = 0
            for tenant in results:
                # get the list of systems that the user has access to via tenants
                data_action = "SELECT * FROM systems_tenants WHERE tenant_id = '"+tenant[1]+"'"
                cur.execute(data_action)
                systems = cur.fetchall()
                for system in systems:
                    payload += system[0]+" "
                    system_flag = 1

            # if no systems
            if system_flag == 0:
                print "No systems have been added the tenants this user belongs to."
                sys.exit(0)

            payload = payload[:-1]
            payload += "\",\"operator\":\"or\"}}}],\"should\":[{\"match\":{\"_all\":\""+var_d['--query']+"\"}}]}}}"

            url = "http://"+es+":9200/hemlock/_search"
            r = requests.post(url, data=json.dumps(json.loads(payload)))
            results = r.json()
            results = results['hits']['hits']
            result_list = []
            for result in results:
                result_list.append(result['_id'])

            if no_couchbase:
                if results:
                    # !! TODO
                    #    format this the same way that it would get output if
                    #    it was couchbase so it's consistent.
                    print results
                else:
                    print "No results."
                    sys.exit(0)
            else:
                if result_list:
                    records = []
                    c = h_server.get_multi(result_list)
                    for key, result in c.items():
                        records.append(result.value)
                    for record in records:
                        print record
                else:
                    print "No results."
                    sys.exit(0)

        elif "system" in action_a:
            # update to systems/clients table
            if "deregister" in action_a:
                # delete
                data_action = "DELETE FROM systems_tenants WHERE system_id = '"+var_d['--uuid']+"'"
                data_action2 = "DELETE FROM systems WHERE uuid = '"+var_d['--uuid']+"'"
                self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action2)
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
                self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action2)
            elif "add" in action_a:
                # write
                # systems_tenants
                if "tenant" in action_a:
                    data_action = "INSERT INTO systems_tenants(system_id, tenant_id) VALUES(\""+var_d['--uuid']+"\", \""+var_d['--tenant_id']+"\")"
                self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
            elif "remove" in action_a:
                # delete
                # systems_tenants
                if "tenant" in action_a:
                    remove_action = "SELECT * FROM systems_tenants WHERE system_id = '"+var_d['--uuid']+"'"
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+remove_action)
                    cur.execute(remove_action)
                    self.log.debug(debug, "Successfully executed the following SQL query: "+remove_action)
                    remove_results = cur.fetchall()
                    self.log.debug(debug, "Results: "+str(remove_results))
                    if len(remove_results) > 1:
                        data_action = "DELETE FROM systems_tenants WHERE system_id = '"+var_d['--uuid']+"' and tenant_id = '"+var_d['--tenant_id']+"'"
                        self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                    else:
                        print "You can not remove the last tenant from a system."
                        sys.exit(0)
            else:
                # read only
                if "tenants" in action_a:
                    data_action = "SELECT * FROM systems_tenants WHERE system_id = '"+var_d['--uuid']+"'"
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                elif "clients" in action_a:
                    data_action = "SELECT * FROM systems_clients WHERE system_id = '"+var_d['--uuid']+"'"
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                else:
                    data_action = "SELECT * FROM systems"
                    if "get" in action_a:
                        data_action += " WHERE uuid = '"+var_d['--uuid']+"'"
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
            cur.execute(data_action)
            self.log.debug(debug, "Successfully executed the following SQL query: "+data_action)
            if data_action2:
                cur.execute(data_action2)
                self.log.debug(debug, "Successfully executed the following SQL query: "+data_action2)

        else:
            # update to clients/schedules/roles/tenants/users tables
            if "add" in action_a: 
                # write
                if "tenant" in action_a:
                    data_action = "INSERT INTO users_tenants(user_id, tenant_id) VALUES(\""+var_d['--uuid']+"\", \""+var_d['--tenant_id']+"\")"
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                elif "schedule" in action_a:
                    # !! TODO ensure that the same client is not added to the same schedule more than once
                    # client_add_schedule
                    if action_a[0] == "client":
                        data_action = "INSERT INTO schedules_clients(client_id, schedule_id) VALUES(\""+var_d['--uuid']+"\", \""+var_d['--schedule_id']+"\")"
                    # schedule_add_client
                    else:
                        data_action = "INSERT INTO schedules_clients(client_id, schedule_id) VALUES(\""+var_d['--uuid']+"\", \""+var_d['--client_id']+"\")"
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                else: # roles
                    data_action = "INSERT INTO users_roles(user_id, role_id) VALUES(\""+var_d['--uuid']+"\", \""+var_d['--role_id']+"\")"
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
            elif "remove" in action_a:
                # delete
                if "tenant" in action_a:
                    remove_action = "SELECT * FROM users_tenants WHERE user_id = '"+var_d['--uuid']+"'"
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+remove_action)
                elif "schedule" in action_a:
                    # client_remove_schedule
                    if action_a[0] == "client":
                        remove_action = "SELECT * FROM schedules_clients WHERE client_id = '"+var_d['--uuid']+"'"
                    # schedule_remove_client
                    else:
                        remove_action = "SELECT * FROM schedules_clients WHERE schedule_id = '"+var_d['--uuid']+"'"
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+remove_action)
                else: # roles
                    remove_action = "SELECT * FROM users_roles WHERE user_id = '"+var_d['--uuid']+"'"
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+remove_action)
                cur.execute(remove_action)
                remove_results = cur.fetchall()
                self.log.debug(debug, "Successfully executed the following SQL query: "+remove_action)
                self.log.debug(debug, "Results: "+str(remove_results))
                if len(remove_results) > 1:
                    if "tenant" in action_a:
                        data_action = "DELETE FROM users_tenants WHERE user_id = '"+var_d['--uuid']+"' and tenant_id = '"+var_d['--tenant_id']+"'"
                        self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                    elif "schedule" in action_a:
                        # client_remove_schedule
                        if action_a[0] == "client":
                            data_action = "DELETE FROM schedules_clients WHERE client_id = '"+var_d['--uuid']+"' and system_id = '"+var_d['--system_id']+"'"
                        # schedule_remove_client
                        else:
                            data_action = "DELETE FROM schedules_clients WHERE system_id = '"+var_d['--uuid']+"' and client_id = '"+var_d['--client_id']+"'"
                        self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                    else: # roles
                        data_action = "DELETE FROM users_roles WHERE user_id = '"+var_d['--uuid']+"' and role_id = '"+var_d['--role_id']+"'"
                        self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                else:
                    # it's ok if it's a schedule/client
                    if "schedule" not in action_a:
                        print "You can not remove the last tenant or role from a user."
                        sys.exit(0)
            elif "change" in action_a:
                data_action = "UPDATE schedules SET schedule_server_id = '"+var_d['--schedule_server_id']+"' where uuid = "+var_d['--uuid'] 
            elif "create" in action_a:
                # write
                if "server" in action_a:
                    data_action = "INSERT INTO schedule_servers("
                else:
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
                self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action2)
                self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action3)
            elif "delete" in action_a:
                # delete
                if "tenants" in action_a:
                    data_action = "DELETE FROM "+action_a[0]+"s_tenants WHERE "+action_a[0]+"_id = '"+var_d['--uuid']+"'"
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                elif "roles" in action_a:
                    data_action = "DELETE FROM "+action_a[0]+"s_roles WHERE "+action_a[0]+"_id = '"+var_d['--uuid']+"'"
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                elif "server" in action_a:
                    data_action = "DELETE FROM schedules WHERE schedule_server_id = '"+var_d['--uuid']+"'"
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                elif "schedule" in action_a:
                    data_action = "DELETE FROM "+action_a[0]+"s_clients WHERE "+action_a[0]+"_id = '"+var_d['--uuid']+"'"
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                if "server" in action_a:
                    data_action2 = "DELETE FROM schedule_servers WHERE uuid = '"+var_d['--uuid']+"'"
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action2)
                else:
                    data_action2 = "DELETE FROM "+action_a[0]+"s WHERE uuid = '"+var_d['--uuid']+"'"
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action2)
            # start scheduler
            elif "start" in action_a:
                # validate that the schedule_server_id provided exists
                data_action = "SELECT uuid FROM schedule_servers WHERE uuid = '"+var_d['--schedule_server_id']+"'"
                cur.execute(data_action)
                results = cur.fetchall()
                if results:
                    # check if there is already a hemlock_scheduler running
                    # if there is already one running, don't spawn another one
                    cmd = "ps cax | grep hemlock-sched | wc -l"
                    result = os.popen(cmd).read()
                    if result[0] == "0":
                        # DEBUG
                        # call hemlock-scheduler
                        if debug == 0:
                            cmd = "hemlock-scheduler "+var_d['--hemlock_creds_path']+" "+var_d['--schedule_server_id']+" >> scheduler.log &"
                        else:
                            cmd = "hemlock-scheduler "+var_d['--hemlock_creds_path']+" "+var_d['--schedule_server_id']+" -D >> scheduler.log &"

                        # result should be 0, otherwise error
                        result = os.system(cmd)
                    else:
                        print "There is already a Hemlock Scheduler running."
                else:
                    print "The schedule server '"+var_d['--schedule_server_id']+"' does not exist."
            else:
                # read only
                if "roles" in action_a:
                    data_action = "SELECT * FROM users_roles WHERE user_id = '"+var_d['--uuid']+"'"
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                elif "schedule" in action_a and "server" in action_a:
                    data_action = "SELECT * FROM schedule_servers"
                    if "get" in action_a:
                        data_action += " WHERE uuid = '"+var_d['--uuid']+"'"
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                elif "tenants" in action_a and "user" in action_a:
                    data_action = "SELECT * FROM users_tenants WHERE user_id = '"+var_d['--uuid']+"'"
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                elif "tenants" in action_a and "system" in action_a:
                    data_action = "SELECT * FROM systems_tenants WHERE system_id = '"+var_d['--uuid']+"'"
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                elif "users" in action_a and "tenant" in action_a:
                    data_action = "SELECT * FROM users_tenants WHERE tenant_id = '"+var_d['--uuid']+"'"
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                elif "users" in action_a and "role" in action_a:
                    data_action = "SELECT * FROM users_roles WHERE role_id = '"+var_d['--uuid']+"'"
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                elif "clients" in action_a and "schedule" in action_a:
                    data_action = "SELECT * FROM schedules_clients WHERE schedule_id = '"+var_d['--uuid']+"'"
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                elif "clients" in action_a and "system" in action_a:
                    data_action = "SELECT * FROM systems_clients WHERE system_id = '"+var_d['--uuid']+"'"
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                elif "schedules" in action_a and "client" in action_a:
                    data_action = "SELECT * FROM schedules_clients WHERE client_id = '"+var_d['--uuid']+"'"
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                elif "systems" in action_a and "tenant" in action_a:
                    data_action = "SELECT * FROM systems_tenants WHERE tenant_id = '"+var_d['--uuid']+"'"
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                elif "systems" in action_a and "client" in action_a:
                    data_action = "SELECT * FROM systems_clients WHERE client_id = '"+var_d['--uuid']+"'"
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                elif "server" in action_a:
                    # write
                    if "store" in action_a:
                        # delete any pre-existing hemlock_server_creds that are stored
                        # notify end user, and give them the option to opt out
                        resp = ""
                        while resp != 'y' and resp != 'n':
                            resp = raw_input("This action will overwrite any existing hemlock server credentials previously stored, are you sure you want to do this? (y/n)")
                            resp = resp.lower()
                        if resp == 'y':
                            data_action = "TRUNCATE TABLE hemlock_server"
                            self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                            cur.execute(data_action)
                            results = cur.fetchall()
                            self.log.debug(debug, "Successfully executed the following SQL query: "+data_action)
                            self.log.debug(debug, "Results: "+str(results))

                            # store hemlock server credentials
                            data_action = "INSERT INTO "+action_a[0]+"_server("
                            i = 0
                            j = -1
                            for prop in props:
                                if prop == "credential_file": 
                                    data_action += "credentials, "
                                    j = i
                                else:
                                    data_action += prop+", "
                                i += 1
                            data_action = data_action[:-2]+") VALUES("
                            i = 0
                            for val in vals:
                                if j == i:
                                    #    instead of val, val is the file to open,
                                    #    read in and then convert to a json object to store
                                    #    encrypted values with AES
                                    try:
                                        cred_dict = {}
                                        f = open(val, 'r')
                                        for line in f:
                                            if len(line) > 0 and line[0] != "#" and "=" in line:
                                                entry_a = line.split("=")
                                                cred_dict[entry_a[0].strip()] = entry_a[1].strip()
                                        f.close()
                                        creds = json.dumps(cred_dict)
                                        data_action += "AES_ENCRYPT(\""+creds.replace('"','\\"')+"\", \""+aes_key+"\"), "
                                    except:
                                        error = 1
                                        print "Unable to read credentials file"
                                        sys.exit(0)
                                else:
                                    data_action += "\""+val+"\", "
                                i += 1
                            data_action = data_action[:-2]+")"
                        else:
                            data_action = ""
                        self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                elif "client" in action_a:
                    if "get" in action_a:
                        # get a client
                        data_action = "SELECT * FROM "+action_a[0]+"s WHERE uuid = '"+var_d['--uuid']+"'"
                        self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                    elif "list" in action_a:
                        # list clients
                        data_action = "SELECT * FROM "+action_a[0]+"s"
                        self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                    # purge, run, schedule, and store are not read only
                    # delete
                    elif "purge" in action_a:
                        # delete clients
                        data_action = "DELETE FROM schedules_clients WHERE client_id = '"+var_d['--uuid']+"'"
                        data_action2 = "DELETE FROM systems_clients WHERE client_id = '"+var_d['--uuid']+"'"
                        data_action3 = "DELETE FROM clients WHERE uuid = '"+var_d['--uuid']+"'"
                        self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                        self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action2)
                        self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action3)
                    # write
                    elif "run" in action_a:
                        # run a client for data push/pull
                        hemlock_base = Hemlock_Base()
                        hemlock_runner = Hemlock_Runner()

                        # client type using the client_uuid
                        data_action = "SELECT type FROM clients WHERE uuid = '"+var_d['--uuid']+"'"
                        self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                        cur.execute(data_action)
                        results = cur.fetchall()
                        self.log.debug(debug, "Successfully executed the following SQL query: "+data_action)
                        self.log.debug(debug, "Results: "+str(results))
                        var_d['--client'] = results[0][0]

                        args = []
                        for key in var_d:
                            args.append(key)
                            args.append(var_d[key])
                        client_uuid, client, splits = hemlock_base.process_args(debug, args)

                        CLIENT_CREDS_FILE, c_inst = hemlock_base.client_import(debug, client)

                        # using the client_uuid get the system_id
                        data_action = "SELECT * from systems_clients where client_id = '"+client_uuid+"'"
                        self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                        cur.execute(data_action)
                        results = cur.fetchall()
                        self.log.debug(debug, "Successfully executed the following SQL query: "+data_action)
                        self.log.debug(debug, "Results: "+str(results))
                        system_uuid = str(results[0][0]) 

                        # get client_dict and server_dict that are stored in mysql
                        client_dict, server_dict = hemlock_runner.get_creds(debug, m_server, client_uuid, aes_key)
                        # verify that the system exists and is properly associated
                        hemlock_base.verify_system(debug, system_uuid, server_dict)

                        h_server = hemlock_base.connect_server(debug, server_dict, no_couchbase)

                        if not client.startswith("stream"):
                            c_server = c_inst.connect_client(debug, client_dict)
                        else:
                            c_server = c_inst.connect_client(debug, client_dict, h_server, client_uuid)
                        data_list = []
                        desc_list = []

                        if not client.startswith("stream"):
                            data_list, desc_list = c_inst.get_data(debug, client_dict, c_server, h_server, system_uuid, no_couchbase)
                        hemlock_base.send_data(debug, data_list, desc_list, h_server, system_uuid, no_couchbase)
                        hemlock_base.update_hemlock(debug, system_uuid, server_dict)
                    # write
                    elif "schedule" in action_a:
                        # !! TODO ensure that the same client is not added to the same schedule more than once
                        # create a schedule that is associated with a client

                        data_action = "INSERT INTO schedules("
                        data_action2 = "INSERT INTO schedules_"+action_a[0]+"s("
                        i = 0
                        k = -1
                        for prop in props:
                            if prop == "client_id":
                                data_action2 += prop+", schedule_id) VALUES("
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
                        self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                        self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action2)
                    # write
                    elif "store" in action_a:
                        # !! TODO add a parameter that has the no_couchbase flag
                        # store client credentials
                        data_action = "INSERT INTO "+action_a[0]+"s("
                        data_action2 = "INSERT INTO systems_"+action_a[0]+"s("
                        i = 0
                        j = -1
                        k = -1

                        # add couchbase flag for use with scheduling
                        data_action += "no_couchbase, "

                        for prop in props:
                            if prop == "credential_file": 
                                data_action += "credentials, "
                                j = i
                            elif prop == "system_id":
                                data_action2 += prop+", client_id) VALUES("
                                k = i
                            else:
                                data_action += prop+", "
                            i += 1
                        data_action = data_action[:-2]+") VALUES("

                        # add couchbase flag for use with scheduling
                        data_action += "\""+str(no_couchbase)+"\", "

                        i = 0
                        for val in vals:
                            if j == i:
                                #    instead of val, val is the file to open,
                                #    read in and then convert to a json object to store
                                #    encrypted values with AES
                                try:
                                    cred_dict = {}
                                    f = open(val, 'r')
                                    for line in f:
                                        if len(line) > 0 and line[0] != "#" and "=" in line:
                                            entry_a = line.split("=")
                                            cred_dict[entry_a[0].strip()] = entry_a[1].strip()
                                    f.close()
                                    creds = json.dumps(cred_dict)
                                    data_action += "AES_ENCRYPT(\""+creds.replace('"','\\"')+"\", \""+aes_key+"\"), "
                                except:
                                    error = 1
                                    self.log.debug(debug, str(sys.exc_info()[0]))
                                    print "Unable to read credentials file"
                                    sys.exit(0)
                            elif k == i:
                                data_action2 += "\""+val+"\", \""+uid+"\")"
                            else:
                                data_action += "\""+val+"\", "
                            i += 1
                        if k == -1:
                            data_action2 = ""
                        data_action = data_action[:-2]+")"
                        self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                        self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action2)
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
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                    cur.execute(data_action)
                    results = cur.fetchall()
                    self.log.debug(debug, "Successfully executed the following SQL query: "+data_action)
                    self.log.debug(debug, "Results: "+str(results))
                    tables =  [x[0] for x in results]

                    # for each table, get data and field names
                    for table in tables:
                        table_array = []
                        # get field names of each table
                        data_action = "DESC "+table
                        self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                        cur.execute(data_action)
                        results = cur.fetchall()
                        self.log.debug(debug, "Successfully executed the following SQL query: "+data_action)
                        self.log.debug(debug, "Results: "+str(results))
                        # get data from each table
                        data_action = "SELECT * FROM "+table
                        self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                        cur.execute(data_action)
                        results2 = cur.fetchall()
                        self.log.debug(debug, "Successfully executed the following SQL query: "+data_action)
                        self.log.debug(debug, "Results: "+str(results2))
                        # match up field names and data into a dictionary
                        for entry in results2:
                            item_dict = {}
                            for field, item in zip([x[0] for x in results], entry):
                                # do not return user's passwords
                                if field != "password" and field != "credentials":
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
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
            try:
                if data_action:
                    cur.execute(data_action)
                    self.log.debug(debug, "Successfully executed the following SQL query: "+data_action)
                if data_action2:
                    cur.execute(data_action2)
                    self.log.debug(debug, "Successfully executed the following SQL query: "+data_action2)
                if data_action3:
                    cur.execute(data_action3)
                    self.log.debug(debug, "Successfully executed the following SQL query: "+data_action3)
            except:
                error = 1
                print "not valid"
                sys.exit(0)

        results = cur.fetchall()
        self.log.debug(debug, "Results: "+str(results))
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
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                elif "clients" in action_a:
                    # schedule
                    data_action = "desc "+action_a[0]+"s_clients"
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                elif "tenants" in action_a:
                    # system
                    data_action = "desc "+action_a[0]+"s_tenants"
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                elif "users" in action_a:
                    if "tenant" in action_a:
                        data_action = "desc "+action_a[1]+"_tenants"
                    # role
                    else:
                        data_action = "desc "+action_a[1]+"_roles"
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                elif "schedules" in action_a:
                    # client
                    data_action = "desc "+action_a[1]+"_clients"
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                elif "systems" in action_a:
                    if "tenant" in action_a:
                        data_action = "desc "+action_a[1]+"_tenants"
                    # client
                    else:
                        data_action = "desc "+action_a[1]+"_clients"
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                elif "schedule" in action_a and "server" in action_a:
                    data_action = "desc schedule_servers"
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                else:
                    data_action = "desc "+action_a[0]+"s"
                    self.log.debug(debug, "Getting ready to perform the following SQL query: "+data_action)
                cur.execute(data_action)
                desc_results = cur.fetchall()
                self.log.debug(debug, "Successfully executed the following SQL query: "+data_action)
                self.log.debug(debug, "Results: "+str(desc_results))

                if len(results) == 1 and "list" not in action_a:
                    vals = list(results[0])
                    i = 0
                    while i < len(desc_results):
                        if desc_results[i][0] != "password" and desc_results[i][0] != "credentials":
                            x.append([desc_results[i][0],vals[i]])
                        i += 1
                else:
                    if "clients" in action_a:
                        tab_header = ['Client ID']
                        tab_align = ['c']
                        i = 0
                        a = -1
                        while i < len(desc_results):
                            if desc_results[i][0] == 'client_id':
                                a = i
                            i += 1
                        i = 0
                        while i < len(results):
                            x.append([results[i][a]])
                            i += 1
                    elif "roles" in action_a:
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
                    elif "schedules" in action_a:
                        tab_header = ['Schedule ID']
                        tab_align = ['c']
                        i = 0
                        a = -1
                        while i < len(desc_results):
                            if desc_results[i][0] == 'schedule_id':
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

        if "query" not in action_a and "start" not in action_a and "remove" not in action_a and "delete" not in action_a and "deregister" not in action_a and "all" not in action_a and "run" not in action_a and "purge" not in action_a:
            print tab.draw()
        return x, error

if __name__ == "__main__":
    start_time = time.time()
    hemlock = Hemlock()
    args, user, pw, db, server, c_server, c_user, bucket, c_pw, es, debug, no_couchbase = hemlock.get_auth()
    var_d, action = hemlock.process_args(debug, args)
    m_server = hemlock.mysql_server(debug, server, user, pw, db)

    x, error = hemlock.process_action(debug, action, var_d, m_server, c_server, c_user, bucket, c_pw, no_couchbase, es)
    hemlock.log.debug(debug, "Rows: "+str(x))
    hemlock.log.debug(debug, "Errors encountered: "+str(error))

    try:
        m_server.commit()
        m_server.close()
        hemlock.log.debug(debug, "Successfully closed the MySQL connection")
    except:
        print "Failed to close the MySQL connection."
        hemlock.log.debug(debug, str(sys.exc_info()[0]))
    print "Took",time.time() - start_time,"seconds to complete."
