#ifndef __SCHEMA_TOOLS_BINDINGS_H__
#define __SCHEMA_TOOLS_BINDINGS_H__
#include <stdint.h>
#include <stdbool.h>

struct object {
    uint8_t u8;
    int8_t i8;
    uint16_t u16;
    int16_t i16;
    uint32_t u32;
    int32_t i32;
    uint64_t u64;
    int64_t i64;
    bool boolish;
    uint8_t s12[12];
};

int32_t encode_object(uint8_t *dst, uint32_t dlen, const struct object *src);

int32_t encode_object_array(uint8_t *dst, uint32_t dlen, const struct object *src, uint32_t slen);

int32_t decode_object(struct object *dst, const uint8_t *src, uint32_t slen);

int32_t decode_object_array(struct object *dst, uint32_t dlen, const uint8_t *src, uint32_t slen);

uint32_t len_object(const struct object *val);

uint32_t array_len_object(const struct object *src, uint32_t slen);

struct vla__object_8 {
    uint32_t len;
    struct object items[8];
};

int32_t encode_variable_object(uint8_t *dst, uint32_t dlen, struct vla__object_8 *src);

int32_t decode_variable_object(struct vla__object_8 *dst, const uint8_t *src, uint32_t slen);

uint32_t len_variable_object(const struct vla__object_8 *src);

int32_t encode_fixed_object(uint8_t *dst, uint32_t dlen, struct object (*src)[8]);

int32_t decode_fixed_object(struct object (*dst)[8], const uint8_t *src, uint32_t slen);

uint32_t len_fixed_object(const struct object (*src)[8]);

enum GLOBAL_ANY_OF_KEYS {
    GLOBAL_ANY_OF_OBJECT = 0,
};

union GLOBAL_ANY_OF {
    void *erased;
    struct object *object;
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
