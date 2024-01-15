s = [3, 4]


def lol(s):
    for i in range(2):
        del s[0]
    print(s, 1)

lol(s)
print(s, 1)