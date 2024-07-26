#!/bin/bash

# List the contents of the /mnt/myshare directory
ls /mnt/myshare/finaldatabase

# Set the permissions of the /mnt/myshare/finaldatabase/finaldatabase/final.db file
chmod 755 /mnt/myshare/finaldatabase/finaldatabase/final.db

# Run app.py changed to see if can verify mounting
python check_file.py
python app.py