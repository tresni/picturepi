#! /usr/bin/env python3
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
from datetime import datetime
from random import randrange

from flask import Flask, render_template as render

from app.forms import *
from app.cron import crontab, cronjob
from app.timedatectl import getTimezone, setTimezone

app = Flask(__name__)
app.secret_key = b"Z\xfa_'@D\xe4\x07'\xd7\x91a\x12A\x97\xdb"

# @authenicated
@app.route('/')
def index():
    return render('index.jinja')

# @authenticated
@app.route('/retrieve', methods=['POST', 'GET'])
@crontab
@cronjob("retrieve photos")
def retrieve(retrieve, crontab):
    frequency = None
    if retrieve.hours == "*":
        try:
            int(str(retrieve.minutes))
            frequency = "hourly"
        except ValueError:
            if retrieve.minutes == "*/15":
                frequency = 15
            if retrieve.minutes == "*/30":
                frequency = 30
    else:
        frequency = "daily"
    form = PhotoRetrievalForm(data={"frequency": frequency})
    if form.validate_on_submit():
        retrieve.clear()
        if form.frequency.data in ["hourly", "daily"]:
            retrieve.minute.on(randrange(60))
            if form.frequency.data == "daily":
                retrieve.hour.on(randrange(24))
        else:
            retrieve.minute.every(form.frequency.data)
        crontab.write()
    return render('photos.jinja', form=form)

# @authenticated
@app.route('/screen', methods=['POST', 'GET'])
@crontab
@cronjob("photo screen on", "echo -n 0 > /sys/class/backlight/rpi_backlight/bl_power")
@cronjob("photo screen off", "echo -n 1 > /sys/class/backlight/rpi_backlight/bl_power")
def screen(on, off, crontab):
    data = {"on": on.schedule().get_next(datetime) if on else on,
            "off": off.schedule().get_next(datetime) if off else off}

    form = ScreenTimeForm(data=data)
    if form.validate_on_submit():
        on.setall(form.on.data)
        off.setall(form.off.data)
        crontab.write()
    return render('screen.jinja', form=form)


@app.route('/timezone', methods=['POST', 'GET'])
def timezone():
    form = TimeZoneForm(data={"timezone": getTimezone()})
    if form.validate_on_submit():
        setTimezone(form.timezone.data)
    return render('timezone.jinja', form=form)
