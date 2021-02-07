# g++ -frounding-math -ffloat-store -I/usr/local/include -I/usr/local/include/ibex  -O3 -DNDEBUG -Wno-deprecated -frounding-math  -o 4_rooms 4_rooms.cpp -L/usr/local/lib -libex -lprim -lClp -lCoinUtils
# To install folder ibex on home and dynbex 

#cmake_minimum_required(VERSION 3.5)
set(CMAKE_CXX_STANDARD 11)
#set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
#project(safesystems)

#-I/usr/local/include/ibex
# g++  -I/usr/local/include/ibex  -o main main.cpp -libex -lprim

#set(PYTHON_LIBRARIES "\\usr\\lib\\python2.7")
#set(PYTHON_INCLUDE_DIRS "\\usr\\include\\python2.7")

#find_package(PythonLibs 2.7 REQUIRED)
#target_include_directories(test PRIVATE ${PYTHON_INCLUDE_DIRS})

if(UNIX)
    message("This is a ${CMAKE_SYSTEM_NAME} system")
elseif(WIN32)
    message("This is a Windows Systems")
endif()

# https://github.com/ibex-team/ibex-lib   try this then ! 

# include_directories(/usr/local/include/ibex ${PROJECT_SOURCE_DIR}/lib/jsoncpp/include)

# include_directories(${PROJECT_SOURCE_DIR}/lib/ibex/dynibex-2.01/src/  ${PROJECT_SOURCE_DIR}/lib/jsoncpp/include)
include_directories(${PROJECT_SOURCE_DIR}/config
                    ${PROJECT_SOURCE_DIR}/lib/jsoncpp/include
                    
                    ${PROJECT_SOURCE_DIR}/lib/dynibex
                    ${PROJECT_SOURCE_DIR}/lib/dynibex/arithmetic
                    ${PROJECT_SOURCE_DIR}/lib/dynibex/bisector
                    ${PROJECT_SOURCE_DIR}/lib/dynibex/cliquer
                    ${PROJECT_SOURCE_DIR}/lib/dynibex/combinatorial
                    ${PROJECT_SOURCE_DIR}/lib/dynibex/contractor
                    ${PROJECT_SOURCE_DIR}/lib/dynibex/function
                    ${PROJECT_SOURCE_DIR}/lib/dynibex/geometry
                    ${PROJECT_SOURCE_DIR}/lib/dynibex/integrate
                    ${PROJECT_SOURCE_DIR}/lib/dynibex/java
                    ${PROJECT_SOURCE_DIR}/lib/dynibex/numeric
                    ${PROJECT_SOURCE_DIR}/lib/dynibex/parser
                    ${PROJECT_SOURCE_DIR}/lib/dynibex/predicate
                    ${PROJECT_SOURCE_DIR}/lib/dynibex/set
                    ${PROJECT_SOURCE_DIR}/lib/dynibex/strategy
                    ${PROJECT_SOURCE_DIR}/lib/dynibex/symbolic
                    ${PROJECT_SOURCE_DIR}/lib/dynibex/system
                    ${PROJECT_SOURCE_DIR}/lib/dynibex/tools
                    )


#include_directories(/usr/local/dynibex-2.01/include/ibex)
#set(HEADERS Matplotlibcpp.h )

set(SOURCES pattern_generator.cpp)

add_executable(pattern_generator
               ${HEADERS} 
               ${SOURCES})
# target_include_directories(pattern_generator PRIVATE ${PYTHON_INCLUDE_DIRS})
target_link_libraries(pattern_generator
                      #ibex
                      prim
                      #${PYTHON_LIBRARIES} 
                      ${PROJECT_SOURCE_DIR}/lib/dynibex/libibex.a
                      ${PROJECT_SOURCE_DIR}/build/lib/libjsoncpp.so)