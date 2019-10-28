import numpy as np

class retime:
    def __init__(self, fn):
        try:
            self._Pr("Path", fn)
            with open("graph.txt") as f:
                self._n = int(f.readline().split()[0])
                self._M = int(f.readline().split()[0])
                t = f.readline().split()
                self._t = np.empty(self._n)
                for i in range(self._n):
                    self._t[i] = float(t[i])
                n = self._n
                self.g = np.empty(n*n).reshape(n,n)
                for i in range(self._n):
                    l = f.readline().split()
                    for j in range(self._n):
                        self.g[i][j] = float(l[j])
                self._g = self.g.copy()
            self._Pr("Graph", self.g)
        except:
            print("Can't open file.")
            raise("Load file error.")

    def Run(self):
        self.Suv()
        self.W()
        self.D()

    def _Pr(self, strIn, obj):
        print(strIn + "=")
        print(obj)
        print()

    def Suv(self):
        for k in range(self._n):
            for V in range(self._n):
                for U in range(self._n):
                    tmp = self.g[U][k] + self.g[k][V]
                    if self.g[U][V] > tmp :
                        self.g[U][V] = tmp
        self.Suv = self.g.copy()
        self._Pr("S'uv", self.Suv)

    def W(self):
        self.W = np.ceil(self.g/self._M)
        self._Pr("W(U,V)", self.W)

    def D(self):
        for row in range(self._n):
            for col in range(self._n):
                if col == row :
                    self.g[row][col] = self._t[col]
                else:
                    tmp = self.W[row][col]
                    self.g[row][col] = self._M*tmp - self.Suv[row][col] + float(self._t[col])
        self.D = self.g
        self._Pr("D(U,V)", self.D)

    def TimeConstrain(self, c):


if __name__ == "__main__" :
    app = retime("/home/yanjiun/Desktop/archIC/graph.txt")
    app.Run()
