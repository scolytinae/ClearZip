@echo off

set PYTHON_EXE=C:\Python27\python.exe
set DEFAULT_PROJ_DIR=.\dfPostXE
set DEFAULT_TRASH_FILE=.\xeTrash.lst
set DEFAULT_SCRIPT=.\clearzip.py

rem To use celarzip.exe
rem set DEFAULT_SCRIPT=.\dist\clearzip.exe
rem set PYTHON_EXE=

if not exist %DEFAULT_SCRIPT% (
  echo %DEFAULT_SCRIPT% doesnt exist! Edit this bat file. Insert correct script path
  exit \b 1
)

set PROJ_DIR=%1
if not exist "%PROJ_DIR%" (
  set PROJ_DIR=%DEFAULT_PROJ_DIR%
)

set TRASH_FILE=%2
if not exist "%TRASH_FILE%" (
  set TRASH_FILE=%DEFAULT_TRASH_FILE%
)

%PYTHON_EXE% %DEFAULT_SCRIPT% -t %TRASH_FILE% -m zip %PROJ_DIR%
