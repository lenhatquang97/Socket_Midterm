import re 
arr=re.sub(' +', ' ', 'Maple    12                      3704       2').split(' ')
#Count thread
print(arr[len(arr)-1])
#ProcessID
print(arr[len(arr)-2])
#First
chain=''
for i in range(0,len(arr)-2,1):
    chain+=arr[i]
print(chain)