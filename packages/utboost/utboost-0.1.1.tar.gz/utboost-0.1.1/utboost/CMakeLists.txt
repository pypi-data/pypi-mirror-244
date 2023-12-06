cmake_minimum_required(VERSION 3.0)

project(utboost)

option(USE_OPENMP "Enable OpenMP" ON)
option(BUILD_TEST "Build C++ tests with Google Test" OFF)
option(USE_DEBUG "Set to ON for Debug mode" OFF)

if(UNIX OR MINGW OR CYGWIN)
    SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread -Wall -std=c++11 -w")
endif()

if (USE_DEBUG)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O0 -g")
else()
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3")
endif()

if(USE_OPENMP)
    message(STATUS "OpenMP is enabled")
    find_package(OpenMP REQUIRED)
    SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
else()
    # Ignore unknown #pragma warning
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-unknown-pragmas")
endif(USE_OPENMP)

if(WIN32 AND MINGW)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -static-libstdc++")
endif()

set(CMAKE_INSTALL_PREFIX ${PROJECT_SOURCE_DIR})

set(UTBOOST_INCLUDE_DIR ${PROJECT_SOURCE_DIR}/include)
set(UTBOOST_INSTALL_LIB_DIR ${PROJECT_SOURCE_DIR}/lib)

include_directories(${UTBOOST_INCLUDE_DIR})

file(GLOB SOURCES
    src/io/*.cpp
    src/ensemble/*.cpp
    src/learner/*.cpp
    src/metric/*.cpp
    src/split_criteria/*.cpp
    src/objective/*.cpp
)

add_library(_${PROJECT_NAME} SHARED ${SOURCES} src/c_api.cpp)

if(BUILD_TEST)
    message(STATUS "Building C++ tests with GoogleTest")
    add_subdirectory(test/lib/googletest)
    include_directories(${gtest_SOURCE_DIR}/include ${gtest_SOURCE_DIR})
    file(GLOB CPP_TEST_SOURCES test/*.cpp)
    add_executable(Google_Tests_run ${CPP_TEST_SOURCES})
    target_link_libraries(Google_Tests_run _${PROJECT_NAME} gtest gtest_main)
endif()

install(TARGETS _${PROJECT_NAME} DESTINATION ${UTBOOST_INSTALL_LIB_DIR})
