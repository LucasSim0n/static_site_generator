import os
import shutil

from block_funcs import extract_title, markdown_to_html_node


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


def copy_resources(from_path, dest_path):
    shutil.rmtree(dest_path, ignore_errors=True)
    os.mkdir(dest_path)
    files = get_nested_files(from_path)
    dirs = get_nested_dirs(from_path)

    for dir in dirs:
        new_dir = dir.replace(from_path, dest_path)
        os.mkdir(new_dir)

    for file in files:
        new_file = file.replace(from_path, dest_path)
        shutil.copy(file, new_file)


def generate_page(from_path, template_path, dest_path):
    print(f"generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        source = f.read()
    with open(template_path, "r") as t:
        template = t.read()

    content = markdown_to_html_node(source).to_html()
    title = extract_title(source)

    page = template.replace("{{ Title }}", title).replace("{{ Content }}", content)

    with open(dest_path, "w") as dest:
        dest.write(page)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    for dir in get_nested_dirs(dir_path_content):
        new_dir = dir.replace(dir_path_content, dest_dir_path)
        os.mkdir(new_dir)

    for file in get_nested_files(dir_path_content):
        print(file)
        if file[-3:] == ".md":
            target = file.replace(dir_path_content, dest_dir_path)
            generate_page(file, template_path, f"{target[:-3]}.html")
