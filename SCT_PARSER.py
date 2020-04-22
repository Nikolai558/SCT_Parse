import os


try:
    os.mkdir("Sector_Files")
except FileExistsError:
    pass


def create_file(directory_choice, count, file_name):
    global count_variable
    count_variable += 1
    f = open(f"{directory_choice}/{count}_{file_name}.txt", "w")
    return f


count_variable = 10000
with open("ZLC_SECTOR.SCT2", "r") as file:
    all_lines = file.readlines()
    current_line = -1
    next_line = 0

    for lines in all_lines:
        current_line += 1
        next_line += 1
        for character in lines:
            if character[:1] == "#":
                if os.path.exists(f"Sector_Files/{count_variable-1}_Colors.txt"):
                    color_file = open(f"Sector_Files/{count_variable-1}_Colors.txt", "a+")
                else:
                    color_file = create_file("Sector_Files", count_variable, "Colors")
                color_file.write(lines)
                color_file.close()
                print("Made it through # CHECK")

            elif character[:1] == "[" and lines[:5] != "[SID]" and lines[:6] != "[STAR]":
                if os.path.exists(f"Sector_Files/{count_variable - 1}_{lines[:]}.txt"):
                    bracket_file = open(f"Sector_Files/{count_variable - 1}_{lines[:]}.txt", "a+")
                else:
                    bracket_file = create_file("Sector_Files", count_variable, str(lines[:-1]))
                bracket_file.write(lines)
                for section in all_lines[current_line+1:]:
                    if section[:1] == "[":
                        bracket_file.write("\n")
                        bracket_file.close()
                        break
                    bracket_file.write(section)
                print("Made it through bracket CHECK")

            elif character[:1] == "[" and lines[:5] == "[SID]" and lines[:6] != "[STAR]":
                global sid_name
                if os.path.exists(f"Sector_Files/{count_variable - 1}_{lines[:]}.txt"):
                    sids_file = open(f"Sector_Files/{count_variable - 1}_{lines[:]}.txt", "a+")
                else:
                    sids_file = create_file("Sector_Files", count_variable, str(lines[:-1]))
                sids_file.write(lines)
                sids_file.write("\n\n")
                sids_file.close()
                for section1 in all_lines[current_line+1:]:
                    global certain_sid_file

                    if section1[:1] != " " and section1[:1] != '\t' and section1[:1] != "\n" and section1[:1] != "[":
                        sid_name = section1[:26].strip(" ")
                        sid_name = sid_name.replace("/", "-")
                        if os.path.exists(f"Sector_Files/{count_variable - 1}_{sid_name}.txt"):
                            certain_sid_file = open(f"Sector_Files/{count_variable - 1}_{sid_name}.txt", "a+")
                        else:
                            certain_sid_file = create_file("Sector_Files", count_variable, sid_name)
                        certain_sid_file.write(section1)

                    elif section1[:1] == " " or section1[:1] == '\t' or section1[:1] == "\n":
                        certain_sid_file.write(section1)

                    elif section1[:1] == "[":
                        certain_sid_file.write("\n\n")
                        certain_sid_file.close()
                        break
                    else:
                        pass
                print("Made it through SID CHECK")

            elif character[:1] == "[" and lines[:6] == "[STAR]":
                global star_name

                if os.path.exists(f"Sector_Files/{count_variable - 1}_{lines[:]}.txt"):
                    star_file = open(f"Sector_Files/{count_variable - 1}_{lines[:]}.txt", "a+")
                else:
                    star_file = create_file("Sector_Files", count_variable, str(lines[:-1]))
                star_file.write(lines)
                star_file.write("\n\n")
                star_file.close()
                for section6 in all_lines[current_line+1:]:
                    global certain_star_file

                    if section6[:1] != " " and section6[:1] != '\t' and section6[:1] != "\n" and section6[:1] != "[":
                        star_name = section6[:26].strip(" ")
                        star_name = star_name.replace("/", "-")
                        if os.path.exists(f"Sector_Files/{count_variable - 1}_{star_name}.txt"):
                            certain_star_file = open(f"Sector_Files/{count_variable - 1}_{star_name}.txt", "a+")
                        else:
                            certain_star_file = create_file("Sector_Files", count_variable, star_name)
                        certain_star_file.write(section6)

                    elif section6[:1] == " " or section6[:1] == '\t' or section6[:1] == "\n":
                        certain_star_file.write(section6)

                    elif section6[:1] == "[":
                        certain_star_file.write("\n\n")
                        certain_star_file.close()
                        break
                    else:
                        pass
                print("Made it through STAR CHECK")
