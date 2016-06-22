Followme
========

Stupid script to display a tree listing of files and directories,
while watching some specified process and highlighting its current
working directory.

Use as:
  urxvt -e python3 /path/to/followme.py . -p $$  &

urxvt can be replaced with xterm, konsole, gnome-terminal…

This will open up a window and follow your current shell as you change
into subdirectories and create or remove files and directories.

Installation
============

No installation is required, but strace and inotifywait need to be
installed. Install strace and inotify-tools packages if they are missing.

License
=======

The contents of this directory are available under the MIT license.
