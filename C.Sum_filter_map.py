a = [i for i in range(10,100)]
a = filter(lambda x: x%9 == 0,a)
a = sum(map(lambda x:x**2,a))
print(a)

print(sum(map(lambda x:x**2,filter(lambda x: x%9 == 0,[i for i in range(10,100)]))))