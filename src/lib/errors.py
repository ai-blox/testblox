# Authors
# - Hans Stevens
#
# Copyright (c)
#
# This file is part of testblox
#
# testblox is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# testblox is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pysfdisk.  If not, see <http://www.gnu.org/licenses/>


class TestBloxException(Exception):
    """Base expception for testblox."""

    # pylint: disable=unnecessary-pass
    pass

class NotRunningAsRoot(TestBloxException):
    """Command is not running as root."""

    # pylint: disable=unnecessary-pass
    pass

class BlockDeviceDoesNotExist(TestBloxException):
    """Block device does not exists."""

    # pylint: disable=unnecessary-pass
    pass
