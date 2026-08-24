## License & Usage Restrictions
Do not mirror or clone this repository to **Gitee** or any other platform.

# Debuger-for-hex-file
A Linux debugger for Linux users to easily download their hex files into their ARM Cortex devices.Built on pyOCD and Miniconda, this project was born from the laziness of typing flash commands.

## Installation
You can install the software using:
sudo apt install ./xxxx.deb
## Currently supports:
The software currently supports STM32, Texas Instruments (TI), GD32, and 8051 series microcontrollers.

## Install Additional Chip Packs:
conda run -n universal-flasher pyocd pack --install <pack-name>
## Install Chip Packs Example:
conda run -n universal-flasher pyocd pack --install Keil.STM32F1xx_DFP
## Search For Available Packs:
conda run -n universal-flasher pyocd pack --find <keyword>
## Search For Available Packs Example:
conda run -n universal-flasher pyocd pack --find stm32f103
## Verify installation:
conda run -n universal-flasher pyocd pack --show
## Warning： 
Compatibility with other devices has not been tested yet.
The steps above are for reference only. Actual results may vary — please open an issue or submit feedback if you encounter any problems.

