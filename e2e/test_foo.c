#include "unity.h"

void setUp(void) {}
void tearDown(void) {}

void test_basic_int_assert(void) {
    TEST_ASSERT_EQUAL_INT(42, 42);
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_basic_int_assert);
    return UNITY_END();
}
