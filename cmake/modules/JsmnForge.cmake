# JsmnForge.cmake
#
# TODO: Implement jsmn_forge_generate() CMake function.
#
# This module will provide a CMake function that wraps jsmn-forge codegen
# as a custom command, re-running generation when spec files change.
#
# Distribution pattern (sourced from pybind11 / nanobind):
#   Ship this .cmake file as package data inside the Python distribution.
#   Expose the install path via a CLI flag:
#
#     $ jsmn-forge-codegen --cmake-dir
#     /path/to/site-packages/jsmn_forge/cmake
#
#   Python implementation (importlib.resources):
#     from importlib.resources import files
#     print(files("jsmn_forge").joinpath("cmake"))
#
# Consumer CMakeLists.txt usage:
#
#   execute_process(
#       COMMAND jsmn-forge-codegen --cmake-dir
#       OUTPUT_VARIABLE JSMN_FORGE_CMAKE_DIR
#       OUTPUT_STRIP_TRAILING_WHITESPACE
#   )
#   list(APPEND CMAKE_MODULE_PATH ${JSMN_FORGE_CMAKE_DIR})
#   include(JsmnForge)
#
#   jsmn_forge_generate(
#       SPEC ${CMAKE_CURRENT_SOURCE_DIR}/api.yaml
#       HEADERS_DIR ${CMAKE_CURRENT_SOURCE_DIR}/include
#       SOURCES_DIR ${CMAKE_CURRENT_SOURCE_DIR}/src
#   )
