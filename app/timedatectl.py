#! /usr/bin/python3
# Copyright (C) 2020 Brian Hartvigsen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import subprocess

__timezones = None


def getTimezone():
    cp = subprocess.run(['timedatectl', '--property=Timezone', '--value', 'show'], capture_output=True, text=True)
    return cp.stdout.strip()


def listTimezones():
    global __timezones
    if not __timezones:
        cp = subprocess.run(['timedatectl', 'list-timezones'], capture_output=True, text=True)
        __timezones = cp.stdout.strip().split('\n')
    return __timezones


def setTimezone(tz):
    if tz not in listTimezones():
        raise ValueError("%s is not a valid timezone" % tz)

    cp = subprocess.run(['timedatectl', '--no-ask-password', 'set-timezone', tz], capture_output=True, text=True)
    if cp.returncode:
        raise ValueError(cp.stderr.strip())
    return cp.returncode
