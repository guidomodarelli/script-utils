#!/bin/bash

list=$(ls scripts/)

for file in ${list[@]}; do
	# Get file's name without the extension
	filename="$(echo "$file" | sed -E 's/(.*)\.\w+$/\1/i')"
	# Create a symbolic link to /usr/bin/<filename>
	sudo ln -s "$(realpath scripts/"$file")" /usr/bin/"$filename"
done
