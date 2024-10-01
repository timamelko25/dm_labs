import struct

def LZ78(path):
    with open(path, 'r') as file:
        f = file.read()
    D = ['']
    k = 0
    coded_filename = f"coded_{path.replace('.txt', '.bin')}"
    
    with open(coded_filename, 'wb') as file2:
        while k < len(f):
            p = FD(f, D, k)
            l = len(D[p])
            
            file2.write(struct.pack('I', p)) #
            
            if k + l < len(f):
                file2.write(f[k+l].encode('ascii'))
                D.append(D[p] + f[k+l])


            k += l + 1

def FD(f, D, k):
    l, p = 0, 0
    for i in range(1, len(D)):
        m = len(D[i])
        if f[k:k + m] == D[i]:
            if m > l: 
                l = m
                p = i
    return p

def LZ78_decode(path):
    with open(path, 'rb') as file:
        g = []
        while True:
            bytes_read = file.read(4) #
            if not bytes_read:
                break
            p = struct.unpack('I', bytes_read)[0] #
            q = file.read(1).decode('ascii')
            g.append([p, q])

    D = ['']
    decoded_filename = f"{path.replace('coded', 'decoded').replace('.bin', '.txt')}"
    with open(decoded_filename, 'w') as file2:
        for k in range(len(g)):
            p = g[k][0]
            q = g[k][1]
            file2.write(f"{D[p]}{q}")
            D.append(D[p] + q)

def main():
    while True:
        choice = input("Enter 1 to encode or 2 to decode, or 0 to exit: ")
        if choice == '0':
            break
        path = input("Enter the filename: ")
        if choice == "1":
            LZ78(path)
        elif choice == "2":
            LZ78_decode(path)
        else:
            print("Invalid choice")
    return 0

if __name__ == "__main__":
    main()
