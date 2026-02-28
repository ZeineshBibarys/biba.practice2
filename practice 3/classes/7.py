s=input()
words=s.split()
mx_len=0
mx_word=''
for word in words:
    if len(word)>mx_len:
        mx_len=len(word)
        mx_word=word
print(mx_word)