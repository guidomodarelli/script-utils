#!/bin/python3

import sys
from collections import defaultdict


def nested_dict():
    """
    Creates a default dictionary where each value is an other default
    dictionary.
    """
    return defaultdict(nested_dict)


def default_to_regular(d: dict):
    """
    Converts defaultdicts of defaultdicts to dict of dicts.
    """
    if isinstance(d, defaultdict):
        d = {k: default_to_regular(v) for k, v in d.items()}
    return d


def get_path_dict(paths: list):
    new_path_dict = nested_dict()
    for path in paths:
        if str.startswith(path, "/"):
            path = str.removeprefix(path, "/")
        parts = path.split("/")
        if parts:
            marcher = new_path_dict
            for key in parts[:-1]:
                marcher = marcher[key]
            marcher[parts[-1]] = parts[-1]
    return default_to_regular(new_path_dict)


# prefix components:
space = "    "
branch = "│   "
# pointers:
tee = "├── "
last = "└── "


def tree(paths: dict, prefix: str = "", first: bool = True):
    """A recursive generator, given a directory Path object
    will yield a visual tree structure line by line
    with each line prefixed by the same characters
    """
    # contents each get pointers that are ├── with a final └── :
    pointers = [tee] * (len(paths) - 1) + [last]
    for pointer, path in zip(pointers, paths):
        if first:
            yield prefix + path
        else:
            yield prefix + pointer + path
        if isinstance(paths[path], dict):  # extend the prefix and recurse:
            if first:
                extension = ""
            else:
                extension = branch if pointer == tee else space
                # i.e. space because last, └── , above so no more │
            yield from tree(paths[path], prefix=prefix + extension, first=False)


if __name__ == "__main__":
    list = []
    for arg in sys.argv[1:]:
        list.append(arg)

    result = get_path_dict(list)
    for line in tree(result):
        print(line)
