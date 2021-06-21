
include_directories(
  ${CMAKE_SOURCE_DIR}/config
  ${CMAKE_SOURCE_DIR}/lib/jsoncpp/include                    
  ${CMAKE_SOURCE_DIR}/lib/dynibex
  ${CMAKE_SOURCE_DIR}/lib/dynibex/arithmetic
  ${CMAKE_SOURCE_DIR}/lib/dynibex/bisector
  ${CMAKE_SOURCE_DIR}/lib/dynibex/cliquer
  ${CMAKE_SOURCE_DIR}/lib/dynibex/combinatorial
  ${CMAKE_SOURCE_DIR}/lib/dynibex/contractor
  ${CMAKE_SOURCE_DIR}/lib/dynibex/function
  ${CMAKE_SOURCE_DIR}/lib/dynibex/geometry
  ${CMAKE_SOURCE_DIR}/lib/dynibex/integrate
  ${CMAKE_SOURCE_DIR}/lib/dynibex/java
  ${CMAKE_SOURCE_DIR}/lib/dynibex/numeric
  ${CMAKE_SOURCE_DIR}/lib/dynibex/parser
  ${CMAKE_SOURCE_DIR}/lib/dynibex/predicate
  ${CMAKE_SOURCE_DIR}/lib/dynibex/set
  ${CMAKE_SOURCE_DIR}/lib/dynibex/strategy
  ${CMAKE_SOURCE_DIR}/lib/dynibex/symbolic
  ${CMAKE_SOURCE_DIR}/lib/dynibex/system
  ${CMAKE_SOURCE_DIR}/lib/dynibex/tools
)

add_executable(generator main.cpp)

target_link_libraries(
  generator
  ${CMAKE_SOURCE_DIR}/lib/dynibex/libibex.a
  prim
  ${CMAKE_SOURCE_DIR}/build/lib/libjsoncpp.so
)

# add_library(library_unit_test main.cpp)