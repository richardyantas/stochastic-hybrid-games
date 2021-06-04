set(CMAKE_CXX_STANDARD 11)
include_directories(${SAFE_INCLUDE_DIRECTORIES})
#add_subdirectory(catch2)
#add_executable(Test ${SAFE_SOURCE_DIR}/src/main.cpp)
target_link_libraries(Test
                      library_unit_test
                      ${PROJECT_SOURCE_DIR}/lib/dynibex/libibex.a
                      prim
                      ${PROJECT_SOURCE_DIR}/build/lib/libjsoncpp.so
                      Catch2::Test
                      )        
add_test(test_all Test)
