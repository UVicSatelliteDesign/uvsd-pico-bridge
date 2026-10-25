cmake_minimum_required(VERSION 3.12)

# Pull in SDK (must be before project)
include(pico_sdk_import.cmake)

project(spi_connection C CXX ASM)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

if (PICO_SDK_VERSION_STRING VERSION_LESS "2.3.0")
    message(FATAL_ERROR "Raspberry Pi Pico SDK version 2.3.0 (or later) required. Your version is ${PICO_SDK_VERSION_STRING}")
endif()

# Initialize the SDK
pico_sdk_init()

add_executable(spi_connection
    spi_connection.c
)

pico_enable_stdio_usb(spi_connection 1)

# LINK HARDWARE_SPI HERE:
target_link_libraries(spi_connection 
    pico_stdlib
    hardware_spi
)

if (PICO_CYW43_SUPPORTED)
    target_link_libraries(spi_connection pico_cyw43_arch_none)
endif()

pico_add_extra_outputs(spi_connection)
