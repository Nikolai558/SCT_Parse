import os
import sys
import urllib.request

program_version = "1.2.0"
github_version = None
count_variable = 10000


def check_version():
    global github_version
    global program_version
    git_url = "https://raw.githubusercontent.com/Nikolai558/SCT_Parse/master/README.txt"
    updateSource = urllib.request.urlopen(git_url)
    updateContents = updateSource.readlines()
    updateSource.close()

    for i in updateContents:
        if i[:7] == b"Version":
            github_version = str(i[-7:-2]).strip("b'")

    if github_version == program_version:
        pass
    else:
        continue_var = input(f"Your Version: {program_version}\n"
              f"Current Version on Github: {github_version}\n"
              f"Would you like to continue? [Y/N]: ").lower().strip()
        if continue_var == "n":
            exit()
        elif continue_var == "y":
            pass
        else:
            check_version()


file_counter = 10000


def create_folder() -> None:
    """
    Create's Folder to hold all of the split Sector Files.

    :return: None
    """
    try:
        os.mkdir("Sector_Files")
        print("Creating Folder for Sector_Files")
    except FileExistsError:
        print("Folder for Sector_Files Found\nPlease delete that folder or rename it.\nPress Enter to Close")
        sys.exit()


def read_sector_file() -> list:
    """
    Read Sector File (.SCT2)

    :return: List of strings.
    """
    try:
        file = open("SECTOR.SCT2", "r")
        output = file.readlines()
        file.close()
        print("Reading SECTOR.SCT2")
    except FileNotFoundError:
        input("Sector File not Found. Verify it is named 'SECTOR.SCT2'\n\nPress Enter to Close.")
        sys.exit()
    return output


def create_individual_file(file_name: str, directory: str = "Sector_Files") -> open:
    global file_counter
    print(f"Creating File for {file_name}")
    file = open(f"{directory}\\{file_counter}_{file_name}.txt", "w")
    file_counter += 10
    return file


def parse_sections(lines: list) -> dict:
    """
    Sort the Sector File into the different required sections. [INFO] Must be after Colors

    :param lines: List of strings (Lines in SCT2 file)
    :return: Dictionary, Key = Required Section, Value = List of strings for that Required Section
    """
    output = {"STARTING": [], "COLORS": [], "INFO": [], "VOR": [], "NDB": [], "AIRPORT": [], "RUNWAY": [], "FIXES": [],
              "ARTCC": [], "ARTCC HIGH": [], "ARTCC LOW": [], "SID": [], "STAR": [], "LOW AIRWAY": [],
              "HIGH AIRWAY": [], "GEO": [], "REGIONS": [], "LABELS": []}

    current_section = "STARTING"

    for line in lines:
        line = line.strip('\n')

        if line == "":
            line = "\n"

        if current_section == "STARTING":
            if line[0] != "#":
                output[current_section].append(line)
            else:
                current_section = "COLORS"
                output[current_section].append(line)
            continue

        if current_section == "COLORS":
            if line[0] == "[":
                current_section = line[1:-1]
                output[current_section].append(line)
            else:
                output[current_section].append(line)
            continue

        if current_section == "INFO":
            if line[0] == "[":
                current_section = line[1:-1]
                output[current_section].append(line)
            else:
                output[current_section].append(line)
            continue

        if line[0] == "[":
            current_section = line[1:-1]
            output[current_section].append(line)
        else:
            output[current_section].append(line)

    return output


def sub_section_helper(lines: list, sub_section: str) -> dict:
    """
    Help Parse SID's and STAR's into individual dictionary so that it can be printed to individual files.

    :param sub_section: STAR or SID
    :param lines: list of strings (All lines under the [SID] Section
    :return: Dictionary containing the required sub sections, Key = FileName (Alpha Numaric Safe), Value = List
    """
    output = {}

    key_name = None
    for line in lines:
        line = line.strip('\n')
        if line == "":
            line = "\n"

        if line[0] == "[":
            key_name = f"{sub_section}"
            output[key_name] = []
            output[key_name].append(line)
            continue
        if line[0] == ";":
            output[key_name].append(line)
            continue
        if line[0] == " ":
            output[key_name].append(line)
            continue

        temp_name = line[:26].strip()
        if temp_name.isalnum():
            key_name = temp_name
        else:
            key_name = ""
            for c in temp_name:
                if c.isalnum():
                    key_name += c
                else:
                    key_name += "-"

        output[key_name] = []
        output[key_name].append(line)

    return output


def split_individual_sections(name: str, lines: list) -> None:
    if name == "SID" or name == "STAR":
        data = sub_section_helper(lines, name)
        for k, v in data.items():
            file = create_individual_file(k)
            for line in v:
                file.write(line + "\n")
            file.close()
        return

    else:
        file = create_individual_file(name)
        for line in lines:
            file.write(line + "\n")
        file.close()


def main():
    all_lines = read_sector_file()

    create_folder()

    sections = parse_sections(all_lines)

    for k, v in sections.items():
        split_individual_sections(k, v)


if __name__ == '__main__':
    check_version()
    main()
    input("Program Complete\n\nPress enter to Close.")
