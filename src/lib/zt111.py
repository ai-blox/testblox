#!/usr/bin/env python
import logging
import subprocess

# EPL2 Programming manual can be found here:
# https://support.zebra.com/cpws/docs/eltron/epl2/EPL2_Prog.pdf

class ZT111(object):
    def __init__(self, name, printer=None, label_type=1):
        self.logger = logging.getLogger(name)
        self.logger.info('Initialize ZT111 module')
        self.printer = printer
        self.labelType = label_type
        self.dotsPerMm = 8
        self.dotsPerInch = 203

        if printer is None:
            return

        if label_type == 1:
            self.set_label_size(12.7, 3.175, 50.8)
        else:
            self.logger.error('Unknown label type')

    def get_printers(self):
        printers = []
        try:
            output = subprocess.check_output(['lpstat', '-p'], universal_newlines=True)
        except subprocess.CalledProcessError:
            return []
        for line in output.split('\n'):
            if line.startswith('printer'):
                printers.append(line.split(' ')[1])
        return printers

    def set_printer(self, printer, dots_per_mm=None):
        self.printer = printer
        if dots_per_mm:
            self.dotsPerMm = dots_per_mm

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

    def print_MAC_label(self, macaddress):
        label = None
        if self.labelType == 1:
            label = "A45,10,1,2,1,1,N,\"{0}\"\nA75,10,1,2,1,1,N,\"MAC ADDRESS\"\nb95,6,Q,s6,eH,\"{0}\"".format(
                macaddress)
        elif self.labelType == 2:
            label = "A30,12,1,2,1,1,N,\"{0}\"\nb42,22,Q,s5,eH,\"{0}\"".format(macaddress)
        else:
            self.logger.error('Unknown label type')

        if label:
            label.decode("ascii", "ignore")
            self.print_label(label)

    def print_error_label(self, mac, test_report):
        label = None
        if self.labelType == 1:
            label = 'A20,10,0,2,1,1,N,"MAC: ' + mac + '"\n'
        elif self.labelType == 2:
            label = 'A20,10,0,2,1,1,N,"' + mac + '"\n'
        else:
            self.logger.error('Unknown label type')

        if label:
            y = 35
            results = test_report
            for errorName in results.iterkeys():
                label += 'A20,' + str(y) + ',0,2,1,1,N,"' + errorName + '"\n'
                y += 20

            self.print_label(label)

    def print_dict(self, input_dict):
        output = ''
        x_pos = 5
        y_pos = 5
        X_INC = 10
        Y_INC = 17
        for k in sorted(input_dict):
            output += 'A%d,%d,0,1,1,1,N,' % (x_pos, y_pos)
            output += '"%s:"\n' % k
            # spread on 2 lines, and cut
            L = 20
            v = ', '.join(input_dict[k])
            output += 'A%d,%d,0,1,1,1,N,"%s"\n' % (x_pos+3*X_INC, y_pos, v[:L])
            output += 'A%d,%d,0,1,1,1,N,"%s"\n' % (x_pos+4*X_INC, y_pos+Y_INC, v[L:2*L])
            y_pos += 2*Y_INC
        self.print_label(output)

    def reset_to_default(self):
        commands = '\n'
        commands += '^default\n'
        self._output(commands)
        self.logger.debug("Send command: " + commands.replace('\n', '\\n'))

    def _output(self, commands):
        p = subprocess.Popen(['lpr', '-P{}'.format(self.printer), '-oraw'], stdin=subprocess.PIPE)
        p.communicate('{}\n'.format(commands).encode('utf-8'))
        p.stdin.close()


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

    printer = ZT111("ZT111", 'Zebra_ZT111', 1)

    #label = '\n'
    #label += 'A40,6,1,2,1,1,N,"AI-BLOX"\n'
    #label += 'A65,10,0,1,1,1,N,"MX1030-1 - 10.30.0001 - S/N:23044"\n'
    #label += 'A65,30,0,2,1,1,N,"Xavier NX 8Gb, Headless"\n'
    #label += 'LE55,5,2,85\n'
    #label += 'B85,55,0,3,3,1,30,N,"10.30.0001"\n'

    #label = '\n'
    #label += 'A40,6,1,2,1,1,N,"AI-BLOX"\n'
    #label += 'A65,10,0,1,1,1,N,"MX1030-2 - 10.30.0002 - S/N:23046"\n'
    #label += 'A65,30,0,2,1,1,N,"Xavier NX 8Gb, 7\\" Touch"\n'
    #label += 'LE55,5,2,85\n'
    #label += 'B85,55,0,3,3,1,30,N,"10.30.0002"\n'

    label = '\n'
    label += 'A40,6,1,2,1,1,N,"AI-BLOX"\n'
    label += 'A65,10,0,1,1,1,N,"MX1030-3 - 10.30.0003 - S/N:23047"\n'
    label += 'A65,30,0,2,1,1,N,"Xavier NX 16Gb, Headless"\n'
    label += 'LE55,5,2,85\n'
    label += 'B85,55,0,3,3,1,30,N,"10.30.0003"\n'

    #label = '\n'
    #label += 'A40,6,1,2,1,1,N,"AI-BLOX"\n'
    #label += 'A65,10,0,1,1,1,N,"MX1030-4 - 10.30.0004 - S/N:23039"\n'
    #label += 'A65,30,0,2,1,1,N,"Xavier NX 16Gb, 7\\" Touch"\n'
    #label += 'LE55,5,2,85\n'
    #label += 'B85,55,0,3,3,1,30,N,"10.30.0004"\n'

    #label = '\n'
    #label += 'A40,6,1,2,1,1,N,"AI-BLOX"\n'
    #label += 'A65,10,0,1,1,1,N,"MX1010-1 - 10.10.0001 - S/N:23042"\n'
    #label += 'A65,30,0,2,1,1,N,"Nano, Headless"\n'
    #label += 'LE55,5,2,85\n'
    #label += 'B85,55,0,3,3,1,30,N,"10.10.0001"\n'

    #label = '\n'
    #label += 'A40,6,1,2,1,1,N,"AI-BLOX"\n'
    #label += 'A65,10,0,1,1,1,N,"MX1010-2 - 10.10.0002 - S/N:23030"\n'
    #label += 'A65,30,0,2,1,1,N,"Nano, 7\\" Touch"\n'
    #label += 'LE55,5,2,85\n'
    #label += 'B85,55,0,3,3,1,30,N,"10.10.0002"\n'

    #label = '\n'
    #label += 'A40,6,1,2,1,1,N,"AI-BLOX"\n'
    #label += 'A65,10,0,1,1,1,N,"MX1020-2 - 10.20.0002 - S/N:23039"\n'
    #label += 'A65,30,0,2,1,1,N,"TX2 NX, 7\\" Touch"\n'
    #label += 'LE55,5,2,85\n'
    #label += 'B85,55,0,3,3,1,30,N,"10.20.0002"\n'

    #label = '\n'
    #label += 'A40,6,1,2,1,1,N,"AI-BLOX"\n'
    #label += 'A65,10,0,1,1,1,N,"CB-0210 - 10.50.0210 - S/N:23003"\n'
    #label += 'A65,30,0,2,1,1,N,"GigE + LTE Cat. 4"\n'
    #label += 'LE55,5,2,85\n'
    #label += 'B85,55,0,3,3,1,30,N,"10.50.0210"\n'

    #label = '\n'
    #label += 'A40,6,1,2,1,1,N,"AI-BLOX"\n'
    #label += 'A65,10,0,1,1,1,N,"CB-0010 - 10.50.0010 - S/N:23025"\n'
    #label += 'A65,30,0,2,1,1,N,"GigE comm module"\n'
    #label += 'LE55,5,2,85\n'
    #label += 'B85,55,0,3,3,1,30,N,"10.50.0010"\n'

    #label = '\n'
    #label += 'A40,6,1,2,1,1,N,"AI-BLOX"\n'
    #label += 'A65,10,0,1,1,1,N,"CB-0110 - 10.50.0110 - S/N:23006"\n'
    #label += 'A65,30,0,2,1,1,N,"GigE + Wifi comm module"\n'
    #label += 'LE55,5,2,85\n'
    #label += 'B85,55,0,3,3,1,30,N,"10.50.0110"\n'

    #label = '\n'
    #label += 'A40,6,1,2,1,1,N,"AI-BLOX"\n'
    #label += 'A65,10,0,1,1,1,N,"CB-0210 - 10.50.0210 - S/N:23001"\n'
    #label += 'A65,30,0,2,1,1,N,"GigE + LTE Cat 4 comm module"\n'
    #label += 'LE55,5,2,85\n'
    #label += 'B85,55,0,3,3,1,30,N,"10.50.0210"\n'

    #label = '\n'
    #label += 'A40,6,1,2,1,1,N,"AI-BLOX"\n'
    #label += 'A65,10,0,1,1,1,N,"CB-0010 - 10.60.0005 - S/N:23009"\n'
    #label += 'A65,30,0,2,1,1,N,"BLOX Programming Device"\n'
    #label += 'LE55,5,2,85\n'
    #label += 'B85,55,0,3,3,1,30,N,"10.60.0005"\n'

    #label = '\n'
    #label += 'A40,6,1,2,1,1,N,"AI-BLOX"\n'
    #label += 'A65,10,0,1,1,1,N,"IB-0100 - 10.40.0100 - S/N:23003"\n'
    #label += 'A65,30,0,2,1,1,N,"6-Ch MIPI with USB 3.0"\n'
    #label += 'LE55,5,2,85\n'
    #label += 'B85,55,0,3,3,1,30,N,"10.40.0100"\n'

    #label = '\n'
    #label += 'A40,6,1,2,1,1,N,"AI-BLOX"\n'
    #label += 'A65,10,0,1,1,1,N,"IB-0210 - 10.40.0210 - S/N:23010"\n'
    #label += 'A65,30,0,2,1,1,N,"4-Ch USB 3.0 with 4-DO/DI"\n'
    #label += 'LE55,5,2,85\n'
    #label += 'B85,55,0,3,3,1,30,N,"10.40.0210"\n'

    #label = '\n'
    #label += 'A40,6,1,2,1,1,N,"AI-BLOX"\n'
    #label += 'A65,10,0,1,1,1,N,"IB-0310 - 10.40.0310 - S/N:23016"\n'
    #label += 'A65,30,0,2,1,1,N,"4-Ch 100Mb Eth with 4-DO/DI"\n'
    #label += 'LE55,5,2,85\n'
    #label += 'B85,55,0,3,3,1,30,N,"10.40.0310"\n'

    #label = '\n'
    #label += ' \n'
    #label += 'LE25,6,2,85\n'
    #label += 'A40,15,0,2,1,1,N,"MX1020-2"\n'
    #label += 'A40,40,0,2,1,1,N,"10.20.0002"\n'
    #label += 'A40,65,0,2,1,1,N,"2023010039"\n'
    #label += 'LE200,6,2,85\n'

    #label = '\n'
    #label += ' \n'
    #label += 'LE25,6,2,85\n'
    #label += 'A40,15,0,2,1,1,N,"MX1010-1"\n'
    #label += 'A40,40,0,2,1,1,N,"10.10.0001"\n'
    #label += 'A40,65,0,2,1,1,N,"2023010042"\n'
    #label += 'LE200,6,2,85\n'

    #label = '\n'
    #label += ' \n'
    #label += 'LE25,6,2,85\n'
    #label += 'A40,15,0,2,1,1,N,"MX1030-2"\n'
    #label += 'A40,40,0,2,1,1,N,"10.30.0002"\n'
    #label += 'A40,65,0,2,1,1,N,"2023010046"\n'
    #label += 'LE200,6,2,85\n'

    #label = '\n'
    #label += ' \n'
    #label += 'LE25,6,2,85\n'
    #label += 'A40,15,0,2,1,1,N,"MX1030-3"\n'
    #label += 'A40,40,0,2,1,1,N,"10.30.0003"\n'
    #label += 'A40,65,0,2,1,1,N,"2023010037"\n'
    #label += 'LE200,6,2,85\n'

    #label = '\n'
    #label += ' \n'
    #label += 'LE25,6,2,85\n'
    #label += 'A40,15,0,2,1,1,N,"MX1030-4"\n'
    #label += 'A40,40,0,2,1,1,N,"10.30.0004"\n'
    #label += 'A40,65,0,2,1,1,N,"2023010040"\n'
    #label += 'LE200,6,2,85\n'

    #label = '\n'
    #label += ' \n'
    #label += 'LE25,6,2,85\n'
    #label += 'A40,15,0,2,1,1,N,""\n'
    #label += 'A40,40,0,2,1,1,N,"1   2   3"\n'
    #label += 'A40,65,0,2,1,1,N,""\n'
    #label += 'LE200,6,2,85\n'

    printer.print_label(label)

if __name__ == '__main__':
    main()
