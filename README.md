# testblox

This is a test script for testing a BLOX device

## Setup

There is a setup script which helps you to install all the necessary packages.
You can run this script with:

```shell
sudo ./setup.sh
```

## Run

This script need to be run as root.

Example use
```shell
$ sudo python3 main.py --tb S360V0.1 --config config.yml --debug
```


## Remote PyCharm debugging 

This chapter describes how you can use PyCharm to run this script remotely.
The problem is that this script need to be run as root. PyCharm doesn't support this standard.
But there is lucky a workaround.

### Don't require a password running sudo python

```shell
sudo visudo -f /etc/sudoers.d/python
```

Add a line of the form:

```shell
<user> ALL = (root) NOPASSWD: <full path to python>
```

For example:
````shell
ai-blox ALL = (root) NOPASSWD: /home/ai-blox/.virtualenvs/testblox/python
````

### Create a sudo script

Call the script python-sudo.sh, containing (with your correct full python path):

```shell
#!/bin/bash
sudo /home/ai-blox/.virtualenvs/testblox/python "$@"
```

Be sure the script is executable

```shell
chmod +x python-sudo.sh
```

### Use the scrip as your Python interpreter

In PyCharm, go to Settings > Project Interpreter. Click the gear icon by the current Project Interpreter drop-down, and choose "Add…". Then choose Existing environment. Browse to python-sudo.sh and select it, and set it as the interpreter for the project.

Now when you run or debug, the code will run as root

## How to create a new partition table file

Create first a partition table with `fdisk` and apply this partition table.

Afterwards, you can export the partition table with following command.
Chose a logical name.

```shell 
$ sudo sfdisk -d /dev/mmcblk1 > partition-table-name.txt
```

Save the generated file in the partition-tables directory