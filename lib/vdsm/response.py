#
# Copyright 2008-2015 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#
# Refer to the README and COPYING files for full details of the license
#


from vdsm.define import doneCode
from vdsm.define import errCode


def success(message=None, **kwargs):
    kwargs["status"] = {
        "code": doneCode["code"],
        "message": message or doneCode["message"]
    }
    return kwargs


def error(name, message=None):
    status = errCode[name]["status"]
    return {
        "status": {
            "code": status["code"],
            "message": message or status["message"]
        }
    }
