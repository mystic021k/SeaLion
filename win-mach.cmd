@echo off
setlocal EnableExtensions EnableDelayedExpansion

rem Source tree follows this script, so a checkout in another directory still works.
set "ROOT=%~dp0"
if "%ROOT:~-1%"=="\" set "ROOT=%ROOT:~0,-1%"

rem MozillaBuild: /mozillabuild <dir> wins, then MOZILLABUILD, then the usual install path.
if defined MOZILLABUILD (
  set "MB=%MOZILLABUILD%"
) else (
  set "MB=C:\mozilla-build"
)

set "MACH_CMD="
:parse_args
if "%~1"=="" goto args_done
if /I "%~1"=="/?" goto usage
if /I "%~1"=="-h" goto usage
if /I "%~1"=="--help" goto usage
if /I "%~1"=="/mozillabuild" goto take_mb
if /I "%~1"=="--mozillabuild" goto take_mb
if defined MACH_CMD (
  set "MACH_CMD=!MACH_CMD! %1"
) else (
  set "MACH_CMD=%1"
)
shift
goto parse_args

:take_mb
if "%~2"=="" (
  echo Missing directory after %~1
  exit /b 1
)
set "MB=%~2"
shift
shift
goto parse_args

:args_done
if not defined MACH_CMD goto usage

if "%MB:~-1%"=="\" set "MB=%MB:~0,-1%"
if not exist "%MB%\msys\bin\bash.exe" (
  echo MozillaBuild not found: "%MB%"
  echo Set MOZILLABUILD, or pass /mozillabuild ^<directory^>.
  exit /b 1
)
if not exist "%ROOT%\mach" (
  echo SeaLion tree not found: "%ROOT%"
  exit /b 1
)
if not exist "%ROOT%\.mozconfig-windows" (
  echo Missing "%ROOT%\.mozconfig-windows"
  exit /b 1
)

call :to_msys "%ROOT%" ROOT_MSYS
if errorlevel 1 exit /b 1
call :to_msys "%MB%" MB_MSYS
if errorlevel 1 exit /b 1

set "MOZILLABUILD=%MB%\"
"%MB%\msys\bin\bash.exe" --login -c "cd '%ROOT_MSYS%' && export MOZCONFIG='%ROOT_MSYS%/.mozconfig-windows' && export PYTHON='%MB_MSYS%/python3/python3.exe' && export PATH='%MB_MSYS%/python3:%MB_MSYS%/python3/Scripts:'$PATH && ./mach !MACH_CMD!"
set "RC=%ERRORLEVEL%"
exit /b %RC%

:to_msys
set "WINPATH=%~1"
if "%WINPATH:~-1%"=="\" set "WINPATH=%WINPATH:~0,-1%"
if /I not "%WINPATH:~1,1%"==":" (
  echo Not a drive path: "%WINPATH%"
  exit /b 1
)
set "DRIVE=%WINPATH:~0,1%"
set "TAIL=%WINPATH:~2%"
set "TAIL=%TAIL:\=/%"
set "DRIVE=%DRIVE:A=a%"
set "DRIVE=%DRIVE:B=b%"
set "DRIVE=%DRIVE:C=c%"
set "DRIVE=%DRIVE:D=d%"
set "DRIVE=%DRIVE:E=e%"
set "DRIVE=%DRIVE:F=f%"
set "DRIVE=%DRIVE:G=g%"
set "DRIVE=%DRIVE:H=h%"
set "DRIVE=%DRIVE:I=i%"
set "DRIVE=%DRIVE:J=j%"
set "DRIVE=%DRIVE:K=k%"
set "DRIVE=%DRIVE:L=l%"
set "DRIVE=%DRIVE:M=m%"
set "DRIVE=%DRIVE:N=n%"
set "DRIVE=%DRIVE:O=o%"
set "DRIVE=%DRIVE:P=p%"
set "DRIVE=%DRIVE:Q=q%"
set "DRIVE=%DRIVE:R=r%"
set "DRIVE=%DRIVE:S=s%"
set "DRIVE=%DRIVE:T=t%"
set "DRIVE=%DRIVE:U=u%"
set "DRIVE=%DRIVE:V=v%"
set "DRIVE=%DRIVE:W=w%"
set "DRIVE=%DRIVE:X=x%"
set "DRIVE=%DRIVE:Y=y%"
set "DRIVE=%DRIVE:Z=z%"
set "%~2=/%DRIVE%%TAIL%"
exit /b 0

:usage
echo Usage: win-mach.cmd [/mozillabuild ^<dir^>] ^<mach arguments^>
echo   Source tree: the directory containing this script.
echo   MozillaBuild: the MOZILLABUILD variable, or C:\mozilla-build when it is unset.
echo   win-mach.cmd clobber
echo   win-mach.cmd build
echo   win-mach.cmd /mozillabuild D:\mozilla-build build
exit /b 1
