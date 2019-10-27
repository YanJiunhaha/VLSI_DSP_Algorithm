import numpy as np

with open("graph.txt") as f:
    n = int(f.readline().split()[0])
    M = int(f.readline().split()[0])
    t = f.readline().split()
    g = np.empty(n*n).reshape(n,n)
    for i in range(n):
        l = f.readline().split()
        for j in range(n):
            g[i][j] = float(l[j])
    for k in range(n):
        for V in range(n):
            for U in range(n):
                tmp = g[U][k] + g[k][V]
                if g[U][V] > tmp :
                    g[U][V] = tmp
    Suv = g.copy()
    print("S'uv")
    print(Suv)
    W = np.ceil(g/M)
    print("W(U,V)")
    print(W)

    #t = [1, 1, 2, 2, 0]
    for row in range(n):
        for col in range(n):
            if col == row :
                g[row][col] = float(t[col])
            else:
                tmp = W[row][col]
                g[row][col] = M*tmp - Suv[row][col] + float(t[col])
    D = g
    print("D(U,V)")
    print(D)
