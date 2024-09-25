def LZ78(f, file):
    D = ['']
    d = 0
    k = 1
    while k <= len(f):
        p = FD(f, D, k)
        l = len(D[p])
        file.write(f"{p} {f[k+l-1]} ")
        d = d + 1
        D.append(D[p] + f[k+l-1])
        k = k + l + 1

def FD(f, D, k):
    l, p = 0, 0
    for i in range(0,len(D)):
        m = len(D[i])
        if D[i] == f[k+m-2] and m > l:
            p = i
            l = m
    return p

def LZ78_decode(g, file):
    D = ['']
    d = 0
    for k in range(0, len(g)):
        p = int(g[k][0])
        q = g[k][1]
        file.write(f"{D[p]}{q}")
        d = d + 1
        D.append(D[p] + q)

def main():
    number = 1
    path = f"{number}.txt"
    path2 = f"output{number}.txt"
    path3 = f"decode{number}.txt"
    
    file = open(path, 'r')
    file2 = open(path2, 'w')
    f = file.read()

    LZ78(list(f), file2)
    file.close()
    file2.close()
    
    file2 = open(path2, 'r')
    file3 = open(path3, 'w')
    
    tmp = file2.read().split()
    g = []
    for i in range(0, len(tmp)-1, 2):
        g.append([tmp[i], tmp[i+1] if i + 1 < len(tmp) else ''] )
    print(g)
    #LZ78_decode(g, file3)

    file.close()
    file2.close()
    return 0

if __name__ == "__main__":
    main()