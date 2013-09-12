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
This module controlls and runs the scheduler for performing actions between
client systems and the Hemlock server.

Created on 30 August 2013
@author: Charlie Lewis
"""

from apscheduler.scheduler import Scheduler
from clients.hemlock_debugger import Hemlock_Debugger
from hemlock import Hemlock

import logging
import MySQLdb as mdb
import signal
import sys

class Hemlock_Scheduler():
    """
    This class is responsible for spawning and controlling the the scheduler
    and all operations that are scheduled in a cron-like fashion.
    """

    def __init__(self):
        self.log = Hemlock_Debugger()
        self.sched = self.init_schedule()
        args = []
        for arg in sys.argv:
            args.append(arg)
        try:
            self.path = args[1]
        except:
            print "No path provided, defaulting to 'hemlock_creds' in the current working directory"
            self.path = "hemlock_creds"

        try:
            self.debug = args[2]
        except:
            self.debug = 0

    def check_schedules(self):
        """
        Checks for existing schedules, cleans up ones that no longer need to
        run, starts new ones that need to be scheduled.
        """
        server_dict = {}
        #    check environment variables first, then check for creds file
        try:
            server_dict['HEMLOCK_MYSQL_SERVER'] = os.environ['HEMLOCK_MYSQL_SERVER']
            server_dict['HEMLOCK_MYSQL_USERNAME'] = os.environ['HEMLOCK_MYSQL_USERNAME']
            server_dict['HEMLOCK_MYSQL_PW'] = os.environ['HEMLOCK_MYSQL_PW']
        except:
            # read in hemlock server creds file
            try:
                self.log.debug(self.debug, "Opening server_creds file: "+self.path)
                f = open(self.path, 'r')
                self.log.debug(self.debug, "Server creds file handle: "+str(f))
                for line in f:
                    self.log.debug(self.debug, line)
                    if len(line) > 0 and line[0] != "#" and "=" in line:
                        # split each line on the first '='
                        line = line.split("=",1)
                        try:
                            server_dict[line[0]] = line[1].strip()
                        except:
                            print "Malformed Server Creds file."
                            self.log.debug(self.debug, sys.exc_info()[0])
                            sys.exit(0)
                f.close()
            except:
                print "Unable to open "+self.path
                self.log.debug(self.debug, sys.exc_info()[0])
                sys.exit(0)

        # connect to the mysql server
        try:
            m_server = mdb.connect(server_dict['HEMLOCK_MYSQL_SERVER'],
                                   server_dict['HEMLOCK_MYSQL_USERNAME'],
                                   server_dict['HEMLOCK_MYSQL_PW'],
                                   "hemlock")

            self.log.debug(self.debug, "MySQL Handle: "+str(m_server))
        except:
            self.log.debug(self.debug, sys.exc_info()[0])
            print "MySQL server failure"
            sys.exit(0)

        cur = m_server.cursor()
        self.log.debug(self.debug, "MySQL Cursor: "+str(cur))

        cur.execute("SELECT * FROM schedules")
        results = cur.fetchall()
        self.log.debug(self.debug, str(results))

        # !! TODO
        #    remove schedules that are not stored
        jobs = self.sched.get_jobs()
        for job in jobs:
            test_log2 = open('scheduler.log', 'a')
            test_log2.write(str(job)+"\n")
            test_log2.write(str(job.name)+"\n")
            test_log2.close() 

        #    read schedules that are stored
        for schedule in results:
            self.schedule_job_cron(self.job_work, str(schedule[1]), str(schedule[1]), str(schedule[3]), str(schedule[4]), str(schedule[5]), str(schedule[6]), str(schedule[7]))

        # !! TODO
        #    query to get everything in schedules
        #    updates schedules

    def job_work(self, args):
        """
        Do the actual work that was scheduled at the scheduled tiem.

        :param args: job arguments
        """
        # DEBUG
        # do actual work here
        # !! TODO
        #    if streaming is already running and requested again, ignore
        #    if the job requested, regardless, is still running, skip this run, and log it
        test_log2 = open('scheduler.log', 'a')
        test_log2.write("test: ")
        test_log2.write(str(args))
        test_log2.write("\n")
        test_log2.close() 

    def init_schedule(self):
        """
        Initialize the scheduler.

        :return: an instance of the scheduler.
        """
        # DEBUG
        logging.basicConfig(filename='scheduler.log', level=logging.DEBUG)
        sched = Scheduler()

        # Start the scheduler
        sched.start()

        return sched

    def schedule_job(self, function, periodicity, start_time):
        """
        Schedule a new job.

        :param function: function to be called that does the work
        :param periodicity: how often to run the scheduled work
        :param start_time: when to start the job
        """
        # DEBUG
        self.sched.add_interval_job(function, seconds=periodicity, start_date=start_time)

    def schedule_job_cron(self, function, args, name, minute, hour, day_of_month, month, day_of_week):
        """
        Schedule a new cron job.

        :param function: function to be called that does the work
        :param args: arguments to pass to the function that does the work
        :param name: name of the job
        :param minute: cron minute to run the job
        :param hour: cron hour to run the job
        :param day_of_month: cron day_of_month to run the job
        :param month: cron month to run the job
        :param day_of_week: cron day_of_week to run the job
        """
        # DEBUG
        self.sched.add_cron_job(function, args=['foo'], name=name, minute=minute, hour=hour, day=day_of_month, month=month, day_of_week=day_of_week)

if __name__ == "__main__":
    hemlock_scheduler = Hemlock_Scheduler()
    logging.basicConfig(filename='scheduler.log', level=logging.DEBUG)

    # DEBUG
    # run every 60 seconds
    hemlock_scheduler.schedule_job(hemlock_scheduler.check_schedules, 60, '2013-08-29 12:32:43')

    # APSScheduler.Scheduler only works until the main thread exits
    signal.pause()
