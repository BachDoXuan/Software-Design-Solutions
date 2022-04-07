import time

l = []
t1 = time.time()
for i in range(1000000):
    l.append(i)
t2 = time.time()
print(t2 - t1)

t1 = time.time()
for i in range(1000000):
    l.pop()
t2 = time.time()
print(t2 - t1)