import os
import sys
import urllib.request

PROGRAM_VERSION = "2.0.2"
GITHUB_VERSION = ""
file_counter: int = 10000
folder_counter: int = 1


def check_version() -> None:
    """
    Check the program version versus the github version number

    :return: None
    """
    global GITHUB_VERSION
    global PROGRAM_VERSION
    git_url: str = "https://raw.githubusercontent.com/Nikolai558/SCT_Parse/master/README.txt"
    update_source: urllib.request.urlopen = urllib.request.urlopen(git_url)
    update_contents: list = update_source.readlines()
    update_source.close()

    for i in update_contents:
        if i[:7] == b"Version":
            GITHUB_VERSION = str(i[-7:-2]).strip("b'")

    if GITHUB_VERSION == PROGRAM_VERSION:
        pass
    else:
        while True:
            continue_var: str = input(f"Your Version: {PROGRAM_VERSION}\n"
                                      f"Current Version on Github: {GITHUB_VERSION}\n"
                                      f"Would you like to continue? [Y/N]: ").lower().strip()

            if continue_var == "n":
                exit()

            if continue_var == "y":
                return


def create_folder(folder_name: str, directory: str = os.getcwd(), insert_number: bool = True) -> str:
    """
    Create's Folder to hold all of the split Sector Files.

    :param insert_number: Insert a number before the folder name
    :param directory: Base Directory
    :param folder_name: FolderName
    :return: Full File Path for the Directory created
    """
    global folder_counter

    if insert_number:
        output: str = f"{directory}\\{str(folder_counter).zfill(2)}_{folder_name}"
        folder_counter += 1
    else:
        output: str = f"{directory}\\{folder_name}"

    try:
        os.mkdir(output)
        print(f"Creating Folder for {folder_name}")
    except FileExistsError:
        print(f"Folder for {folder_name} Found\nPlease delete that folder or rename it.\nPress Enter to Close")
        sys.exit()
    return output


def read_sector_file() -> list:
    """
    Read Sector File (.SCT2)

    :return: List of strings.
    """
    try:
        file: open = open("SECTOR.SCT2", "r")
        output: list = file.readlines()
        file.close()
        print("Reading SECTOR.SCT2")
    except FileNotFoundError:
        input("Sector File not Found. Verify it is named 'SECTOR.SCT2'\n\nPress Enter to Close.")
        sys.exit()
    return output


def create_individual_file(file_name: str, directory: str = "Sector_Files") -> open:
    global file_counter
    print(f"Creating File for {file_name}")
    file: open = open(f"{directory}\\{file_counter}_{file_name}.txt", "w")
    file_counter += 10
    return file


def parse_sections(lines: list) -> dict:
    """
    Sort the Sector File into the different required sections. [INFO] Must be after Colors

    :param lines: List of strings (Lines in SCT2 file)
    :return: Dictionary, Key = Required Section, Value = List of strings for that Required Section
    """
    output: dict = {"STARTING": [], "COLORS": [], "INFO": [], "VOR": [], "NDB": [], "AIRPORT": [], "RUNWAY": [],
                    "FIXES": [], "ARTCC": [], "ARTCC HIGH": [], "ARTCC LOW": [], "SID": [], "STAR": [],
                    "LOW AIRWAY": [], "HIGH AIRWAY": [], "GEO": [], "REGIONS": [], "LABELS": []}

    current_section: str = "STARTING"

    for line in lines:
        line: str = line.strip('\n')

        if line == "":
            line: str = "\n"

        if current_section == "STARTING":
            if line[0] != "#":
                output[current_section].append(line)
            else:
                current_section: str = "COLORS"
                output[current_section].append(line)
            continue

        if current_section == "COLORS":
            if line[0] == "[":
                current_section: str = line[1:-1]
                output[current_section].append(line)
            else:
                output[current_section].append(line)
            continue

        if current_section == "INFO":
            if line[0] == "[":
                current_section: str = line[1:-1]
                output[current_section].append(line)
            else:
                output[current_section].append(line)
            continue

        if line[0] == "[":
            current_section: str = line[1:-1]
            output[current_section].append(line)
        else:
            output[current_section].append(line)

    return output


def sub_section_helper(lines: list, sub_section: str) -> dict:
    """
    Help Parse SID's and STAR's into individual dictionary so that it can be printed to individual files.

    :param sub_section: STAR or SID
    :param lines: list of strings (All lines under the [SID] Section
    :return: Dictionary containing the required sub sections, Key = FileName (Alpha Numeric Safe), Value = List
    """
    output: dict = {}

    key_name: str = ""
    for line in lines:
        line: str = line.strip('\n')
        if line == "":
            line: str = "\n"

        if line[0] == "[":
            key_name: str = f"{sub_section}"
            output[key_name]: list = []
            output[key_name].append(line)
            continue
        if line[0] == ";":
            output[key_name].append(line)
            continue
        if line[0] == " ":
            output[key_name].append(line)
            continue

        temp_name: str = line[:26].strip()
        if temp_name.isalnum():
            key_name: str = temp_name
        else:
            key_name: str = ""
            for c in temp_name:
                if c.isalnum():
                    key_name += c
                else:
                    key_name += "-"

        output[key_name]: list = []
        output[key_name].append(line)

    return output


def split_individual_sections(name: str, lines: list) -> None:
    """
    Split Individual Sections into multiple files.

    :param name: string File name
    :param lines: List of lines inside file.
    :return: None
    """
    if name == "SID" or name == "STAR":
        _dir: str = create_folder(directory=f"{os.getcwd()}\\Sector_Files", folder_name=name)
        data: dict = sub_section_helper(lines, name)
        for k, v in data.items():
            file: open = create_individual_file(k, directory=_dir)
            for line in v:
                file.write(line + "\n")
            file.close()
        return

    else:
        _dir: str = create_folder(directory=f"{os.getcwd()}\\Sector_Files", folder_name=name)
        file: open = create_individual_file(name, directory=_dir)
        for line in lines:
            file.write(line + "\n")
        file.close()


def main() -> None:
    """
    Main Program Entry

    :return: None
    """
    all_lines: list = read_sector_file()
    create_folder("Sector_Files", insert_number=False)

    sections: dict = parse_sections(all_lines)

    for k, v in sections.items():
        split_individual_sections(k, v)


if __name__ == '__main__':
    check_version()
    main()
    input("Program Complete\n\nPress enter to Close.")
