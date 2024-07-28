#!/bin/bash

echo "All project files"
echo "Timestamp: $(date "+%Y-%m-%d %H:%M:%S")"

file_list() {
    find . -type f -not -path '*/\.*' | grep -v '\.\(pyc\|git\|gitignore\)$' | sort
}

echo "File index:"
echo "----------------------------------------"
file_list
echo
echo

echo "Git status:"
echo "----------------------------------------"
git status
echo
echo

echo "Staged commits:"
echo "----------------------------------------"
git diff --cached
echo
echo

echo "Unstaged changes:"
echo "----------------------------------------"
git diff
echo
echo

echo "Last 10 git log entries:"
echo "----------------------------------------"
git log -n 10 --pretty=format:"%h - %an, %ar : %s"
echo
echo

echo "Running tests:"
echo "----------------------------------------"
test_output=$(python -m doctest *.py 2>&1)
test_exit_code=$?
echo "Test exit code: $test_exit_code"
echo
echo "Test output:"
echo $test_output
echo
echo

file_list | while read -r file; do
    echo "File: $file"
    echo "----------------------------------------"
    cat "$file" 2>/dev/null || echo "Unable to read file"
    echo "<EOF>"
    echo
done