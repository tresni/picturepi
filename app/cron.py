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
import os
from functools import wraps
from crontab import CronTab

cronfile = os.environ.get('CRONTAB', os.path.join(os.getcwd(), 'crontab'))


def crontab(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            crontab = CronTab(tabfile=cronfile)
        except FileNotFoundError:
            with open(cronfile, 'a'):
                pass
            crontab = CronTab(tabfile=cronfile)

        return f(*args, crontab=crontab, **kwargs)
    return decorator


def cronjob(name, user="root", command="echo"):
    def inner(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            crontab = kwargs['crontab']
            job = None
            try:
                job = next(crontab.find_comment(name))
            except StopIteration:
                job = crontab.new(comment=name, user=user, command=command)

            args = args + (job,)
            return func(*args, **kwargs)
        return decorator
    return inner
