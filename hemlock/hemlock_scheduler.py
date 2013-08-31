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

from apscheduler.scheduler import Scheduler
from clients.hemlock_debugger import Hemlock_Debugger
from hemlock import Hemlock

import logging
import MySQLdb as mdb
import signal
import sys

class Hemlock_Scheduler():
    def __init__(self):
        self.log = Hemlock_Debugger()
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
        server_dict = {}

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

        test_log2 = open('scheduler.log', 'a')
        test_log2.write(str(results))
        test_log2.close() 

        # !! TODO
        #    query to get everything in schedules
        #    updates schedules

    def job_work(self):
        # DEBUG
        # do actual work here
        # !! TODO
        test_log2 = open('scheduler.log', 'a')
        test_log2.write("bar")
        test_log2.close() 

    def init_schedule(self):
        # DEBUG
        logging.basicConfig(level=logging.DEBUG)
        sched = Scheduler()

        # Start the scheduler
        sched.start()

        return sched

    def schedule_job(self, sched, function, periodicity, start_time):
        # DEBUG
        sched.add_interval_job(function, seconds=periodicity, start_date=start_time)

if __name__ == "__main__":
    hemlock_scheduler = Hemlock_Scheduler()
    logging.basicConfig(level=logging.DEBUG)
    sched = hemlock_scheduler.init_schedule()
    # example schedules
    # !! TODO
    # DEBUG
    hemlock_scheduler.schedule_job(sched, hemlock_scheduler.check_schedules, 300, '2013-08-29 12:32:43')
    hemlock_scheduler.schedule_job(sched, hemlock_scheduler.job_work, 120, '2013-08-29 12:30:09')
    hemlock_scheduler.schedule_job(sched, hemlock_scheduler.job_work, 120, '2013-08-29 12:31:03')

    # APSScheduler.Scheduler only works until the main thread exits
    signal.pause()
