#ifndef __SCHEMA_TOOLS_BINDINGS_H__
#define __SCHEMA_TOOLS_BINDINGS_H__
#include <stdint.h>
#include <stdbool.h>

struct thing_nested {
    int32_t foo;
};

int32_t encode_thing_nested(uint8_t *dst, uint32_t dlen, const struct thing_nested *src);

int32_t encode_thing_nested_array(uint8_t *dst, uint32_t dlen, const struct thing_nested *src, uint32_t slen);

int32_t decode_thing_nested(struct thing_nested *dst, const uint8_t *src, uint32_t slen);

int32_t decode_thing_nested_array(struct thing_nested *dst, uint32_t dlen, const uint8_t *src, uint32_t slen);

uint32_t len_thing_nested(const struct thing_nested *val);

uint32_t array_len_thing_nested(const struct thing_nested *src, uint32_t slen);

struct thing_a_1 {
    int64_t foo;
};

int32_t encode_thing_a_1(uint8_t *dst, uint32_t dlen, const struct thing_a_1 *src);

int32_t encode_thing_a_1_array(uint8_t *dst, uint32_t dlen, const struct thing_a_1 *src, uint32_t slen);

int32_t decode_thing_a_1(struct thing_a_1 *dst, const uint8_t *src, uint32_t slen);

int32_t decode_thing_a_1_array(struct thing_a_1 *dst, uint32_t dlen, const uint8_t *src, uint32_t slen);

uint32_t len_thing_a_1(const struct thing_a_1 *val);

uint32_t array_len_thing_a_1(const struct thing_a_1 *src, uint32_t slen);

struct thing {
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
    struct thing_nested nested;
    uint8_t multi_string[3][4][9];
    struct thing_a_1 a_1[3];
};

int32_t encode_thing(uint8_t *dst, uint32_t dlen, const struct thing *src);

int32_t encode_thing_array(uint8_t *dst, uint32_t dlen, const struct thing *src, uint32_t slen);

int32_t decode_thing(struct thing *dst, const uint8_t *src, uint32_t slen);

int32_t decode_thing_array(struct thing *dst, uint32_t dlen, const uint8_t *src, uint32_t slen);

uint32_t len_thing(const struct thing *val);

uint32_t array_len_thing(const struct thing *src, uint32_t slen);

enum GLOBAL_ANY_OF_KEYS {
    GLOBAL_ANY_OF_THING = 0,
    GLOBAL_ANY_OF_THING_NESTED = 1,
    GLOBAL_ANY_OF_THING_A_1 = 2,
};

union GLOBAL_ANY_OF {
    void *erased;
    struct thing *thing;
    struct thing_nested *thing_nested;
    struct thing_a_1 *thing_a_1;
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
