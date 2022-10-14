# Disk test unit

## Config parameters

**Mandantory**
- name: the name will be displayed in the logging 
- path: reference to the block device e.g. mmcblk1
- size: the expected disk size given with a size and unit key, e.g.:
  ```yaml
  blk_size:
     size: 64
     unit: G 
    ```

**Optional**
- partition_table: link to a partition table json file. If provided, the sd card will be configured with the partition table. 

## Config example
```yaml
name: 'usdc'
blk_id: mmcblk1
blk_size:
  size: 64
  unit: G
partition_table: 64GB_P5_32GB_P6_32GB.json
```