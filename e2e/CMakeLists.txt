cmake_minimum_required(VERSION 3.14)
project(jsmn-forge-e2e LANGUAGES C)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/../cmake/modules")
find_package(Unity REQUIRED)

enable_testing()

add_executable(test_foo test_foo.c)
target_link_libraries(test_foo PRIVATE unity::framework)
add_test(NAME test_foo COMMAND test_foo)
