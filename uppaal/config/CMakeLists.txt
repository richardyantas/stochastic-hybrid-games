# cmake_minimum_required(VERSION 3.20.3)
cmake_minimum_required(VERSION 3.18.4)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS "-g -fno-omit-frame-pointer -Wall")
project (uppaal)
find_package(PkgConfig REQUIRED)
pkg_check_modules(JSONCPP jsoncpp)
include_directories(${PROJECT_SOURCE_DIR}/config)
add_library(config SHARED config.cpp config_wrapper_swh.cpp)
target_link_libraries(config PUBLIC ${JSONCPP_LIBRARIES})
install(TARGETS config DESTINATION bin)

# -I/usr/include/jsoncpp  -L/usr/lib/x86_64-linux-gnu/     libjsoncpp.so