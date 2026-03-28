with open("sample.txt", "a") as f:
    f.write("Appended line 1\n")
    f.write("Appended line 2\n")

with open("sample.txt", "r") as f:
    print(f.read())