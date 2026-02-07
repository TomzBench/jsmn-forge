#ifndef __SCHEMA_TOOLS_BINDINGS_H__
#define __SCHEMA_TOOLS_BINDINGS_H__
#include <stdint.h>
#include <stdbool.h>

struct vla__u32_3 {
    uint32_t len;
    uint32_t items[3];
};

struct vla__vla__u32_3_4 {
    uint32_t len;
    struct vla__u32_3 items[4];
};

struct vla__vla__vla__u32_3_4_5 {
    uint32_t len;
    struct vla__vla__u32_3_4 items[5];
};

struct vla__u32____3_4 {
    uint32_t len;
    uint32_t items[3][4];
};

struct vla__vla__u32____3_4_5 {
    uint32_t len;
    struct vla__u32____3_4 items[5];
};

struct vla__vla__u32_3____4_5 {
    uint32_t len;
    struct vla__u32_3 items[4][5];
};

struct vla__u32____4____3_5 {
    uint32_t len;
    uint32_t items[4][3][5];
};

struct thing {
    struct vla__u32_3 vla_0;
    struct vla__vla__u32_3_4 vla_1;
    struct vla__vla__vla__u32_3_4_5 vla_2;
    struct vla__vla__u32____3_4_5 vla_3;
    struct vla__vla__u32_3____4_5 vla_4;
    struct vla__u32____4____3_5 vla_5;
    struct vla__u32____3_4 vla_6[5];
    struct vla__u32_3 vla_7[5][4];
    uint32_t vla_8[5][4][3];
};

int32_t encode_thing(uint8_t *dst, uint32_t dlen, const struct thing *src);

int32_t encode_thing_array(uint8_t *dst, uint32_t dlen, const struct thing *src, uint32_t slen);

int32_t decode_thing(struct thing *dst, const uint8_t *src, uint32_t slen);

int32_t decode_thing_array(struct thing *dst, uint32_t dlen, const uint8_t *src, uint32_t slen);

uint32_t len_thing(const struct thing *val);

uint32_t array_len_thing(const struct thing *src, uint32_t slen);

enum GLOBAL_ANY_OF_KEYS {
    GLOBAL_ANY_OF_THING = 0,
};

union GLOBAL_ANY_OF {
    void *erased;
    struct thing *thing;
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
