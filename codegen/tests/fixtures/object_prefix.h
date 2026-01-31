#ifndef __SCHEMA_TOOLS_BINDINGS_H__
#define __SCHEMA_TOOLS_BINDINGS_H__
#include <stdint.h>
#include <stdbool.h>

struct fooey_thing_nested {
    int32_t foo;
};

int32_t fooey_encode_thing_nested(uint8_t *dst, uint32_t dlen, const struct fooey_thing_nested *src);

int32_t fooey_encode_thing_nested_array(uint8_t *dst, uint32_t dlen, const struct fooey_thing_nested *src, uint32_t slen);

int32_t fooey_decode_thing_nested(struct fooey_thing_nested *dst, const uint8_t *src, uint32_t slen);

int32_t fooey_decode_thing_nested_array(struct fooey_thing_nested *dst, uint32_t dlen, const uint8_t *src, uint32_t slen);

uint32_t fooey_len_thing_nested(const struct fooey_thing_nested *val);

uint32_t fooey_array_len_thing_nested(const struct fooey_thing_nested *src, uint32_t slen);

struct fooey_thing_a_1 {
    int64_t foo;
};

int32_t fooey_encode_thing_a_1(uint8_t *dst, uint32_t dlen, const struct fooey_thing_a_1 *src);

int32_t fooey_encode_thing_a_1_array(uint8_t *dst, uint32_t dlen, const struct fooey_thing_a_1 *src, uint32_t slen);

int32_t fooey_decode_thing_a_1(struct fooey_thing_a_1 *dst, const uint8_t *src, uint32_t slen);

int32_t fooey_decode_thing_a_1_array(struct fooey_thing_a_1 *dst, uint32_t dlen, const uint8_t *src, uint32_t slen);

uint32_t fooey_len_thing_a_1(const struct fooey_thing_a_1 *val);

uint32_t fooey_array_len_thing_a_1(const struct fooey_thing_a_1 *src, uint32_t slen);

struct fooey_thing {
    uint8_t u8;
    int8_t i8;
    uint16_t u16;
    int16_t i16;
    uint32_t u32;
    int32_t i32;
    uint64_t u64;
    int64_t i64;
    bool bool;
    uint8_t s32[32];
    uint32_t many_numbers[5];
    struct fooey_thing_nested nested;
    uint8_t multi_string[3][4][9];
    struct fooey_thing_a_1 a_1[3];
};

int32_t fooey_encode_thing(uint8_t *dst, uint32_t dlen, const struct fooey_thing *src);

int32_t fooey_encode_thing_array(uint8_t *dst, uint32_t dlen, const struct fooey_thing *src, uint32_t slen);

int32_t fooey_decode_thing(struct fooey_thing *dst, const uint8_t *src, uint32_t slen);

int32_t fooey_decode_thing_array(struct fooey_thing *dst, uint32_t dlen, const uint8_t *src, uint32_t slen);

uint32_t fooey_len_thing(const struct fooey_thing *val);

uint32_t fooey_array_len_thing(const struct fooey_thing *src, uint32_t slen);

enum GLOBAL_ANY_OF_KEYS {
    GLOBAL_ANY_OF_FOOEY_THING = 0,
    GLOBAL_ANY_OF_FOOEY_THING_NESTED = 1,
    GLOBAL_ANY_OF_FOOEY_THING_A_1 = 2,
};

union GLOBAL_ANY_OF {
    void *erased;
    struct fooey_thing *fooey_thing;
    struct fooey_thing_nested *fooey_thing_nested;
    struct fooey_thing_a_1 *fooey_thing_a_1;
};

struct GLOBAL_ANY_OF_WITH_KEY {
    enum GLOBAL_ANY_OF_KEYS key;
    union GLOBAL_ANY_OF value;
};

struct GLOBAL_ANY_OF_WITH_KEY_LEN {
    enum GLOBAL_ANY_OF_KEYS key;
    union GLOBAL_ANY_OF value;
    uint32_t len;
};

int32_t vtable_generic_encode(uint8_t *dst, uint32_t dlen, struct GLOBAL_ANY_OF_WITH_KEY *ctx);

int32_t vtable_generic_decode(struct GLOBAL_ANY_OF_WITH_KEY *ctx, const uint8_t *src, uint32_t slen);

uint32_t vtable_generic_len(struct GLOBAL_ANY_OF_WITH_KEY *ctx);

int32_t vtable_array_encode(uint8_t *dst, uint32_t dlen, struct GLOBAL_ANY_OF_WITH_KEY_LEN *ctx);

int32_t vtable_array_decode(struct GLOBAL_ANY_OF_WITH_KEY_LEN *ctx, const uint8_t *src, uint32_t slen);

uint32_t vtable_array_len(struct GLOBAL_ANY_OF_WITH_KEY_LEN *ctx);

#endif /* __SCHEMA_TOOLS_BINDINGS_H__ */
