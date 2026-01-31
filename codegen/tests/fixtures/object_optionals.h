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

union maybe__u8 {
    uint8_t value;
};

struct optional__u8 {
    bool present;
    union maybe__u8 maybe;
};

union maybe__i8 {
    int8_t value;
};

struct optional__i8 {
    bool present;
    union maybe__i8 maybe;
};

union maybe__u16 {
    uint16_t value;
};

struct optional__u16 {
    bool present;
    union maybe__u16 maybe;
};

union maybe__i16 {
    int16_t value;
};

struct optional__i16 {
    bool present;
    union maybe__i16 maybe;
};

union maybe__u32 {
    uint32_t value;
};

struct optional__u32 {
    bool present;
    union maybe__u32 maybe;
};

union maybe__i32 {
    int32_t value;
};

struct optional__i32 {
    bool present;
    union maybe__i32 maybe;
};

union maybe__u64 {
    uint64_t value;
};

struct optional__u64 {
    bool present;
    union maybe__u64 maybe;
};

union maybe__i64 {
    int64_t value;
};

struct optional__i64 {
    bool present;
    union maybe__i64 maybe;
};

union maybe__bool {
    bool value;
};

struct optional__bool {
    bool present;
    union maybe__bool maybe;
};

union maybe__u8____32 {
    uint8_t value[32];
};

struct optional__u8____32 {
    bool present;
    union maybe__u8____32 maybe;
};

union maybe__u32____5 {
    uint32_t value[5];
};

struct optional__u32____5 {
    bool present;
    union maybe__u32____5 maybe;
};

union maybe__thing_nested {
    struct thing_nested value;
};

struct optional__thing_nested {
    bool present;
    union maybe__thing_nested maybe;
};

union maybe__u8____3____4____9 {
    uint8_t value[3][4][9];
};

struct optional__u8____3____4____9 {
    bool present;
    union maybe__u8____3____4____9 maybe;
};

struct thing {
    struct optional__u8 u8;
    struct optional__i8 i8;
    struct optional__u16 u16;
    struct optional__i16 i16;
    struct optional__u32 u32;
    struct optional__i32 i32;
    struct optional__u64 u64;
    struct optional__i64 i64;
    struct optional__bool bool;
    struct optional__u8____32 s32;
    struct optional__u32____5 many_numbers;
    struct optional__thing_nested nested;
    struct optional__u8____3____4____9 multi_string;
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
};

union GLOBAL_ANY_OF {
    void *erased;
    struct thing *thing;
    struct thing_nested *thing_nested;
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
