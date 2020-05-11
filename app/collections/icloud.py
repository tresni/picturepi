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
import os.path
from random import choice
from urllib.parse import urlparse

import base62
import requests

BASE_URL = "https://p%02d-sharedstreams.icloud.com/%s"
STREAMS_URL = "%s/sharedstreams/webstream"
ASSETS_URL = "%s/sharedstreams/webasseturls"


class icloudCollection(object):
    def __init__(self, album):
        self.album = album

    def getPhotos(self, output):
        album = self.album
        if album[0] == "A":
            shard = base62.decode(album[1])
        else:
            shard = base62.decode(album[1:3])

        s = requests.Session()

        base = BASE_URL % (shard, album)
        r = s.post(STREAMS_URL % base, json={"streamCtag": None})
        photostream = r.json()
        wanted = list(map(lambda x: x["derivatives"][max(x["derivatives"], key=int)]["checksum"], photostream["photos"]))

        photos = map(lambda x: x["photoGuid"], photostream["photos"])
        r = s.post(ASSETS_URL % base, json={"photoGuids": list(photos)})
        assets = r.json()

        filenames = []

        for k, p in assets["items"].items():
            if k not in wanted:
                continue

            loc = assets["locations"][p["url_location"]]
            url = "%s://%s%s" % (loc["scheme"], choice(loc["hosts"]), p["url_path"])
            _, ext = os.path.splitext(urlparse(url).path)
            localfn = os.path.join(output, "%s%s" % (k, ext))
            filenames.append(localfn)
            if os.path.exists(localfn):
                continue

            photo = s.get(url)
            with open(localfn, 'wb') as fd:
                for chunk in photo.iter_content(chunk_size=128):
                    fd.write(chunk)

        return filenames
