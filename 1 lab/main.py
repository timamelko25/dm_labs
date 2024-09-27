import re

def LZ78(path):
    file = open(path, 'r')
    file2 = open(f"coded_{path}", 'w')
    f = file.read()
    f = list(f)
    D = ['']
    d = 0
    k = 1
    while k < len(f):
        p = FD(f, D, k)
        l = len(D[p])
        file2.write(f"{p}{f[k+l-1]}")
        d = d + 1
        D.append(D[p] + f[k+l-1])
        k = k + l + 1
    file.close()
    file2.close()

def FD(f, D, k):
    l, p = 0, 0
    for i in range(0,len(D)):
        m = len(D[i])
        if D[i] == f[k+m-2] and m > l:
            p = i
            l = m
    return p

def LZ78_decode(path):
    file = open(path, 'r')
    file2 = open(f"decoded_{path}", 'w')
    tmp = []
    pattern = r'\d+|[A-Za-z]|[ \n]|[-.,—!?:;"]'
    for char in file:
        matches = re.findall(pattern, char)
        tmp.extend(matches)
        
    g = []
    for i in range(0, len(tmp)-1, 2):
        g.append([tmp[i], tmp[i+1]])
    D = ['']
    d = 0
    for k in range(0, len(g)):
        p = int(g[k][0])
        q = g[k][1]
        file2.write(f"{D[p]}{q}")
        d = d + 1
        D.append(D[p] + q)
    file.close()
    file2.close()


def main():
    while True:
        path = input("Enter the filename: ")
        choice = input("Enter 1 to encode or 2 to decode, or 0 to exit: ")
        if choice == '0':
            break
        elif choice == "1":
            LZ78(path)
        elif choice == "2":
            LZ78_decode(path)
    return 0

if __name__ == "__main__":
    main()