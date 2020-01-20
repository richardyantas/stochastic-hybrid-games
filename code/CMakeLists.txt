# g++ -frounding-math -ffloat-store -I/usr/local/include -I/usr/local/include/ibex  -O3 -DNDEBUG -Wno-deprecated -frounding-math  -o 4_rooms 4_rooms.cpp -L/usr/local/lib -libex -lprim -lClp -lCoinUtils
# To install folder ibex on home and dynbex 

cmake_minimum_required(VERSION 3.5)
set(CMAKE_CXX_STANDARD 11)
#set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
project(safesystems)

#-I/usr/local/include/ibex
# g++  -I/usr/local/include/ibex  -o main main.cpp -libex -lprim

set(PYTHON_LIBRARIES "\\usr\\lib\\python2.7")
set(PYTHON_INCLUDE_DIRS "\\usr\\include\\python2.7")

find_package(PythonLibs 2.7 REQUIRED)
#target_include_directories(test PRIVATE ${PYTHON_INCLUDE_DIRS})

if(UNIX)
    message("This is a ${CMAKE_SYSTEM_NAME} system")
elseif(WIN32)
    message("This is a Windows Systems")
endif()

include_directories(/usr/local/include/ibex)
#include_directories(/usr/local/dynibex-2.01/include/ibex)

set(HEADERS Matplotlibcpp.h )
set(SOURCES main.cpp)
add_executable(out ${HEADERS} ${SOURCES})

target_include_directories(out PRIVATE ${PYTHON_INCLUDE_DIRS})
target_link_libraries(out ibex prim ${PYTHON_LIBRARIES})