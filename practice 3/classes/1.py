m=list(map(int,input().split()))
sum=0
for i in m:
    sum+=i
counter=0
for i in m:
    if i>sum/len(m):
        counter+=1
print(counter)