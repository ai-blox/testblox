from pca95xx import PCA95XX_GPIO
from time import sleep

# Assumes a PCA9555 with 16 GPIO's at address 0x20
chip = PCA95XX_GPIO(0, 0x74, 16)

chip.setup(0, PCA95XX_GPIO.OUT) #DO1
chip.setup(1, PCA95XX_GPIO.OUT) #DO3
chip.setup(2, PCA95XX_GPIO.OUT) #DO2
chip.setup(3, PCA95XX_GPIO.OUT) #DO4
chip.setup(4, PCA95XX_GPIO.OUT) #DO5
chip.setup(5, PCA95XX_GPIO.OUT) #DO6
chip.setup(6, PCA95XX_GPIO.OUT) #DO7
chip.setup(7, PCA95XX_GPIO.IN) #DI1
chip.setup(8, PCA95XX_GPIO.IN) #DI2
chip.setup(9, PCA95XX_GPIO.IN) #DI3
chip.setup(10, PCA95XX_GPIO.IN) #DI4
chip.setup(11, PCA95XX_GPIO.IN) #DI5
chip.setup(12, PCA95XX_GPIO.IN) #DI6
chip.setup(13, PCA95XX_GPIO.OUT) #GREEN
chip.setup(14, PCA95XX_GPIO.OUT) #RED

di1 = 0
di2 = 0
di3 = 0
di4 = 0
di5 = 0
di6 = 0

while(True):
    if di1 != chip.input(7):
        di1 = chip.input(7)
        if di1 > 0:
            chip.output(0, 1)
            print("DI1=0")
        else:
            chip.output(0, 0)
            print("DI1=1")

    if di2 != chip.input(8):
        di2 = chip.input(8)
        if di2 > 0:
            chip.output(2, 0)
            print("DI2=0")
        else:
            chip.output(2, 1)
            print("DI2=1")

    if di3 != chip.input(9):
        di3 = chip.input(9)
        if di3 > 0:
            chip.output(1, 0)
            print("DI3=0")
        else:
            chip.output(1, 1)
            print("DI3=1")

    if di4 != chip.input(10):
        di4 = chip.input(10)
        if di4 > 0:
            chip.output(3, 0)
            print("DI4=0")
        else:
            chip.output(3, 1)
            print("DI4=1")
                    
    if di5 != chip.input(11):
        di5 = chip.input(11)
        if di5 > 0:
            chip.output(4, 0)
            chip.output(14, 0)
            print("DI5=0")
        else:
            chip.output(4, 1)
            chip.output(14, 1)
            print("DI5=1")

    if di6 != chip.input(12):
        di6 = chip.input(12)
        if di6 > 0:
            chip.output(5, 0)
            chip.output(13, 0)
            print("DI6=0")
        else:
            chip.output(5, 1)
            chip.output(13, 1)
            print("DI6=1")

    sleep(0.1)
