import os

os.makedirs("folder/subfolder/inner", exist_ok=True)
for item in os.listdir("."):
    print(item)
    
for file in os.listdir("."):
    if file.endswith(".txt"):
        print(file)