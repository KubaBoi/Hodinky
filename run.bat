arduino-cli compile --fqbn esp32:esp32:lilygo_t_display Hodinky.ino -v --output-dir .\build
esptool --chip esp32 --port COM11 --baud 460800 write_flash -z 0x1000 .\build\Hodinky.ino.bootloader.bin 0x8000 .\build\Hodinky.ino.partitions.bin 0x10000 .\build\Hodinky.ino.bin