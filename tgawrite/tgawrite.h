/*
Copyright (c) 2016 Don Bright
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1. Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/
/*
 write RGB pixels to tga image file
 see also http://paulbourke.net/dataformats/tga/ , http://www.cplusplus.com
 http://stackoverflow.com/questions/16538945/writing-uncompressed-tga-to-file-in-c
 this is designed to be small, simple, easy to understand, and easy to modify.
 splitting colors using the union allows modification for various pixel formats.
 just switch the order in the union and you can use a different rgba order.
*/

#include <stdio.h>
#include <stdint.h>

uint32_t tgawrite( const char *fname, uint32_t *pixels, uint16_t w, uint16_t h )
{
	union pixl8 {
		uint8_t blue,green,red,alpha;
		uint32_t data;
	} pixel;
	FILE *f = fopen( fname, "wb" );
	uint8_t tgaheader[18] = {0,0,2,0,0,0,0,0,0,0,0,0,w,w>>8,h,h>>8,32,0};
	fwrite( tgaheader, 1, 18, f );
	for ( uint32_t i=0; i<w*h; pixel.data = pixels[i], i++ ) {
			putc( pixel.blue, f );
			putc( pixel.green, f );
			putc( pixel.red, f );
			putc( pixel.alpha, f );
	}
	fclose( f );
}

