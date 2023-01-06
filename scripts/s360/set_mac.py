import os
import sys
import smbus
import time

bus = smbus.SMBus(1)

START_MAC = 0x8C1F643B703C

def program_eth0_mac(mac):

    addr = 0x05

    for ele in range(0, 8*6, 8):
        byte = ((mac >> ele) & 0xff)
        #print("Write to " + hex(addr) + ', byte: ' + hex(byte) )
        bus.write_byte_data(0x50, addr, byte)
        time.sleep(0.1)
        addr -= 1


def program_eth1_mac(mac):

    addr = 0x15

    for ele in range(0, 8 * 6, 8):
        byte = ((mac >> ele) & 0xff)
        #print("Write to " + hex(addr) + ', byte: ' + hex(byte) )
        bus.write_byte_data(0x50, addr, byte)
        time.sleep(0.1)
        addr -= 1


def calculate_mac(box):

    offset = (box - 31) * 2
    eth_mac = [0, 0]
    eth_mac[0] = START_MAC + offset
    eth_mac[1] = START_MAC + offset  + 1

    return eth_mac


if __name__ == "__main__":

    if not os.geteuid() == 0:
        sys.exit("\nOnly root can run this script\n")

    print('set fan to max')
    with open('/sys/devices/pwm-fan/target_pwm', 'w') as text_file:
        print('255', file=text_file)

    print('Enter box number:')
    box_num = int(input())

    if (box_num < 31) or (box_num > 330):
        print('box number need to be between 31 and 330')
        exit()

    eth_mac = calculate_mac(box_num)

    print("MAC Address eth0 : ", end="")
    print(':'.join(['{:02x}'.format((eth_mac[0] >> ele) & 0xff)
                    for ele in range(0, 8 * 6, 8)][::-1]))
    program_eth0_mac(eth_mac[0])

    print("MAC Address eth1 : ", end="")
    print(':'.join(['{:02x}'.format((eth_mac[1] >> ele) & 0xff)
                    for ele in range(0, 8 * 6, 8)][::-1]))
    program_eth1_mac(eth_mac[1])

