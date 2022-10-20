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

from src.units.base import BaseUnit

class Apt(BaseUnit):

    def __init__(self, config):
        super().__init__(config)

        self.logger.info('Initialize apt unit')

        self.commands = self.check_config_parameter('commands', mandatory=True)

        if self.commands is None:
            self.logger.error('Failed to initialize disk test unit')
            return

        self.disk = BlockDevice(self.path)

        self.initialized = True

    def state_0(self):