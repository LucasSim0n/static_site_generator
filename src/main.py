import sys

from files_funcs import copy_resources, generate_pages_recursive


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_resources("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()
