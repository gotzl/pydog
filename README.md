Small library to interface [EA DOG LCD](https://www.lcd-module.com/produkte/dog.html) displays. Currently, only the DOGXL160-7 is supported with 4-wire SPI communication.

## Installation
```
# install
pip install . # --user

# uninstall
pip uninstall pydog
```

## Dependencies
```
pip install numpy rpi-gpio spidev smbus # --user
```

## Usage example
```
from pydog import DOGXL
dpl = DOGXL()

# full update
img = Image.new('L', (dpl.width, dpl.height), 0)
img = ImageDraw.Draw(Himage)
img.line((0, 0 , dpl.width, dpl.height), fill = 0xff)
dpl.set_pixel(DOGXL.getbuffer(img))

# partial (windowed) update
# height has to be multiple of 4 !
img = Image.new('L', (60, 4*10), 0)
img = ImageDraw.Draw(Himage)
img.line((0, 0 , img.width, img.height), fill = 0xff)
# update window, rectangle at pixel (20,20)
# y-position has to be multiple of 4 !
dpl.set_pixel(DOGXL.getbuffer(img), 
        pos=(20, 20//4),
        size=(img.size[0],img.size[1]//4))
dpl.lcd_exit()
dpl.module_exit()
```