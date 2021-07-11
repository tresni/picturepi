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
from app.timedatectl import listTimezones

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField
from wtforms.fields import FieldList
from wtforms.fields.html5 import TimeField
from wtforms.validators import URL


class ScreenTimeForm(FlaskForm):
    on = TimeField("on")
    off = TimeField("off")


class PhotoRetrievalForm(FlaskForm):
    frequency = SelectField('Frequency', choices=[
        ('15', '15 minutes'),
        ('30', '30 minutes'),
        ('hourly', 'hourly'),
        ('daily', 'daily')
    ])


class TimeZoneForm(FlaskForm):
    timezone = SelectField('Timezone', choices=list(zip(listTimezones(), listTimezones())))


class AlbumsForm(FlaskForm):
    albums = FieldList(StringField('Albums', [URL(), ]))
