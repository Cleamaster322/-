N = int(input())
ocenki = []
answer =[]
for i in range(N):
    M = int(input())
    tmp = []
    for j in range(M):
        Name,ocenka = input().split()
        tmp.append(int(ocenka))
    ocenki.append(tmp)

for i in ocenki:
    if any([x>1 for x in i]):
        answer.append(1)
    else:
        answer.append(0)

if all(answer):
    print("Yes")
else:
    print('No')

 
