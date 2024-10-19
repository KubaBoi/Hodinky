echo off
set port=COM11
set baud=460800

set filepath=%1 
if [%1] == [] set filepath=Hodinky.ino
for %%a in ("%filepath%") do set name=%%~nxa
echo %filepath% %name%

arduino-cli compile --fqbn esp32:esp32:lilygo_t_display %filepath% -v --output-dir .\build
if %errorlevel% neq 0 exit /b %errorlevel%

esptool --chip esp32 --port %port% --baud %baud% ^
    write_flash -z ^
    0x1000 .\build\%name%.bootloader.bin ^
    0x8000 .\build\%name%.partitions.bin ^
    0x10000 .\build\%name%.bin              