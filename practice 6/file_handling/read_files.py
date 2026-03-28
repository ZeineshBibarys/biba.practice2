with open("sample.txt", "w") as f:
    f.write("Hello, this is line 1\n")
    f.write("This is line 2\n")
    f.write("Python file handling practice\n")

with open("sample.txt", "r") as f:
    content = f.read()
    print(content)