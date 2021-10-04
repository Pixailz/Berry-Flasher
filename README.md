# BerryFlasher

## Installation

```bash
git clone --branch alpha https://github.com/pixailz/berry-flasher
cd berry-flasher
pip install -r requirements.txt
python3 berry-flasher
```

## TO REWRITE

BerryFlasher.print_menu()
- make menu for selecting image to flash
  - download system image from link

## TO DO

add colors :'(
- find cross library or find out in powershell
- i like term color, soooooooo much

## structure for os link

```python
[
    {
        "name": "os_name",
        "variant": "full/lite/nightly",
        "arch": "arm64/armhf",
        "link": "https://dummy.com/os_image.tar.gz",
        "upload_date": "yyyy/mm/dd [HH:mm]",
        "is_present": "true/false"
    },
    {
        "name": "RaspiOS",
        "variant": "full",
        "arch": "arm64",
        "link": "https://downloads.raspberrypi.org/raspios_arm64/images/raspios_arm64-2021-05-28/2021-05-07-raspios-buster-arm64.zip",
        "upload_date": "2021-05-07 17:18",
    },
    {
        "name": "RaspiOS",
        "variant": "nighlty",
        "arch": "armhf",
        "link": "https://downloads.raspberrypi.org/nightlies/2021-09-15-raspios-buster-nightly-armhf.zip",
        "upload_date": "2021-09-15 05:44",
    }
]
```

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
