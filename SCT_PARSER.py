import os



try:
    os.mkdir("Sector_Files")
except FileExistsError:
    pass


def create_file(dir, count, file_name):
    global count_variable
    count_variable += 1
    f = open(f"{dir}/{count}_{file_name}.txt", "w")
    return f


count_variable = 10000
with open("ZLC_SECTOR.SCT2", "r") as file:
    all_lines = file.readlines()
    current_line = -1
    next_line = 0

    for lines in all_lines:
        current_line += 1
        next_line += 1
        for character in lines[:7]:
            if character[:1] == "#":
                # put all of these in a file.
                if os.path.exists(f"Sector_Files/{count_variable-1}_Colors.txt"):
                    color_file = open(f"Sector_Files/{count_variable-1}_Colors.txt", "a+")
                else:
                    #input("<<<<<want to create new file>>>>>>")
                    color_file = create_file("Sector_Files", count_variable, "Colors")
                color_file.write(lines)
                color_file.close()

            if character[:1] == "[":
                if os.path.exists(f"Sector_Files/{count_variable - 1}_{lines[:]}.txt"):
                    bracket_file = open(f"Sector_Files/{count_variable - 1}_{lines[:]}.txt", "a+")
                else:
                    #input("<<<<<want to create new file>>>>>>")
                    bracket_file = create_file("Sector_Files", count_variable, str(lines[:-1]))
                bracket_file.write(lines)
                for section in all_lines[current_line+1:]:
                    if section[:1] == "[":
                        bracket_file.write("\n")
                        bracket_file.close()
                        #input("<<<<FOUND NEW BRACKET>>>>")
                        break
                    bracket_file.write(section)
                if character[:5] == "[SID]":
                    input("HEY YOU MADE IT TO THE SIDS")
















