import os

try:
    with open('/mnt/myshare/finaldatabase/finaldatabase/final.db', 'r') as f:
        print("Successfully opened the file!")
except Exception as e:
    print(f"Failed to open the file: {e}")