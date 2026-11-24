@echo off
rem Runs the Gradle wrapper on JDK 25 (Stonecutter 0.10 needs it; the mods themselves compile with toolchains 17/21/25).
rem Usage: dev\gw.bat <tasks...>   e.g. dev\gw.bat :1.21.1-fabric:buildAndCollect   or   dev\gw.bat buildAndCollect
rem JDK 25: %JDK25% if set, else the Temurin 25 that Gradle provisioned in %USERPROFILE%\.gradle\jdks, else JAVA_HOME as is.
setlocal
set "SD_JDK=%USERPROFILE%\.gradle\jdks\eclipse_adoptium-25-amd64-windows.2"
if defined JDK25 set "SD_JDK=%JDK25%"
if exist "%SD_JDK%\bin\java.exe" set "JAVA_HOME=%SD_JDK%"
rem Author's machine: the Gradle home and temp files live on D: (drive C: is almost full).
set "SD_HOME=D:\minecraft mods razrab\.gradle-home"
if exist "%SD_HOME%" set "GRADLE_USER_HOME=%SD_HOME%"
if exist "%SD_HOME%" set "TMP=%SD_HOME%\tmp"
if exist "%SD_HOME%" set "TEMP=%SD_HOME%\tmp"
cd /d "%~dp0.."
call gradlew.bat %*
