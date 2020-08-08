import time
import sys
import os
import numpy

dogxl_c = False
try:
    import pydog_helper
    dogxl_c = True
except Exception as e:  print("Could not load dogxl C helper library:", e)

class DOGXL(object):
    def __init__(self, RST_PIN = 24, DC_PIN = 25, CS_PIN = 8):
        import RPi.GPIO
        import spidev


        self.RST_PIN = RST_PIN
        self.DC_PIN = DC_PIN
        self.CS_PIN = CS_PIN
        self.width = 160
        self.height = 104
        self.invisible_pages = (128-104)//4
        self.GPIO = RPi.GPIO
        # SPI device, bus = 0, device = 0
        self.SPI = spidev.SpiDev(0, 0)
        self.module_init()
        self.ldc_init()

    def module_init(self):
        self.GPIO.setmode(self.GPIO.BCM)
        self.GPIO.setwarnings(False)
        self.GPIO.setup(self.RST_PIN, self.GPIO.OUT)
        self.GPIO.setup(self.DC_PIN, self.GPIO.OUT)
        self.GPIO.setup(self.CS_PIN, self.GPIO.OUT)
        self.SPI.max_speed_hz = 4000000
        self.SPI.mode = 0b00
        return 0

    def module_exit(self):
        self.SPI.close()

        self.GPIO.output(self.RST_PIN, 0)
        self.GPIO.output(self.DC_PIN, 0)

        self.GPIO.cleanup([self.RST_PIN, self.DC_PIN, self.CS_PIN])

    def ldc_init(self):
        self.GPIO.output(self.RST_PIN, 0)
        time.sleep(0.01)
        self.GPIO.output(self.RST_PIN, 1)
        time.sleep(0.01)
        init_seq = [ 0xf1, 0x67, 0xc0, 0x40, 0x50, 0x2b, 0xeb, 0x81, 0x5f, 0x89, 0xaf]
        self.send_command(init_seq)
        # clear the ram
        self.send_data([0x0]*(self.width*self.height//4))

    def lcd_exit(self):
        # send display sleep
        self.send_command(0xae)

    def digital_write(self, pin, value):
        self.GPIO.output(pin, value)

    def digital_read(self, pin):
        return self.GPIO.input(pin)

    def spi_writebyte(self, data):
        self.SPI.writebytes2(data)

    def send_command(self, command):
        self.digital_write(self.DC_PIN, 0)
        self.digital_write(self.CS_PIN, 0)
        if not isinstance(command, list):
            command = [command]
        self.spi_writebyte(command)
        self.digital_write(self.CS_PIN, 1)

    def send_data(self, data):
        self.digital_write(self.DC_PIN, 1)
        self.digital_write(self.CS_PIN, 0)
        if not isinstance(data, list) and not isinstance(data, numpy.ndarray):
            data = [data]
        self.spi_writebyte(data)
        self.digital_write(self.CS_PIN, 1)

    def set_pixel(self, buf, pos=None, size=None):
        # update only a part of the ram        
        if pos is not None and size is not None:
            # set column start address
            self.send_command([0xf4, pos[0]])
            # set page start address
            self.send_command([0xf5, pos[1]])

            # set column end address
            self.send_command([0xf6, pos[0]+size[0]])
            # set page end address
            self.send_command([0xf7, pos[1]+size[1]])

            # enable window program
            self.send_command(0xf9)
            # send the data
            self.send_data(buf)
            # disable window progam
            self.send_command(0xf8)

        else:
            # send 'invisible' pages
            self.send_data([0x0] * (self.width * self.invisible_pages))            
            # send the data
            self.send_data(buf)

    @staticmethod
    def getbuffer(image):
        image_monocolor = image.convert('L')
        imwidth, imheight = image_monocolor.size
        buf = numpy.zeros(imwidth * imheight//4, dtype=numpy.uint8)

        # move bit arithmetic to C code for acceleration
        if dogxl_c:
            data = numpy.asarray(image_monocolor)
            pydog_helper.getbuffer(buf, data, imwidth, imheight)
            buf = buf.tolist()
        else:
            pixels = image_monocolor.load()
            for y in range(imheight):
                for x in range(imwidth):
                    greyscale = ((pixels[x, y])//0x40)&0x3
                    buf[y//4 * imwidth + x] |= ( greyscale << ((y % 4)<<1) )
        return buf