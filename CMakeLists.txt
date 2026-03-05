cmake_minimum_required(VERSION 3.15)
project(py_lumina_core LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# ── pybind11 ─────────────────────────────────────────────────────────
find_package(pybind11 CONFIG REQUIRED)

# ── C++ core module (header-only, built into the binding target) ─────
pybind11_add_module(_core
    ${CMAKE_CURRENT_SOURCE_DIR}/src/cpp/bindings/py_lumina_bindings.cpp
)

target_include_directories(_core PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/src/cpp/include
)

target_compile_options(_core PRIVATE
    -O3 -Wall -Wextra -Wpedantic
)

# Install into the Python package directory
install(TARGETS _core DESTINATION py_lumina)