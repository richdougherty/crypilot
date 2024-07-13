#!/bin/bash

echo "All project files"
echo "Timestamp: $(date "+%Y-%m-%d %H:%M:%S")"

file_list() {
    find . -type f -not -path '*/\.*' | grep -v '\.\(pyc\|git\|gitignore\)$' | sort
}

echo "File index:"
file_list
echo
echo

file_list | while read -r file; do
    echo "File: $file"
    echo "----------------------------------------"
    cat "$file" 2>/dev/null || echo "Unable to read file"
    echo "<EOF>"
    echo
done