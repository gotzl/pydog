#include <stdio.h>  
#include <stdint.h>

void getbuffer(uint8_t * buf, uint8_t * pixels, int width, int height) {
    int x,y,greyscale;
    for(y=0;y<height;y++) {
        for(x=0;x<width;x++) {
            greyscale = ((pixels[y*width + x])/0x40)&0x3;
            buf[y/4 * width + x] |= ( greyscale << ((y % 4)<<1) );
        }
    }
}