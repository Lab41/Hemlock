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
This module is used for running a debugger across all modules in Hemlock.

Create on 28 August 2013
@author: Charlie Lewis
"""

class Hemlock_Debugger():
    """
    This class is responsible for printing out debug statements as well as
    write them to file.
    """

    def debug(self, debug, string):
        """
        Prints and logs all debug statements.

        :param debug: instance of
            :class:`~hemlock.clients.hemlock_debugger.Hemlock_Debugger`
        :param string: stringified version of whatever is being debugged.
        """
        if debug:
            print string
            f = open('debug.log', 'a')
            f.write(string+"\n")
            f.close()
