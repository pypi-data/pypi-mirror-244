cmake_minimum_required(VERSION 3.17.0)

project(nudisxs LANGUAGES C CXX Fortran)

find_package(Python REQUIRED COMPONENTS Interpreter Development.Module NumPy)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${PROJECT_SOURCE_DIR}/cmake/")
find_package(LHAPDF REQUIRED)

# F2PY headers
execute_process(
  COMMAND "${Python_EXECUTABLE}"
  -c "import numpy.f2py; print(numpy.f2py.get_include())"
  OUTPUT_VARIABLE F2PY_INCLUDE_DIR
  OUTPUT_STRIP_TRAILING_WHITESPACE
)

# Define the module name
set(NUDISXS_PY_BINDING "_nudisxs")

# Use execute_process to run Python commands directly
execute_process(
    COMMAND "${Python_EXECUTABLE}" -c "import sysconfig; print(sysconfig.get_config_var('EXT_SUFFIX'))"
    OUTPUT_VARIABLE PYTHON_EXT_SUFFIX
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

# Set the default suffix if it is not set
if(NOT PYTHON_EXT_SUFFIX)
    set(PYTHON_EXT_SUFFIX ".so")  # Default to .so for Unix-like systems
endif()

# Construct the expected file name
set(F2PY_OUTPUT_NAME "${NUDISXS_PY_BINDING}${PYTHON_EXT_SUFFIX}")

set(LIBNAME DISxs)
set(SOURCES
  nudisxs/f_sources/d2sDISCC_dxdy.f
  nudisxs/f_sources/d2sDISNC_dxdy.f
  nudisxs/f_sources/NucleonStructureFunctions.f
  nudisxs/f_sources/PhysMathConstants.f
  nudisxs/f_sources/xDIS.f
  nudisxs/f_sources/yDIS.f
  nudisxs/f_sources/DISkinematics.f
  nudisxs/f_sources/FunGeM.f
  nudisxs/f_sources/Routines.f
  nudisxs/f_sources/FQCD_L.f
  nudisxs/f_sources/F_L.f
  nudisxs/f_sources/R.f
  nudisxs/f_sources/R_Liang.f
  nudisxs/f_sources/R_WBA.f
  nudisxs/f_sources/InpOutUnits.f
  nudisxs/f_sources/BendFactor.f
  nudisxs/f_sources/Spline2.f
  nudisxs/f_sources/GeM.f
  nudisxs/f_sources/R_E143.f
  nudisxs/f_sources/SF_Liang.f
  )

add_library(${LIBNAME} SHARED ${SOURCES})
target_link_libraries(${LIBNAME} ${LHAPDF_LIBRARIES})

add_custom_command(
  OUTPUT ${F2PY_OUTPUT_NAME}
  COMMAND ${Python_EXECUTABLE}  -m numpy.f2py
    -m ${NUDISXS_PY_BINDING}
    -c
    --f90flags='-fPIC -freal-4-real-8'
    -L${CMAKE_CURRENT_BINARY_DIR}
    -lDISxs
    ${CMAKE_SOURCE_DIR}/nudisxs/f_sources/BendFactor.f
    ${CMAKE_SOURCE_DIR}/nudisxs/f_sources/d2sDISCC_dxdy.f
    ${CMAKE_SOURCE_DIR}/nudisxs/f_sources/d2sDISNC_dxdy.f
    ${CMAKE_SOURCE_DIR}/nudisxs/f_sources/DISkinematics.f
    ${CMAKE_SOURCE_DIR}/nudisxs/f_sources/F_L.f
    ${CMAKE_SOURCE_DIR}/nudisxs/f_sources/NucleonStructureFunctions.f
    ${CMAKE_SOURCE_DIR}/nudisxs/f_sources/PhysMathConstants.f
    ${CMAKE_SOURCE_DIR}/nudisxs/f_sources/R_E143.f
    ${CMAKE_SOURCE_DIR}/nudisxs/f_sources/R_Liang.f
    ${CMAKE_SOURCE_DIR}/nudisxs/f_sources/R.f
    ${CMAKE_SOURCE_DIR}/nudisxs/f_sources/SF_Liang.f
    ${CMAKE_SOURCE_DIR}/nudisxs/f_sources/xDIS.f
    ${CMAKE_SOURCE_DIR}/nudisxs/f_sources/yDIS.f
    ${LHAPDF_LIBRARIES}
    --quiet
    --lower
  DEPENDS ${LIBNAME} # Depend on the DISxs library
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
  )

add_custom_target(${NUDISXS_PY_BINDING} ALL DEPENDS "${CMAKE_CURRENT_BINARY_DIR}/${F2PY_OUTPUT_NAME}")

# Set installation path for the shared libraries
install(TARGETS ${LIBNAME} LIBRARY DESTINATION nudisxs)
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/${F2PY_OUTPUT_NAME}" DESTINATION nudisxs)
