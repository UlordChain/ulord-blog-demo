@echo off
echo you can also use python script
SET mypath=%~dp0
rem echo %mypath% using python script
rem echo %mypath%ipfs.exe
xcopy %mypath%ipfs.exe C:\Windows\System32 /Y
rem SET PATH=%PATH%;%mypath%
pause