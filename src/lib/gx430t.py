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


class GX430t(object):
    def __init__(self, name, printer=None, label_type=1):
        self.logger = logging.getLogger(name)
        self.logger.info('Initialize GX430t module')
        self.printer = printer
        self.labelType = label_type
        self.dotsPerMm = 12
        self.dotsPerInch = 304.8

        if printer is None:
            return

        #if label_type == 1:
        #    self.set_label_size(50.8, 3.175, 25.4)
        #elif label_type == 2:
        #    self.set_label_size(32, 3, 57)
        #else:
        #    self.logger.error('Unknown label type')

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
        commands += '%s\n' % label
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
        label += '^PW600\n'
        label += '^LL600\n'
        label += '^LH30,30\n'

        # Label width: 50.8, -> 590 dots
        # Label height: 25.4, -> 290 dots

        label += '^FX Black bar with serial number\n'
        label += '^FO0,0^GB560,60,60^FS\n'
        label += '^FO15,17\n'
        label += '^FR\n'
        label += '^AC,40\n'
        label += '^FDSN: %s^FS\n' % box_serial_number

        label += '^FX Second section with MAC addresses\n'
        label += '^AAN,30,17\n'
        label += '^FO5,85\n'
        label += '^FDMAC: %s^FS\n' % mac_internet
        label += '^AA,20\n'
        label += '^FO455,90\n'
        label += '^FD(INTERNET)^FS\n'

        label += '^AAN,30,17\n'
        label += '^FO5,140\n'
        label += '^FDMAC: %s^FS\n' % mac_camera
        label += '^AA,20\n'
        label += '^FO455,145\n'
        label += '^FD(CAMERA)^FS\n'

        label += '^FX Third section with bar code.\n'
        label += '^FO20,190^BY2^BC,60,Y,N,N,A^FD%s^FS\n' % box_serial_number

        label += '^FO465,180^GFA,1260,1260,15,,::::::::O0FFP01FE,N0IFO01FFE,M07IFO0IFE,L01JFN03IFE,L07JFN0JFE,L0KFM01JFE,K01KFM07JFE,K07KFM0KFE,K0LFL01KFE,J01JF8M03JF,J03IFCN07IF,J03FFEO0IFC,J07FFCO0IF8,J0IFO01FFE,I01FFEO03FFC,I01FFCO03FF8,I03FF8O07FF,I03FFP07FE,I07FFP0FFC,I07FEP0FFC,I07FCP0FF8,I0FFCO01FF8,I0FF8O01FF,::001FF8O03FF,001FFP03LF8,:::::::001FF8O03LF8,I0FF8O03FF,I0FF8O01FF,:I0FFCO01FF8,I07FCO01FF8,I07FEP0FFC:I03FFP07FE,I03FF8O07FF,I01FFCO03FF8,I01FFEO03FFC,J0IFO01FFE,J07FF8O0IF,J07FFEO0IFC,J03IF8N07IF,J01JFN03IFE,K0LFL01KFE,K07KFM0KFE,K03KFM07JFE,L0KFM01JFE,L07JFN0JFE,L01JFN03IFE,M07IFO0IFE,M01IFO03FFE,N01FFP03FE,,::::::::::::::^FS'

        label += '^XZ\n'

        self.print_label(label)


def main():
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

        printer = GX430t("GX430t", 'GX430t', 1)
        printer.print_s360_label("SN360N120120ABCDEF", "12:34:56:78:90:ab:cd", "ab:cd:12:34:56:78:90")

if __name__ == '__main__':
    main()
