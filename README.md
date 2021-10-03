# BerryFlasher

## Installation

```bash
git clone --branch alpha https://github.com/pixailz/berry-flasher
cd berry-flasher
pip install -r requirements.txt
python3 berry-flasher
```

## TO REWRITE
CrossUtils.download()
- refresh don't work all the time (must be fix)
  1. reduce refresh time

      OR
  2. change condition  `elapsed_time_brute[1][:1] == "0"`

LinUtils.do_command()

## TO DO
WinUtils.flash_disk()
- make menu for selecting image to flash
  - download system image from link

### NOTA BENE
VSCode Shortcuts from [here](https://www.codegrepper.com/code-examples/css/collapse+all+functions+visual+studio+code)
- unfolds all:
  - `Ctrl + K + J`

- folding level:
  - fold all
    - `Ctrl + K + 0`
  - fold main:
    - `Ctrl + K + 1`
  - fold sub level 1:
    - `Ctrl + K + 2`
  - fold sub level 2:
    - `Ctrl + K + 3`
  - etc ...

#### PEP8 "linter"
```powershell
pycodestyle --ignore="E501,E302,E305,E226,E265" berry-flasher.py
```
