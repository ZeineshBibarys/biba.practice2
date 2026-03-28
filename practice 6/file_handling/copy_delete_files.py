import shutil
import os

# Copy file
shutil.copy("sample.txt", "copy_sample.txt")

# Backup file
shutil.copy("sample.txt", "sample_backup.txt")

filename = "copy_sample.txt"

if os.path.exists(filename):
    os.remove(filename)
    print("File deleted")
else:
    print("File not found")