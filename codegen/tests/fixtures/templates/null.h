#ifndef __SCHEMA_TOOLS_BINDINGS_H__
#define __SCHEMA_TOOLS_BINDINGS_H__
#include <stdint.h>
#include <stdbool.h>

int32_t encode_nullish(uint8_t *dst, uint32_t dlen);

int32_t decode_nullish(const uint8_t *src, uint32_t slen);

uint32_t len_nullish(void);

#endif /* __SCHEMA_TOOLS_BINDINGS_H__ */
