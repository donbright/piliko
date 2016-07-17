// test of tgawrite.h, copyright don bright 2016
// see license.txt for license
// pattern -
// see also http://paulbourke.net/fractals/circlesquares/index.html
// see also https://www.youtube.com/watch?v=kRHKbJMm6xE

#include "tgawrite.h"

int main() {
	uint16_t w = 512;
	uint16_t h = 256;
	uint32_t pixels[w*h];
	uint8_t pixel[4];
	for (uint16_t i=0;i<h;i++) {
		for (uint16_t j=0;j<w;j++) {
			pixel[0] = i*i-j*j; // red
			pixel[1] = 2*i*j; // green
			pixel[2] = i*i+j*j; // blue
			pixel[3] = 255; // alpha
			pixels[w*i+j] = *((uint32_t*)&pixel);
		}
	}
	FILE *f = fopen( "simple.tga" ,"wb");
	uint32_t result = tgawrite(pixels,w,h,f);
	fclose(f);
	printf("wrote %u bytes to simple.tga\n",result);
}

