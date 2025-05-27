import os
import shutil


def get_nested_files(path):
    files = []
    for element in os.listdir(path):
        next_path = f"{path}/{element}"
        if os.path.isfile(next_path):
            files.append(next_path)
        else:
            files.extend(get_nested_files(next_path))
    return files


def get_nested_dirs(path):
    dirs = []
    for element in os.listdir(path):
        next_path = f"{path}/{element}"
        if os.path.isfile(next_path):
            continue

        dirs.append(next_path)
        dirs.extend(get_nested_dirs(next_path))
    return dirs


def copy_resources():
    shutil.rmtree("public", ignore_errors=True)
    os.mkdir("public")
    files = get_nested_files("static")
    dirs = get_nested_dirs("static")

    for dir in dirs:
        new_dir = dir.replace("static", "public")
        os.mkdir(new_dir)

    for file in files:
        new_file = file.replace("static", "public")
        shutil.copy(file, new_file)


def main():
    copy_resources()


if __name__ == "__main__":
    main()
