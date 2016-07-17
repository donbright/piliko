// test of tgawrite.h, copyright don bright 2016
// see license.txt for license

#include "tgawrite.h"

int patterns[7]={2,3,5,2*3,5*3,2*5,2*3*5};

// see also http://paulbourke.net/fractals/circlesquares/index.html
// see also https://www.youtube.com/watch?v=kRHKbJMm6xE
void makepattern(uint32_t *pixels,uint16_t w,uint16_t h,int color) {
	uint8_t pixel[4] = {0,0,0,0};
	for (uint16_t i=0;i<h;i++) {
		for (uint16_t j=0;j<w;j++) {
			if (color%3==0) pixel[0] = i*i-j*j; // red
			if (color%5==0) pixel[1] = 2*i*j; // green
			if (color%2==0) pixel[2] = i*i+j*j; // blue
			pixel[3] = 255; // alpha
			// uncomment the following line to verify test failures
			// if (color%5==0) pixel[1] = 2*i*j+1;
			pixels[w*i+j] = *((uint32_t*)&pixel);
		}
		//printf("\n");
	}
}

// test results(actual on this machine) against models (ideal)
void tests()
{
	for (int i=0;i<7;i++) {
		char fnamem[20];
		sprintf(fnamem,"thismachine%02d.tga",patterns[i]);
		FILE *fm = fopen( fnamem ,"rb");
		char fnamer[20];
		sprintf(fnamer,"testmodel%02d.tga",patterns[i]);
		FILE *fr = fopen( fnamer ,"rb");
		int test,mc,rc;
		test=mc=rc=1;
		while ( (mc!=EOF) && (rc!=EOF) ) {
			mc = fgetc(fm);
			rc = fgetc(fr);
			test &= (mc==rc);
			//printf("%i %i %i %i %i\n",i,mc==EOF,rc==EOF,mc!=EOF,rc!=EOF);
		}
		printf("test %s v %s: %s\n",fnamem,fnamer,test==1?"ok":"fail");
		fclose(fm);
		fclose(fr);
	}
}

int main() {
	uint16_t w = 512;
	uint16_t h = 256;
	uint32_t pixels[w*h];

	for (int i=0;i<7;i++) {
		char fname[20];
		sprintf(fname,"thismachine%02d.tga",patterns[i]);
		//sprintf(fname,"testmodel%02d.tga",patterns[i]);//gen models
		FILE *f = fopen( fname ,"wb");
		makepattern(pixels,w,h,patterns[i]);
		int32_t result = tgawrite(pixels,w,h,f);
		printf("%i bytes written to %s\n",result,fname);
		fclose(f);
	}
	tests();
}
