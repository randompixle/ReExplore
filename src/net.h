#pragma once
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
  unsigned char* data;
  size_t size;
} ReBuffer;

int re_http_get(const char* url, ReBuffer* out);
void re_buffer_free(ReBuffer* b);
unsigned char* re_image_decode_rgba(const unsigned char* bytes, int len, int* out_w, int* out_h);

#ifdef __cplusplus
}
#endif
