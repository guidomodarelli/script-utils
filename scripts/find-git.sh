#!/bin/bash

get_root() {
	if [ "$#" -eq 0 ]; then
		echo .
	else
		echo "$1"
	fi
}

root="$(get_root $1)"

find "$root" -name HEAD -execdir [ -e refs -a -e objects ] \; -printf "%h\n" | grep "/\.git$" | xargs dirname
