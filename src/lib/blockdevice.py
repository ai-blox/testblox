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

import os
import json
import pathlib
import subprocess
from hfilesize import FileSize
from typing import Union
from subprocess import PIPE
from src.lib.partition import Partition
from src.lib.errors import NotRunningAsRoot, BlockDeviceDoesNotExist


def find_executable(name: str) -> Union[str, classmethod]:
    """
    Return valid executable path for provided name.
    :param name: binary, executable name
    :return: Return the string representation of the path with forward (/) slashes.
    """
    standard_executable_paths = ["/bin", "/sbin", "/usr/local/bin", "/usr/local/sbin", "/usr/bin", "/usr/sbin"]

    for path in standard_executable_paths:
        executable_path = pathlib.Path(path) / name
        if executable_path.exists():
            return executable_path.as_posix()

    return FileNotFoundError


class BlockDevice(object):
    LSBLK_EXEC = find_executable(name="lsblk")
    SUDO_EXEC = find_executable(name="sudo")
    SFDISK_EXEC = find_executable(name="sfdisk")
    FDISK_EXEC = find_executable(name="fdisk")
    CAT_EXEC = find_executable(name="cat")
    BLOCKDEV_EXEC = find_executable(name="blockdev")
    MKFS_EXEC = find_executable(name="mkfs")

    def __init__(self, path, use_sudo=False):
        # Setup member variables
        self.path = path
        self.use_sudo = use_sudo
        self.partitions = {}
        self.label = None
        self.uuid = None
        self.sector_size = None
        self.disk_size = None

        # self._assert_root()
        # self._ensure_exists()

    def read_partition_table(self):
        """Create the partition table using sfdisk and load partitions"""
        command_list = [self.SFDISK_EXEC, "--json", self.path]
        if self.use_sudo:
            command_list.insert(0, self.SUDO_EXEC)
        disk_config = json.loads(subprocess.check_output(command_list))
        self.label = disk_config["partitiontable"]["label"] or None
        self.uuid = disk_config["partitiontable"]["id"] or None

        for partition_config in disk_config["partitiontable"]["partitions"]:
            partition = Partition.load_from_sfdisk_output(partition_config, self)
            self.partitions[partition.get_partition_number()] = partition

        physical_block_size = "/sys/block/{device}/queue/physical_block_size".format(device=self.path.split('/')[-1])
        command_list = [self.CAT_EXEC, physical_block_size]
        if self.use_sudo:
            command_list.insert(0, self.SUDO_EXEC)
        self.sector_size = int(subprocess.check_output(command_list))

        command_list = [self.BLOCKDEV_EXEC, "--getsize64", self.path]
        if self.use_sudo:
            command_list.insert(0, self.SUDO_EXEC)
        self.disk_size = int(subprocess.check_output(command_list))

        if (self.label is None) or (self.uuid is None) or (self.sector_size is None) or (self.disk_size is None):
            return False

        return True

    def get_disk_size(self):
        return self.disk_size

    def check_disk_size(self, size):
        disk_size = FileSize(self.get_disk_size())
        expt_size = FileSize(size)
        if (disk_size >= (expt_size * 0.9)) and (disk_size <= disk_size):
            return True
        else:
            return False

    def get_partition(self, partition):
        return self.partitions.get(str(partition), None)

    def get_partition_size(self, partition):
        partition = self.get_partition(partition)
        if partition is None:
            size = 0
        else:
            size = '{:.0fH}'.format(FileSize(int(partition.size * self.sector_size)))
        return size

    def check_partition_size(self, partition, size):
        disk_size = FileSize(self.get_partition_size(partition))
        expt_size = FileSize(size)
        if (disk_size >= (expt_size * 0.9)) and (disk_size <= disk_size):
            return True
        else:
            return False

    def apply_partition_table(self, partition_table):
        command = "sudo sfdisk /dev/mmcblk1 < partion-tables/{table}".format(table=partition_table)
        process = subprocess.Popen(command, stdin=PIPE, stdout=PIPE, shell=True)
        process.communicate()

        if process.returncode == 0:
            return True
        else:
            return False

    def format_partition(self, partition, type):

        if self.get_partition(partition) is None:
            return False

        command_list = [self.MKFS_EXEC, "-t", type, "{path}p{partition}".format(path=self.path,  partition=partition)]
        if self.use_sudo:
            command_list.insert(0, self.SUDO_EXEC)
        subprocess.check_output(command_list)

        return True

    ### Old code
    def lsblk(self):
        block_list_json = subprocess.check_output(['lsblk', '-J'])
        block_list = json.loads(block_list_json)

        if 'blockdevices' in block_list:
            self.block_list = block_list['blockdevices']
            return True

        return False

    def find_block_device(self):
        for block in self.block_list:
            if block['name'] == self.path:
                return block
        return None

    def get_block_device_size(self, device):
        blck_size = None
        block = self.find_block_device(device)
        if block is not None:
            blck_size = float(block['size'][:-1])
            unit = block['size'][-1]
        return {'size': blck_size, 'unit': unit}

    def check_block_device_size(self, device, expected_size):
        blck_size = self.get_block_device_size(device)
        if (blck_size['size'] >= (expected_size['size'] * 0.9)) and (blck_size['size'] <= (expected_size['size'])) and (
                blck_size['unit'] == expected_size['unit']):
            return True
        else:
            return False

    def _assert_root(self):
        """Ensure that the script is being run as root"""
        if os.getuid() != 0:
            raise NotRunningAsRoot("Must be running as root")

    def _ensure_exists(self):
        if not os.path.exists(self.path):
            raise BlockDeviceDoesNotExist("Block device %s does not exist" % self.path)


if __name__ == "__main__":
    disk = BlockDevice('/dev/mmcblk1')
