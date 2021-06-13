cmake_minimum_required(VERSION 3.20.3)
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_FLAGS "-g -fno-omit-frame-pointer -Wall")
set(SAFE_INCLUDE_DIRECTORIES
    "${CMAKE_SOURCE_DIR}/lib/dynibex/"
    "${CMAKE_SOURCE_DIR}/lib/dynibex/arithmetic"
    "${CMAKE_SOURCE_DIR}/lib/dynibex/bisector"
    "${CMAKE_SOURCE_DIR}/lib/dynibex/cliquer"
    "${CMAKE_SOURCE_DIR}/lib/dynibex/combinatorial"
    "${CMAKE_SOURCE_DIR}/lib/dynibex/contractor"
    "${CMAKE_SOURCE_DIR}/lib/dynibex/function"
    "${CMAKE_SOURCE_DIR}/lib/dynibex/geometry"
    "${CMAKE_SOURCE_DIR}/lib/dynibex/integrate"
    "${CMAKE_SOURCE_DIR}/lib/dynibex/numeric"
    "${CMAKE_SOURCE_DIR}/lib/dynibex/parser"
    "${CMAKE_SOURCE_DIR}/lib/dynibex/predicate"
    "${CMAKE_SOURCE_DIR}/lib/dynibex/set"
    "${CMAKE_SOURCE_DIR}/lib/dynibex/strategy"
    "${CMAKE_SOURCE_DIR}/lib/dynibex/symbolic"
    "${CMAKE_SOURCE_DIR}/lib/dynibex/system"
    "${CMAKE_SOURCE_DIR}/lib/dynibex/tools"
)

add_subdirectory(src)

enable_testing()
add_subdirectory(test)