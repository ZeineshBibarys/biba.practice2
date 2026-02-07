a = int(input())

for _ in range(a):
    b = int(input())
    arr = []

    for _ in range(b):
        arr.append(int(input()))

    found = False

    for i in range(b):
        for j in range(b):
            for k in range(b):
                if arr[i] < arr[j] and arr[j] > arr[k]:
                    print("YES")
                    print(i + 1, j + 1, k + 1)  # +1 если индексы нужны с 1
                    found = True
                    break
            if found:
                break
        if found:
            break

    if not found:
        print("NO")

    