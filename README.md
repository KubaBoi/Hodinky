
# Readme

Project Hodinky.ino is simple watch program. Instalation is:

`.\run.bat`

Without any argument.

## Toolchain

https://github.com/cjacker/opensource-toolchain-esp32

## Setup

ISA: https://www.cadence.com/content/dam/cadence-www/global/en_US/documents/tools/silicon-solutions/compute-ip/isa-summary.pdf

https://t-watch-document-en.readthedocs.io/en/latest/introduction/product/2020.html

https://wellys.com/posts/esp32_cli/

`arduino-cli core update-index https://dl.espressif.com/dl/package_esp32_index.json`

`arduino-cli config init`

config file: `C:\Users\Jakub Anderle\AppData\Local\Arduino15\arduino-cli.yaml`

```
board_manager:
  additional_urls:
    - https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
```

`arduino-cli core install esp32:esp32@2.0.17` 

`arduino-cli board list`

`arduino-cli compile --fqbn esp32:esp32:lilygo_t_display Hodinky.ino -v --output-dir .\build`

`esptool --chip esp32 --port COM11 --baud 460800 write_flash -z 0x1000 .\build\Hodinky.ino.bootloader.bin 0x8000 .\build\Hodinky.ino.partitions.bin 0x10000 .\build\Hodinky.ino.bin`

- --chip esp32: Specifikace čipu ESP32.
- --port COM11: Specifikace sériového portu, ke kterému je vaše ESP32 připojeno.
- --baud 460800: Nastavení baud rate pro rychlejší nahrávání (může být nižší, pokud máte problémy s připojením).
- write_flash -z: Přikazuje esptool, aby nahrál (flash) specifikované binární soubory.
- 0x1000 Hodinky.ino.bootloader.bin: Adresa a cesta k binárnímu souboru bootloaderu.
- 0x8000 Hodinky.ino.partitions.bin: Adresa a cesta k binárnímu souboru partition table.
- 0x10000 Hodinky.ino.bin: Adresa a cesta k vašemu firmware.