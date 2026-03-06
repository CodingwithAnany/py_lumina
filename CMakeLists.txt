cmake_minimum_required(VERSION 3.15)
project(pylumina LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(pybind11 REQUIRED)

# ── Extension module ────────────────────────────────────────────────

pybind11_add_module(_core
    cpp/bindings/pybind_module.cpp
    cpp/engine/physics_engine.cpp
    cpp/engine/integrator.cpp
    cpp/forces/gravity.cpp
    cpp/forces/wind.cpp
    cpp/forces/drag.cpp
    cpp/collision/collision.cpp
)

target_include_directories(_core PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/cpp/engine
    ${CMAKE_CURRENT_SOURCE_DIR}/cpp/forces
    ${CMAKE_CURRENT_SOURCE_DIR}/cpp/collision
)

# Install into the Python package directory
install(TARGETS _core DESTINATION pylumina)