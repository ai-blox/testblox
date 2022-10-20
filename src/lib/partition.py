"""Code for handling information about partitions."""

# Authors
#
# - pre-alpha 0.0.1 2016 - Matt Comben
# - GA 1.0.0 2020 - Tomasz Szuster
# - testblox - Hans Stevens
#
# Copyrigh (c)
#
# This file is part of testblox.
#
# testblox is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# pysfdisk is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pysfdisk.  If not, see <http://www.gnu.org/licenses/>

import re


class Partition:
    """Interface for defining partitions."""

    @staticmethod
    def load_from_sfdisk_output(config, block_device):
        """Generate partition object from output of sfdisk."""
        if "node" not in config:
            return None

        if "start" not in config:
            return None

        if "size" not in config:
            return None

        partition_number = re.match("^.*([0-9]+)$", config["node"]).group(1)
        partition_config = {
            "node": config["node"],
            "uuid": config["uuid"] if "uuid" in config else None,
            "start": int(config["start"]),
            "size": int(config["size"]),
            "attrs": config["attrs"] if "attrs" in config else None,
            "type": config["type"] if "type" in config else None,
        }
        return Partition(partition_number=partition_number, block_device=block_device, **partition_config)

    def __init__(self, partition_number, block_device, **kwargs):
        """Set member variables."""
        self.block_device = block_device
        self.partition_number = partition_number
        for config_name in kwargs:
            setattr(self, config_name, kwargs[config_name])

    def get_partition_number(self) -> str:
        """
        Obtain partition number.
        :return: the partition number
        """
        return self.partition_number