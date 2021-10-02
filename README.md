# BerryFlasher

## Installation

```bash
git clone --branch alpha https://github.com/pixailz/berry-flasher
cd berry-flasher
pip install -r requirements.txt
python3 berry-flasher
```

## TO REWRITE
CrossUtils.convert_byte
- handle float number

CrossUtils.download()
1. reduce refresh time

    OR
2. change condition  `elapsed_time_brute[1][:1] == "0"`

LinUtils.do_command()

## TO DO
WinUtils.flash_disk()
- make menu for selecting image to flash
  - download system image from link

#### PEP8 "linter"
```powershell
pycodestyle.exe --ignore="E501,E302,E305,E226,E265" <file_name>
```
