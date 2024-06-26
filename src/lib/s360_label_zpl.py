#!/usr/bin/env python3
import logging
import time
import subprocess
import os

# EPL2 Programming manual can be found here:
# https://support.zebra.com/cpws/docs/eltron/epl2/EPL2_Prog.pdf

import PIL
# we only want to exercise the PCX code for now: unregister all other plugins so our input
# doesn't get recognized as those formats. not getting recognized as a PCX should just lead to
# a single boring path that doesn't distract the fuzzing process.
PIL._plugins[:] = ["PcxImagePlugin"]

from PIL import Image
import codecs
from io import BytesIO
import sys


class S360LabelZpl(object):
    def __init__(self, name, printer=None, label_type=1):
        self.logger = logging.getLogger(name)
        self.logger.info('Initialize S360LabelZpl module')
        self.printer = printer
        self.labelType = label_type
        self.dotsPerMm = 8
        self.dotsPerInch = 203

        if printer is None:
            return

        if label_type == 1:
            self.set_label_size(12.7, 3.175, 50.8)
        elif label_type == 2:
            self.set_label_size(32, 3, 57)
        else:
            self.logger.error('Unknown label type')

        self.set_print_head_resistance("0784")
        self.set_ribbon_tension("L")


    def set_printer(self, printer, dots_per_mm=None):
        self.printer = printer
        if dots_per_mm:
            self.dotsPerMm = dots_per_mm

    def set_print_head_resistance(self, resistance):

        commands = '\n'
        commands += '^SR%s\n' % (resistance)
        self.logger.debug("Send command: " + commands.replace('\n', '\\n'))
        self._output(commands)

    def set_ribbon_tension(self, tension):

        commands = '\n'
        commands += '^SJW%s\n' % (tension)
        self.logger.debug("Send command: " + commands.replace('\n', '\\n'))
        self._output(commands)

    def set_label_size(self, heigth, distance, width, in_inch=False):
        if not in_inch:
            dots = self.dotsPerMm
        else:
            dots = self.dotsPerInch

        commands = '\n'
        commands += 'S0\nD14\n'
        commands += ('Q%s,%s\n' % (int(heigth * dots), int(distance * dots)))
        commands += ('q%s\n' % int(width * dots))
        self.logger.debug("Send command: " + commands.replace('\n', '\\n'))
        self._output(commands)

    def print_label(self, label):
        commands = '\n'
        commands += 'N\n'
        commands += '%s\n' % label
        commands += 'P\n'
        self._output(commands)
        self.logger.debug("Send command: " + commands.replace('\n', '\\n'))

    def store_graphics(self, name, image_file):

        with open(image_file, 'rb') as image:
            try:
                Image.open(image).getdata()
            except Exception:
                pass

        with open(image_file, 'rb') as image:

            image_size = os.path.getsize(image_file)

            commands = b'\n'
            commands += b'GM"%s"%d\n' % (name.encode('utf-8'), image_size)

            commands += image.read()

            commands += b'\n'
            self._output_raw(commands)
            self.logger.debug("Send command: " + str(commands).replace('\n', '\\n'))

    def print_graphics_infomation(self):
        commands = '\n'
        commands += 'GI\n'
        self._output(commands)
        self.logger.debug("Send command: " + commands.replace('\n', '\\n'))
    def delete_graphics(self, name):
        commands = '\n'
        commands += 'GK"%s"\n'% name
        self._output(commands)
        self.logger.debug("Send command: " + commands.replace('\n', '\\n'))

    def delete_all_graphics(self):
        commands = '\n'
        commands += 'GK"*"\n'
        self._output(commands)
        self.logger.debug("Send command: " + commands.replace('\n', '\\n'))

    def print_graphics(self, name, x, y):
        commands = '\n'
        commands += 'N\n'
        commands += 'GG%s,%s,"%s"\n' % (int(x), int(y), name)
        commands += 'P\n'
        self._output(commands)
        self.logger.debug("Send command: " + commands.replace('\n', '\\n'))

    def reset_to_default(self):
        commands = '\n'
        commands += '^default\n'
        self._output(commands)
        self.logger.debug("Send command: " + commands.replace('\n', '\\n'))


    def _output(self, commands):
        p = subprocess.Popen(['lpr', '-P{}'.format(self.printer), '-oraw'], stdin=subprocess.PIPE)
        p.communicate('{}\n'.format(commands).encode('utf-8'))
        p.stdin.close()

    def _output_raw(self, commands):
        p = subprocess.Popen(['lpr', '-P{}'.format(self.printer), '-oraw'], stdin=subprocess.PIPE)
        p.communicate(commands)
        p.stdin.close()


    def print_s360_label(self, box_serial_number, mac_internet, mac_camera):

        label = '^XA\n'

        # Label width: 51, 51 * 8 = 408
        # Label height: 25, 25 * 8 = 200
        # label += '^FO30,10^GB408,200,2^FS\n'

        label += '^FX Black bar with serial number\n'
        # label += '^FO30,20^GB300,60,2^FS\n'
        label += '^FO20,50\n'
        label += '^FR\n'
        label += '^AC,40\n'
        label += '^FDSN: S360N120120^FS\n'

        label += '^XZ\n'


        self.print_label(label)


def main():
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

        printer = S360LabelZpl("ZT111", 'Zebra_ZT111', 2)
        printer.print_s360_label("SN360N1291292ABCDEF", "12:34:56:78:90:ab:cd", "ab:cd:12:34:56:78:90")

if __name__ == '__main__':
    main()
