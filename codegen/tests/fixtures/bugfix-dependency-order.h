#ifndef __SCHEMA_TOOLS_BINDINGS_H__
#define __SCHEMA_TOOLS_BINDINGS_H__
#include <stdint.h>
#include <stdbool.h>

struct boom {
    uint32_t a;
};

int32_t encode_boom(uint8_t *dst, uint32_t dlen, const struct boom *src);

int32_t encode_boom_array(uint8_t *dst, uint32_t dlen, const struct boom *src, uint32_t slen);

int32_t decode_boom(struct boom *dst, const uint8_t *src, uint32_t slen);

int32_t decode_boom_array(struct boom *dst, uint32_t dlen, const uint8_t *src, uint32_t slen);

uint32_t len_boom(const struct boom *val);

uint32_t array_len_boom(const struct boom *src, uint32_t slen);

struct thing {
    struct boom inner;
};

int32_t encode_thing(uint8_t *dst, uint32_t dlen, const struct thing *src);

int32_t encode_thing_array(uint8_t *dst, uint32_t dlen, const struct thing *src, uint32_t slen);

int32_t decode_thing(struct thing *dst, const uint8_t *src, uint32_t slen);

int32_t decode_thing_array(struct thing *dst, uint32_t dlen, const uint8_t *src, uint32_t slen);

uint32_t len_thing(const struct thing *val);

uint32_t array_len_thing(const struct thing *src, uint32_t slen);

enum GLOBAL_ANY_OF_KEYS {
    GLOBAL_ANY_OF_THING = 0,
    GLOBAL_ANY_OF_BOOM = 1,
};

union GLOBAL_ANY_OF {
    void *erased;
    struct thing *thing;
    struct boom *boom;
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
