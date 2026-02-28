a=int(input())
arr=list(map(int,input().split()))
b=sum(arr)/a
d=0
for i in arr:
    if i>b:
        d+=1
print(d)