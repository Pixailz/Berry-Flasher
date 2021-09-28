# BerryFlasher

## Installation

```bash
git clone --branch alpha https://github.com/pixailz/berry-flasher
cd berry-flasher
pip install -r requirements.txt
python3 berry-flasher
```

## TO REWRITE
nothing for the moment

## TO DO
WinUtils.flash_disk()
- make menu for selecting image to flash
  - download system image from link

CrossUtils.Flash()
- check if possible
  - if not make WinUtils.Flash()

UI
- CrossUtils.download
  - add eta

BerryFlasher.print_disk()
- how disk info are displayed, in one line form:
  - entry choice number (assigned with disk id)
  - disk id
  - disk name
  - total space
- clear disk output when refresh etc ...

#### PEP8 "linter"
```powershell
pycodestyle.exe --ignore="E501,E302,E305,E226,E265" <file_name>
```
