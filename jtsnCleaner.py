import os, re


def search_dir():

    valid = []

    for dir_path, dir_names, file_names in os.walk("./"):
        for f in file_names:
            file_type = f.split(".")[-1]

            if file_type in ["mkv", "avi", "mp4"]:
                fp = os.path.join(dir_path, f)
                valid.append((f, file_type, fp))

    return valid


def handle_command(command, num):

    if command == "exit":
        exit()
    elif num:
        try:
            int(command)
        except ValueError:
            return True
    elif len(command) < 1:
        return True
    else:
        return False


def await_response(query, num=False):
    handling = True

    while handling:
        response = input(query)
        handling = handle_command(response, num)

    return response


def main():
    user_input = {"name": "", "regex": "", "season": "1"}
    valid_files = search_dir()

    print("Found %i files:" % len(valid_files))

    for file_name, file_type, file_path in valid_files:
        print(file_name)

    print("\nPlease type the name of the series")

    user_input["name"] = await_response("\n(Series name) | exit >> ")

    print("\nWhat season is this?")

    season_num = int(await_response("\n(Season number) | exit >> ", num=True))

    if season_num < 10:
        user_input["season"] = "0%i" % season_num
    else:
        user_input["season"] = "%i" % season_num

    print("\nWhat to look for?")

    trying = True

    while trying:

        user_input["regex"] = await_response("\n(Regex) | exit >> ")

        correction = []
        match_all = True

        for file_name, file_type, file_path in valid_files:
            match = re.match(user_input["regex"], file_name)
            if match:
                new_file_name = user_input["name"] + " S%sE%s.%s" % (user_input["season"], match.group(1), file_type)
                print("%s -> %s" % (file_name, new_file_name))
                correction.append((file_name, new_file_name))
            else:
                print("No match for '%s'" % file_name)
                match_all = False

        if not match_all:
            print("Not all items were matched, please enter new regex")
            continue

        response = input("Does this look right? y|n >> ")

        if response == "y":
            for old_name, new_name in correction:
                os.rename(old_name, new_name)
            print("Done")
            trying = False

if __name__ == '__main__':
    main()