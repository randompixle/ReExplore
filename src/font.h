#pragma once

typedef struct {
  void* tt_data;
  int pixel_size;
  int tt_size;
  float scale;
  int ascent;
  int descent;
  int line_gap;
  int loaded;
} ReFont;

int font_load(ReFont* f, const char* ttf_path, int pixel_size);
void font_free(ReFont* f);
