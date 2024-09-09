@echo off
rem turn off echo

rem set TouchDesigner build numbers
set TOUCHVERSION=2023.11880

rem set our project file target
set TOEFILE="dev-env.toe"

rem set the rest of our paths for executables
set TOUCHDIR=%PROGRAMFILES%\Derivative\TouchDesigner.
set TOUCHEXE=\bin\TouchDesigner.exe

rem set dev flag to true
set DEV=TRUE
set BLENDMONITORDATA=%~dp0_public

rem combine our elements so we have a single path to our TouchDesigner.exe 
set TOUCHPATH="%TOUCHDIR%%TOUCHVERSION%%TOUCHEXE%"


if exist %TOUCHPATH% goto :STARTPROJECT

echo Touch Version: %TOUCHVERSION% is not installed.

CHOICE /M "Download"
if %errorlevel% equ 1 goto :DOWNLOAD
if %errorlevel% equ 2 goto :eof
	

:DOWNLOAD
echo Downloading...
rem download version that isn't installed.
start "" https://download.derivative.ca/TouchDesigner.%TOUCHVERSION%.exe
goto :eof


:STARTPROJECT
rem start our project file with the target TD installation
start "" %TOUCHPATH% %TOEFILE%

