include_directories(${PROJECT_SOURCE_DIR}/config)

#file(GLOB SOURCES "*.cpp")
#add_library(config SHARED ${SOURCES})
add_library(config SHARED config.cpp config_wrapper.cpp)
# link_libraries(stdc++fs)
target_link_libraries(config PUBLIC ${PROJECT_SOURCE_DIR}/build/lib/libjsoncpp.so stdc++fs)
install(TARGETS config DESTINATION bin)

# Here
add_library(mylib SHARED mylib.cpp)
# https://stackoverflow.com/questions/17511496/how-to-create-a-shared-library-with-cmake
#find_library(jsoncpp_location libjsoncpp)
#target_link_libraries(mylib PUBLIC ${PROJECT_SOURCE_DIR}/build/lib/libjsoncpp.so)
target_link_libraries(mylib PUBLIC ${PROJECT_SOURCE_DIR}/build/lib/libjsoncpp.so)
#set_property(TARGET mylib PROPERTY IMPORTED_LOCATION ${PROJECT_SOURCE_DIR}/build/lib/libjsoncpp.so)
install(TARGETS mylib DESTINATION bin )
