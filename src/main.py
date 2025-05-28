from files_funcs import copy_resources, generate_pages_recursive


def main():
    copy_resources("static", "docs")
    generate_pages_recursive("content", "template.html", "docs")


if __name__ == "__main__":
    main()
