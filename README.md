# s360



## Setup

If you want to use this project for remote debugging with PyCharm


## How to create a new partition table file

Create first a partition table with `fdisk` and apply this partition table.
Afterwards, you can export the partition table with following command.
Chose a logical name.

```shell 
$ sudo sfdisk -J /dev/mmcblk1 > partition-table-name.txt
```

**Step 3:**

Save the file in the partition-tables directory