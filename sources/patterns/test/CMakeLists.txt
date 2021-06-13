cmake_minimum_required(VERSION 3.20.3)
set(CMAKE_CXX_STANDARD 11)

include_directories(
  ${CMAKE_CURRENT_SOURCE_DIR}
  #${SAFE_INCLUDE_DIRECTORIES}
  ${CMAKE_SOURCE_DIR}/lib/jsoncpp/include/
)

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
# add_test(safe ${EXECUTABLE_OUTPUT_PATH}/safe_test)