#ifndef __SCHEMA_TOOLS_BINDINGS_H__
#define __SCHEMA_TOOLS_BINDINGS_H__
#include <stdint.h>
#include <stdbool.h>

int32_t encode_boolish(uint8_t *dst, uint32_t dlen, bool src);

int32_t decode_boolish(bool *dst, const uint8_t *src, uint32_t slen);

uint32_t len_boolish(bool val);

#endif /* __SCHEMA_TOOLS_BINDINGS_H__ */
