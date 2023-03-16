# #cmake_minimum_required(VERSION 3.10)
# cmake_minimum_required(VERSION 3.20.3)
# #set(CMAKE_CXX_STANDARD 14)
# set(CMAKE_CXX_STANDARD 17)
# set(CMAKE_CXX_FLAGS "-g -fno-omit-frame-pointer -Wall")
# project (ucsp-solar)
# add_subdirectory(lib/jsoncpp/)
# add_subdirectory(lib/config/)
# add_subdirectory(sources/patterns/)


# Corregir los test 
# Corregir el pattern file and refactorize§

cmake_minimum_required(VERSION 3.20.3)
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_FLAGS "-g -fno-omit-frame-pointer -Wall")
# set(SAFE_INCLUDE_DIRECTORIES)
# add_subdirectory(src)

# include_directories()

add_executable(main main.cpp)

target_link_libraries(
  main
  ${CMAKE_SOURCE_DIR}/lib/dynibex/libibex.a
  prim
  ${CMAKE_SOURCE_DIR}/build/lib/libjsoncpp.so
)

enable_testing()

set(TEST_CASES  
  car_test
)

foreach(_test_case ${TEST_CASES})
  add_executable(${_test_case} ${_test_case}.cpp)
  target_link_libraries(
    ${_test_case}
    #${CMAKE_SOURCE_DIR}/build/lib/dynibex/libibex.a
    #prim
    #${CMAKE_SOURCE_DIR}/build/lib/libjsoncpp.so
  )
endforeach()

add_test(car car_test)
# enable_testing()
# add_subdirectory(test)