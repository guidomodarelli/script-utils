#!/bin/bash

get_root() {
	if [ "$#" -eq 0 ]; then
		echo .
	else
		echo "$1"
	fi
}

find_git_repo() {
	local path="$1"

	echo "$(find "$path" -name HEAD -execdir test -e refs -a -e objects \; -printf %h\\n | grep -v .git/modules | xargs dirname | sort)"
}

root="$(get_root $1)"

paths="$(find_git_repo "$root")"

for path in "${paths[@]}"; do
	echo "$path"
	# TODO: List directory tree structure from a list of path file
	# TODO: https://stackoverflow.com/a/72621581
done
