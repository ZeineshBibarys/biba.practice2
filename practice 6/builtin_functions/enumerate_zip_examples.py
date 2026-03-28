names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 95]

# enumerate
for index, name in enumerate(names):
    print(index, name)

# zip
for name, score in zip(names, scores):
    print(name, score)

value = "123"

# Type checking
if isinstance(value, str):
    print("It is a string")

# Conversion
num = int(value)
print(num + 10)

# More examples
print(float("3.14"))
print(str(100))