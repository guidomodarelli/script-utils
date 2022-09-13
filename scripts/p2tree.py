#!/bin/python3

import sys


def paths_to_dict(paths: list):
    root = {}

    for path in paths:
        # separate by slashes, disregarding the first `/`
        path = path.lstrip("/").split("/")
        # pop off the last key-value component
        key, _, val = path.pop(-1).partition("=")
        # find the target dict starting from the root
        target_dict = root
        is_dict = True
        for component in path:
            if not isinstance(target_dict, dict):
                is_dict = False
                break
            target_dict = target_dict.setdefault(component, {})
        if is_dict:
            # assign key-value
            target_dict[key] = val

    return root


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
    args = sys.argv[1:]
    if len(args) == 0:
        print("No args passed")
        sys.exit(1)

    for arg in args:
        list.append(arg)

    result = paths_to_dict(list)
    for line in tree(result):
        print(line)
