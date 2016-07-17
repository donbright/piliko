#ifndef __tgawrite_h__
#define __tgawrite_h__
/*
Copyright (c) 2016 Don Bright http://github.com/donbright
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
 write RGBA pixels to tga image file BGRA.
 see also http://paulbourke.net/dataformats/tga/ , http://www.cplusplus.com
 http://stackoverflow.com/questions/16538945/writing-uncompressed-tga-to-file-in-c
 this is designed to be small, simple, easy to understand, and easy to modify.
 splitting colors using the union allows modification for various pixel formats
 and endianness. just switch the order in the union and you can use a different
 rgba order as input. FILE *F must be open in binary mode ('wb').
 return is -1 on failure, # of pixel bytes+18 on success
*/

#include <stdio.h>
#include <stdint.h>

int32_t tgawrite( uint32_t *pixels, uint16_t w, uint16_t h, FILE *f )
{
	struct data8_t {
		uint8_t red; uint8_t green; uint8_t blue; uint8_t alpha;
	};
	union pixel_t {
		struct data8_t data8;
		uint32_t data32;
	} pixel;
	uint8_t tgaheader[18] = {0,0,2,0,0,0,0,0,0,0,0,0,w,w>>8,h,h>>8,32,0};
	if ( fwrite( tgaheader, 1, 18, f ) != 18 ) return -1;
	for ( uint32_t i=0; i<w*h; i++ ) {
			pixel.data32 = pixels[i];
			// printf("%u %u %hhu %hhu %hhu %hhu\n",i,pixel.data32,pixel.data8.blue,pixel.data8.green,pixel.data8.red,pixel.data8.alpha);
			if (putc( pixel.data8.blue, f )==EOF) return -1;
			if (putc( pixel.data8.green, f )==EOF) return -1;
			if (putc( pixel.data8.red, f )==EOF) return -1;
			if (putc( pixel.data8.alpha, f )==EOF) return -1;
	}
	return 4*w*h+18;
}

#endif // __tgawrite_h__
