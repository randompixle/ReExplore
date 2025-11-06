#ifndef STB_TRUETYPE_H
#define STB_TRUETYPE_H
#ifdef __cplusplus
extern "C" {
#endif
typedef unsigned char stbtt_uint8;
typedef int stbtt_int32;
typedef struct stbtt_fontinfo stbtt_fontinfo;
int  stbtt_InitFont(stbtt_fontinfo *info, const unsigned char *data, int offset);
float stbtt_ScaleForPixelHeight(const stbtt_fontinfo *info, float pixels);
void stbtt_GetFontVMetrics(const stbtt_fontinfo *info, int *ascent, int *descent, int *lineGap);
void stbtt_GetCodepointHMetrics(const stbtt_fontinfo *info, int codepoint, int *advanceWidth, int *leftSideBearing);
unsigned char *stbtt_GetCodepointBitmapSubpixel(const stbtt_fontinfo *info, float scale_x, float scale_y,
                            float shift_x, float shift_y, int codepoint, int *width, int *height, int *xoff, int *yoff);
void stbtt_FreeBitmap(unsigned char *bitmap, void *userdata);
#ifdef __cplusplus
}
#endif
#endif
