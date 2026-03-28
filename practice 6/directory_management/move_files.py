import shutil

# Move file
shutil.move("sample.txt", "folder/sample.txt")

# Copy file
shutil.copy("folder/sample.txt", "folder/subfolder/sample_copy.txt")