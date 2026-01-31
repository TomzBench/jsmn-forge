#ifndef __SCHEMA_TOOLS_BINDINGS_H__
#define __SCHEMA_TOOLS_BINDINGS_H__
#include <stdint.h>
#include <stdbool.h>

int32_t encode_string(uint8_t *dst, uint32_t dlen, const uint8_t *src, uint32_t slen);

int32_t decode_string(uint8_t **dst, uint32_t *dlen, const uint8_t *src, uint32_t slen);

uint32_t len_string(const uint8_t *src, uint32_t slen);

#endif /* __SCHEMA_TOOLS_BINDINGS_H__ */
