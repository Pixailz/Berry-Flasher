#!/usr/bin/env python3
#coding:utf-8
version = "alpha 0.0.4"
# https://github.com/Pixailz

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
# HEADER

import subprocess
import requests
import pathlib
import zipfile
import time

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#

class CrossUtils():

    @staticmethod
    def get_os():

        """os.name like function with subprocess"""

        try:
            subprocess.run("/bin/ls", stdout=subprocess.PIPE)
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
    def convert_byte(number, rounded=False):

        """Byte converter"""

        number = int(number)

        if number > 1_000_000_000_000:
            multiplier = 8 / (8 * 1024 * 1024 * 1024 * 1024)
            measure_unit = "TiB"

        elif number > 1_000_000_000:
            multiplier = 8 / (8 * 1024 * 1024 * 1024)
            measure_unit = "GiB"

        elif number > 1_000_000:
            multiplier = 8 / (8 * 1024 * 1024)
            measure_unit = "MiB"

        elif number > 1_000:
            multiplier = 8 / (8 * 1024)
            measure_unit = "MiB"

        else:
            multiplier = 1
            measure_unit = f"B"

        if rounded:
            tmp_number = int(round(number * multiplier))
            converted = f"{tmp_number}{measure_unit}"

        else:
            tmp_number = round(number * multiplier, 2)
            converted = f"{tmp_number}{measure_unit}"

        return converted

    @staticmethod
    def download(link, file_path, title=""):

        """
        based on this:
        https://stackoverflow.com/a/21868231/7261056
        """

        with open(file_path, "wb") as f:

            # download of file
            response = requests.get(link, stream=True)
            # get length of ile in header
            total_length = response.headers.get("content-length")

            # if total length is not present in header
            if total_length is None:
                # write without progress bar :'(
                f.write(response.content)

            else:
                # cast in int of str
                total_length = int(total_length)
                # convert in human readable
                converted_length = CrossUtils.convert_byte(total_length, rounded=True)

                # epoch begin time
                begin_time = time.time()

                # need to be declared out of the loop
                downloaded_byte = 0
                str_speed = ""
                tmp_seconde = 0

                for data in response.iter_content(chunk_size=4096):

                    # add lenght of data in downloaded _byte
                    downloaded_byte += len(data)
                    # write data
                    f.write(data)

                    # get a list of second(0) and millisecond(1)
                    elapsed_time_brute = str(time.time() - begin_time).split(".")

                    seconde = int(elapsed_time_brute[0])
                    # cut for 2 digits
                    ms = elapsed_time_brute[1][:2]

                    # cross product for a length of 25
                    done = int(25 * downloaded_byte / total_length)
                    # cross product for pourcentage
                    pourcentage_done = int(100 * downloaded_byte / total_length)

                    number_of_dot = (seconde % 3) + 1
                    dot = "." * number_of_dot
                    space = " " * (3 - number_of_dot)
                    str_dot = "Download" + dot + space

                    # done str
                    egal_str = "-" * done
                    # head str
                    egal_str += ">"
                    # empty str
                    empy_str = " " * (25 - done)
                    str_progress = f"[{egal_str}{empy_str}]"

                    # elapsed time
                    minute = seconde // 60
                    seconde = seconde % 60
                    str_elapsed = f"[{str(minute).zfill(2)}:{str(seconde).zfill(2)}:{ms}]"

                    # refresh per second
                    if seconde > tmp_seconde:
                        tmp_seconde = seconde
                        # speed convertion
                        download_speed = CrossUtils.convert_byte(downloaded_byte / seconde)
                        str_speed = f"{download_speed}/s"

                    downloaded_done = CrossUtils.convert_byte(downloaded_byte, rounded=True)
                    str_downloaded = f"({downloaded_done}/{converted_length}/{pourcentage_done}%)"

                    print(f"\r{str_dot}{str_progress} {title} {str_elapsed} {str_speed} {str_downloaded}", flush=True, end="")

                print(" done")

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#

class WinUtils():
    def __init__(self):

        """path_to_ps : path to powershell, needed in some case"""

        self.path_to_ps = "C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe"

    def do_command(self, command, print_out=False):

        """print_out : True  -> print output to user
                    False -> don't print output to user"""

        if print_out:
            subprocess.run([self.path_to_ps, command])

        else:
            out = subprocess.getoutput([self.path_to_ps, command])
            return out

    def balena_check_update(self):

        """get current installed version tag and check if it's up to date"""

        # get current version tag
        current_tag = self.do_command("./bin/balena_cli_win/balena.exe version")

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

        # downloading with python
        CrossUtils.download(self.link, "./tmp/balena_cli_tmp.zip", "balena-cli")

        # if update == True, delete ./bin/balena_cli_win folder
        if update:
            self.do_command("rm -r ./bin/balena_cli_win")

        # unzip downloaded file in bin
        with zipfile.ZipFile("./tmp/balena_cli_tmp.zip", "r") as zip_ref:
            zip_ref.extractall("./bin")

        # rename installation folder
        self.do_command("mv ./bin/balena-cli ./bin/balena_cli_win")

        # delete tmp
        self.do_command("rm -r tmp")

    def balena_cli(self):

        """Checking of necessary file
            if present, update, else download and installation"""

        # get tag of the latest release for balena-cli
        link = "https://github.com/balena-io/balena-cli/releases/latest"
        response = requests.get(link)
        latest_link = response.url.split("/")
        self.latest_tag = latest_link[len(latest_link)-1]

        # create download link
        link_base = "https://github.com/balena-io/balena-cli/releases/download/"
        link_version = f"{self.latest_tag}/balena-cli-{self.latest_tag}-windows-x64-standalone.zip"
        self.link = link_base + link_version

        # check if installation folder is present
        instalation_folder = pathlib.Path("./bin/balena_cli_win")
        if instalation_folder.exists():
            print("installation folder for Windows found")
            self.balena_check_update()

        else:
            self.balena_install()

    def check_root(self):

        """check if script is launched with elevated privileges"""

        command = ("([Security.Principal.WindowsPrincipal]"
                   "[Security.Principal.WindowsIdentity]::GetCurrent())"
                   ".IsInRole([Security.Principal.WindowsBuiltInRole] 'Administrator')")

        is_elevate = self.do_command(command)

        # here the output of subprocess return a string and not a booleen, so convertion :)
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
                        disk_info = [
                            tmp_line[1],
                            tmp_space,
                            tmp_name
                        ]

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

    def flash_disk(self, file_to_patch, disk_id):

        #\\.\PhysicalDrive<id> with id given by list_disk()
        command = (
            "./bin/balena_cli_win/balena "
            f"local flash {file_to_patch} "
            "--drive '\\\\.\\"
            f"PhysicalDrive{disk_id}' "
            "--yes"
        )

        try:
            subprocess.run([self.path_to_ps, command])

        except KeyboardInterrupt:
            # for interrupting balena validating process at the end
            # good flashing average since long time using gui version ;)
            pass

    def clear_screen(self):
        self.do_command("cls")

    def return_terminal_width(self):
        return int(self.do_command("$Host.UI.RawUI.WindowSize.Width"))
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#

class LinUtils():
    def do_command(self, command, print_out=False):

        if not print_out:
            out = subprocess.getoutput(f"/bin/bash -c '{command}'")
            return out

        else:
            subprocess.run(["/bin/bash", "-c", command])

    def balena_check_update(self):

        """get current installed version tag and check if it's up to date"""

        # get current version tag
        current_tag = self.do_command("./bin/balena_cli_lin/balena version")

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

        # downloading with python
        CrossUtils.download(self.link, "./tmp/balena_cli_tmp.zip", "balena-cli")

        # if update == True, delete ./bin/balena_cli_win folder
        if update:
            self.do_command("rm -r ./bin/balena_cli_lin")

        # unzip downloaded file in bin
        with zipfile.ZipFile("./tmp/balena_cli_tmp.zip", "r") as zip_ref:
            zip_ref.extractall("./bin")

        # rename installation folder
        self.do_command("mv ./bin/balena-cli ./bin/balena_cli_lin")

        # give right permission
        self.do_command("chmod +x ./bin/balena_cli_lin/balena")

        # delete tmp
        self.do_command("rm -r tmp")

    def balena_cli(self):

        """Checking of necessary file
            if present, update, else download and installation"""

        # get tag of the latest release for balena-cli
        link = "https://github.com/balena-io/balena-cli/releases/latest"
        response = requests.get(link)
        latest_link = response.url.split("/")
        self.latest_tag = latest_link[len(latest_link)-1]

        # create download link
        link_base = "https://github.com/balena-io/balena-cli/releases/download/"
        link_version = f"{self.latest_tag}/balena-cli-{self.latest_tag}-linux-x64-standalone.zip"
        self.link = link_base + link_version

        # check if installation folder is present
        instalation_folder = pathlib.Path("./bin/balena_cli_lin")
        if instalation_folder.exists():
            print("installation folder for Linux found")
            self.balena_check_update()

        else:
            self.balena_install()

    def check_root(self):

        """check if script is launched with elevated privileges"""

        is_root = self.do_command("echo $UID")

        if is_root == "0":
            return True

        else:
            return False

    def parse_info_disk(self):

        line_disk = self.disk_brut.split("\n")

        for line in line_disk:
            tmp_line = line.split(maxsplit=3)

            if tmp_line[0] != "usb":
                continue

            if tmp_line[2] == "0":
                continue

            tmp_transport_type = tmp_line[0]
            tmp_path = tmp_line[1]
            tmp_space = CrossUtils.convert_byte(tmp_line[2])
            tmp_name = tmp_line[3].replace(" ", "")

            disk_info = [
                tmp_path,
                tmp_space,
                tmp_name
            ]

            self.disk.append(disk_info)

    def list_disk(self):
        self.disk = []

        command = "lsblk --nodeps --noheadings --bytes --output tran,path,size,vendor,model"
        command += " --list"

        self.disk_brut = subprocess.getoutput(command)

        self.parse_info_disk()

        return self.disk

    def flash_disk(self, file_to_patch, disk_id):

        command = (
            "./bin/balena_cli_lin/balena "
            f"local flash {file_to_patch} "
            f"--drive {disk_id} "
            "--yes"
        )

        try:
            #self.do_command(command, print_out=True)
            subprocess.run(["/bin/bash", "-c", command])

        except KeyboardInterrupt:
            # for interrupting balena validating process at the end
            # good flashing average since long time using gui version ;)
            pass

    def clear_screen(self):
        self.do_command("clear", print_out="True")

    def return_terminal_width(self):
        size = self.do_command("stty size").split()
        height = size[0]
        width = size[1]

        return int(width)
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#

class BerryFlasher():

    """main loop (cf. deathloop)"""

    def __init__(self):
        # declaration of cross-platform utility
        self.cross_utils = CrossUtils()

        if self.cross_utils.get_os() == "nt":
            self.utils = WinUtils()

        else:
            self.utils = LinUtils()

        # check if balena-cli is correctly installed
        self.utils.balena_cli()

        # if privileges are not elevated
        if not self.utils.check_root():
            print("launch script with elevated privileges")
            exit()

        self.menu()

    def menu_print_title(self, title):
        bf_version = f"BF {version}"
        bf_version_length = len(bf_version)
        self.center_title = self.utils.return_terminal_width()

        title = title.center(self.center_title - (bf_version_length * 2))
        print(bf_version+ title)

    def menu_print(self):

        self.menu_print_title("MAIN MENU")
        print("")

        for i in range(len(self.menu_options)):
            print(f"    {i+1}. {self.menu_options[i]}")
        print("")

    def menu(self):
        self.menu_options = [
            "List OS",
            "Flash Disk",
            "Update/Install Balena-CLI",
            "Quit"
        ]

        entry_checked = False

        while not entry_checked:
            self.utils.clear_screen()
            self.menu_print()
            entry = input(f"(1-{len(self.menu_options)}): ")

            try:
                int(entry)
            except ValueError:
                print("wrong choice")
                time.sleep(2)
                continue

            for i in range(len(self.menu_options)):
                j = i + 1
                # si Q
                if j == int(entry):
                    entry_checked = True

            if not entry_checked:
                print("wrong choice")
                time.sleep(2)

        if entry == "2":
            self.select_disk()

        elif entry == "4":
            exit()

    def select_disk(self):

        self.list_disk = self.utils.list_disk()
        self.print_disk()

        entry_checked = False
        while not entry_checked:

            # choice with the given list below
            entry = input("select a disk from above : ")

            # refresh disk
            if entry.lower() == "r":
                self.list_disk = self.utils.list_disk()
                self.print_disk()
                continue

            entry = int(entry)

            try:
                self.entry_choice[entry]

            except KeyError:
                print("wrong choice")

            else:
                entry_checked = True


        self.utils.flash_disk(file_to_patch, self.entry_choice[entry])

    def print_disk(self):

        """print list of disk given with the utils.list_disk"""

        if len(self.list_disk) == 0:
            print("No elegible disk found, exiting ...")
            exit()

        else:
            self.entry_choice = {}
            for i in range(len(self.list_disk)):

                disk_id = self.list_disk[i][0]
                self.entry_choice[i+1] = disk_id

                disk_name = self.list_disk[i][2]
                disk_space = self.list_disk[i][1]

                print(f"{i+1}. id: {disk_id} | {disk_name} ({disk_space})")

if __name__ == "__main__":
    BerryFlasher()
