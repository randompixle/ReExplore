#define STB_TRUETYPE_IMPLEMENTATION
#include "../third_party/stb_truetype.h"

#include "font.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
  stbtt_fontinfo info;
  unsigned char* data;
} TTState;

int font_load(ReFont* f, const char* ttf_path, int pixel_size) {
  memset(f, 0, sizeof(*f));

  FILE* fp = fopen(ttf_path, "rb");
  if (!fp) return -1;

  fseek(fp, 0, SEEK_END);
  long sz = ftell(fp);
  fseek(fp, 0, SEEK_SET);

  unsigned char* buf = malloc(sz);
  if (!buf) { fclose(fp); return -2; }

  fread(buf, 1, sz, fp);
  fclose(fp);

  TTState* st = calloc(1, sizeof(TTState));
  if (!st) { free(buf); return -3; }

  st->data = buf;
  if (!stbtt_InitFont(&st->info, st->data, 0)) {
    free(st->data);
    free(st);
    return -4;
  }

  f->tt_data = st;
  f->pixel_size = pixel_size;
  f->tt_size = (int)sz;
  f->scale = stbtt_ScaleForPixelHeight(&st->info, pixel_size);

  stbtt_GetFontVMetrics(&st->info, &f->ascent, &f->descent, &f->line_gap);

  f->loaded = 1;
  return 0;
}

void font_free(ReFont* f) {
  if (!f || !f->loaded) return;
  TTState* st = (TTState*)f->tt_data;
  if (st) {
    free(st->data);
    free(st);
  }
  memset(f, 0, sizeof(*f));
}
