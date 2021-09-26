#!/usr/bin/env python3
#coding:utf-8
# version : alpha_0.0.3
# https://github.com/Pixailz

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
# HEADER

import urllib.request
import subprocess
import pathlib
import zipfile

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#

class CrossUtils():

    @staticmethod
    def get_os():

        """os.name like function with subprocess"""

        try:
            subprocess.run("/bin/ls")
        except FileNotFoundError:
            return "nt"
        else:
            return"posix"

    @staticmethod
    def is_alpha_num(txt):

        """return True if the line is not empty
        (to avoid empty line in output)"""

        return any([char.isalnum() for char in txt])

    @staticmethod
    def convert_byte(number):

        """Byte converter"""

        tmp_number = round(int(number) / 1_000_000_000)

        if tmp_number == 0:
            converted = "0 o"

        elif tmp_number > 0:
            converted = f"{tmp_number} Go"
        else:
            tmp_number = round(int(number) / 1_000_000)
            converted = f"{tmp_number} Mo"

        return converted

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#

class WinUtils():
    def __init__(self):

        """path_to_ps : path to powershell, needed in some case"""

        self.path_to_ps = "C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe"

    def do_command(self, command, print_out=False, get_out=True):

        """print_out : True  -> print output to user
                    False -> don't print output to user"""

        if print_out:
            out = subprocess.getoutput([self.path_to_ps, command])
            print(out)
            return out

        else:
            out = subprocess.getoutput([self.path_to_ps, command])
            return out

    def balena_check_update(self):

        """get current installed version tag and check if it's up to date"""

        # get current version tag
        current_tag = self.do_command("./bin/balena-cli-win/balena.exe version")

        # if current tag match latest
        if current_tag == self.latest_tag.strip("v"):
            print("balena-cli latest update")

        # else run balena_install() but with update=True
        else:
            print("NEED TO UPGRADE")
            self.balena_install(update=True)

    def balena_install(self, update=False):

        """Download and installation of the latest release of
        balena-cli-standalone"""

        # check if tmp is present
        path_to_tmp = pathlib.Path("./tmp")

        # if True, delete it
        if path_to_tmp.exists():
            print("removing tmp folder")
            self.do_command("rm -r tmp")

        # creation of tmp folder
        print("creating tmp folder")
        self.do_command("mkdir tmp")

        # donwloading with powershell
        print("Downloading file")
        self.do_command(f"Invoke-WebRequest -Uri '{self.link}' -OutFile './tmp/balena_tmp_win.zip'")

        # if update == True, delete ./bin/balena-cli-win folder
        if update:
            self.do_command("rm -r ./bin/balena-cli-win")

        # unzip downloaded file in bin
        with zipfile.ZipFile("./tmp/balena_tmp_win.zip", "r") as zip_ref:
            zip_ref.extractall("./bin")

        # rename installation folder
        self.do_command("mv ./bin/balena-cli ./bin/balena-cli-win")

        # delete tmp
        self.do_command("rm -r tmp")

    def balena_cli(self):

        """Checking of necessary file
            if present, update, else download and installation"""

        # get tag of the latest release for balena-cli
        url = "https://github.com/balena-io/balena-cli/releases/latest"
        response = urllib.request.urlopen(url)
        latest_link = response.geturl().split("/")
        self.latest_tag = latest_link[len(latest_link)-1]

        # create download link
        link_base = "https://github.com/balena-io/balena-cli/releases/download/"
        link_version = f"{self.latest_tag}/balena-cli-{self.latest_tag}-windows-x64-standalone.zip"
        self.link = link_base + link_version

        # check if installation folder is present
        instalation_folder = pathlib.Path("./bin/balena-cli-win")
        if instalation_folder.exists():
            print("installation folder for windows found")
            self.balena_check_update()

        else:
            self.balena_install()

    def check_root(self):

        """check if script is launched with elevated privileges"""

        command = ("([Security.Principal.WindowsPrincipal]"
                   "[Security.Principal.WindowsIdentity]::GetCurrent())"
                   ".IsInRole([Security.Principal.WindowsBuiltInRole] 'Administrator')")

        is_elevate = self.do_command(command)

        # here the output of subprocess return an string and not an booleen, so convertion :)
        if is_elevate == "True":
            is_elevate = True

        else:
            is_elevate = False

        return is_elevate

    def parse_info_disk(self):

        """parsing of disk info with the form :
                - identifiers (path)
                - total space (space)
                - model an manufacturer (name)"""

        # split output in lines
        line_disk = self.disk_brut.split("\n")

        # number of line before data
        header_length = 2

        # number of column
        option_length = 4

        for i in range(len(line_disk)):

            # if line isn't in header
            if not i < header_length:

                # if line have data
                if CrossUtils.is_alpha_num(line_disk[i]):

                    """
                    spliting line in "case" maxsplit is used here to retrieve the
                    last two column, wich contain quite often spaces and split
                    check for the spaces
                    """
                    tmp_line = line_disk[i].split(maxsplit=option_length-1)

                    # all the information need to be here
                    if len(tmp_line) < option_length:
                        print("tmp_line too small")

                    else:

                        # if the first column (is_system) return True then skip the line
                        if tmp_line[0] == "True":
                            continue

                        # else delete is_system, we don't need it anymore
                        else:
                            tmp_line.pop(0)

                        # convertion of bytes to Go/Mo
                        tmp_space = CrossUtils.convert_byte(tmp_line[0])

                        # fusion of the column "Manufacturer" and "Model"
                        tmp_name = "".join(tmp_line[2].split())

                        # format data in dictionary
                        disk_info = {
                            "path": tmp_line[1],
                            "space": tmp_space,
                            "name": tmp_name
                        }

                        # add dictionary to the big disk list
                        self.disk.append(disk_info)

    def list_disk(self):

        """get a list of disk"""

        self.disk = []

        command_list_disk = "Get-Disk"

        # filter to "organize" information
        command_filter = " | Format-Table -Property IsSystem,size,number,Manufacturer,Model"
        command_list_disk += command_filter

        # retreive data of disk
        self.disk_brut = self.do_command(command_list_disk)

        # split info
        self.parse_info_disk()

        return self.disk

    def flash_disk(self):
        pass

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#

class LinUtils():
    def check_root(self):

        """check if script is launched with elevated privileges"""

        pass

    def list_disk():
        pass

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#

class BerryFlasher():

    """main loop (cf. deathloop)"""

    def __init__(self):
        self.main()

    def main(self):

        # declaration of cross-platform utility
        cross_utils = CrossUtils()

        """here the tips it's that all the principal function in WinUtils or LinUtils
        have the same name"""

        if cross_utils.get_os() == "nt":
            utils = WinUtils()

        else:
            utils = LinUtils()

        # check if balena-cli is correctly installed
        utils.balena_cli()

        # if privileges are not elevated
        if not utils.check_root():
            print("launch script with elevated privileges")
            exit()

        self.list_disk = utils.list_disk()

        self.print_disk()

        # choice with the given list below
        selected_disk = input("select a disk from above : ")

        utils.flash_disk()

    def print_disk(self):

        """print list of disk given with the utils.list_disk"""

        if len(self.list_disk) == 0:
            print("No elegible disk found, exiting ...")
            exit()

        for i in range(len(self.list_disk)):
            print("===========================")

            for k, v in self.list_disk[i].items():
                print(f"{k} : {v}")

            print("===========================\n")

BerryFlasher()
