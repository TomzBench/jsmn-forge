#ifndef __SCHEMA_TOOLS_BINDINGS_H__
#define __SCHEMA_TOOLS_BINDINGS_H__
#include <stdint.h>
#include <stdbool.h>

int32_t encode_u8(uint8_t *dst, uint32_t dlen, uint8_t src);

int32_t decode_u8(uint8_t *dst, const uint8_t *src, uint32_t slen);

uint32_t len_u8(uint8_t val);

int32_t encode_i8(uint8_t *dst, uint32_t dlen, int8_t src);

int32_t decode_i8(int8_t *dst, const uint8_t *src, uint32_t slen);

uint32_t len_i8(int8_t val);

int32_t encode_u16(uint8_t *dst, uint32_t dlen, uint16_t src);

int32_t decode_u16(uint16_t *dst, const uint8_t *src, uint32_t slen);

uint32_t len_u16(uint16_t val);

int32_t encode_i16(uint8_t *dst, uint32_t dlen, int16_t src);

int32_t decode_i16(int16_t *dst, const uint8_t *src, uint32_t slen);

uint32_t len_i16(int16_t val);

int32_t encode_u32(uint8_t *dst, uint32_t dlen, uint32_t src);

int32_t decode_u32(uint32_t *dst, const uint8_t *src, uint32_t slen);

uint32_t len_u32(uint32_t val);

int32_t encode_i32(uint8_t *dst, uint32_t dlen, int32_t src);

int32_t decode_i32(int32_t *dst, const uint8_t *src, uint32_t slen);

uint32_t len_i32(int32_t val);

int32_t encode_u64(uint8_t *dst, uint32_t dlen, uint64_t src);

int32_t decode_u64(uint64_t *dst, const uint8_t *src, uint32_t slen);

uint32_t len_u64(uint64_t val);

int32_t encode_i64(uint8_t *dst, uint32_t dlen, int64_t src);

int32_t decode_i64(int64_t *dst, const uint8_t *src, uint32_t slen);

uint32_t len_i64(int64_t val);

#endif /* __SCHEMA_TOOLS_BINDINGS_H__ */
