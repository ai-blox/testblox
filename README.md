# testblox

This is a test script for testing a BLOX device

This script need to be run as root.

Example use
```shell
$ sudo python main.py --tb S360V0.1 --config config.yml --debug
```


## Setup [TODO]

If you want to use this project for remote debugging with PyCharm


## How to create a new partition table file

Create first a partition table with `fdisk` and apply this partition table.

Afterwards, you can export the partition table with following command.
Chose a logical name.

```shell 
$ sudo sfdisk -d /dev/mmcblk1 > partition-table-name.txt
```

Save the generated file in the partition-tables directory