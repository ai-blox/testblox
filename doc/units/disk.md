# Disk test unit

## Config parameters

**Mandantory**
- name: the name will be displayed in the logging 
- path: reference to the block device e.g. mmcblk1
- size: the expected disk size e.g. 64G

**Optional**
- partition_table: link to a partition table json file. If provided, the sd card will be configured with the partition table. 
- format: define which partitions need to be formatted e.g.:
  ```yaml
  format:
      -
        partition: 5
        type: ext4
  ```
## Config example
```yaml
name: 'uSDCard'
path: '/dev/mmcblk1'
size: 64G
partition_table: 64GB_P5_32GB_P6_32GB
format:
    -
      partition: 5
      type: ext4
    -
      partition: 6
      type: ext4
```