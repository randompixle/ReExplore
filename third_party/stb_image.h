#ifndef STB_IMAGE_MINI_H
#define STB_IMAGE_MINI_H
#ifdef __cplusplus
extern "C" {
#endif
unsigned char *stbi_load_from_memory(const unsigned char *buffer, int len, int *x, int *y, int *channels_in_file, int desired_channels);
void stbi_image_free(void *retval_from_stbi_load);
#ifdef __cplusplus
}
#endif
#endif
