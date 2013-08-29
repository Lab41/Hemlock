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

from hemlock_debugger import Hemlock_Debugger
from apscheduler.scheduler import Scheduler
import logging
import signal

class Hemlock_Scheduler():
    def __init__(self):
        self.log = Hemlock_Debugger()

    def job_work(self):
        # do actual work here
        # !! TODO
        test_log2 = open('scheduler.log', 'a')
        test_log2.write("bar")
        test_log2.close() 

    def init_schedule(self):
        logging.basicConfig(level=logging.DEBUG)
        sched = Scheduler()

        # Start the scheduler
        sched.start()

        return sched

    def schedule_job(self, sched, function, periodicity, start_time):
        sched.add_interval_job(function, seconds=periodicity, start_date=start_time)

if __name__ == "__main__":
    hemlock_scheduler = Hemlock_Scheduler()
    sched = hemlock_scheduler.init_schedule()
    # example schedules
    # !! TODO
    hemlock_scheduler.schedule_job(sched, hemlock_scheduler.job_work, 120, '2013-08-29 12:30:09')
    hemlock_scheduler.schedule_job(sched, hemlock_scheduler.job_work, 120, '2013-08-29 12:31:03')

    # APSScheduler.Scheduler only works until the main thread exits
    signal.pause()
