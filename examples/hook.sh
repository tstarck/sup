#!/bin/sh

# Example of a useless upload hook for sup. When used, this hook
# will remove all the uploaded files as they are uploaded.

# Hook script is called with upload directory and uploaded file
# name as arguments.

cd $1
rm -f $2
