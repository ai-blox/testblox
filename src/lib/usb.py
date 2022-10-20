import re
import subprocess
import os
import sys


class Usb(object):

    def __init__(self):
        self.devices = []

    def scan(self):
        index = 0
        device_re = re.compile(b"Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$",
                               re.I)
        df = subprocess.check_output("lsusb")
        self.devices = []
        for i in df.split(b'\n'):
            if i:
                info = device_re.match(i)
                if info:
                    dinfo = info.groupdict()
                    dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
                    dinfo['index'] = index
                    index = index + 1
                    self.devices.append(dinfo)

    def find_by_id(self, id):
        search_result = []

        for device_info in self.devices:
            if device_info['id'] == id:
                search_result.append(device_info)

        return search_result

    def find_by_bus(self, bus, device):

        dev = "/dev/bus/usb/b'{bus:03d}'/b'{device:03d}'".format(bus=bus, device=device)
        for device_info in self.devices:
            if device_info['device'] == dev:
                return device_info

        return None


if __name__ == "__main__":

    if not os.geteuid() == 0:
        sys.exit("\nOnly root can run this script\n")

    usb = Usb()
    usb.scan()
    print(usb.find_by_id('0424:9512'))
    print(usb.find_by_bus(1, 2))
