import numpy as np

class retime:
    def __init__(self, fn):
        try:
            self._Pr("Path", fn)
            with open(fn) as f:
                self._n = int(f.readline().split()[0])
                n = self._n
                self._t = np.array(f.readline().split(), dtype="float")
                self._M = n * self._t.max()
                self._g = np.empty(n*n).reshape(n,n)
                for i in range(n):
                    self._g[i] = np.array(f.readline().split(), dtype="float")
                self.g = self._M * self._g
                for i in range(n):
                    self.g[i] = self.g[i] - self._t[i]
            self._Pr("G",self._g)
            self._Pr("G\'", self.g)
        except:
            print("Can't open file.")
            raise("Load file error.")

    def Init(self):
        self.CalSuv()
        self.CalW()
        self.CalD()

    def _Pr(self, strIn, obj):
        print(strIn + "=")
        print(obj)
        print()

    def CalG_(self):
        self.g_ = self.g * self._M

    def _ShortestPath(self, g):
        n = g.shape[0]
        for k in range(n):
            for V in range(n):
                for U in range(n):
                    tmp = g[U][k] + g[k][V]
                    if g[U][V] > tmp :
                        g[U][V] = tmp
        for i in range(n):
            if g[i][i] < 0 :
                raise("Shortest path has negtive cycles.")
        return g

    def CalSuv(self):
        self.g = self._ShortestPath(self.g)
        self.Suv = self.g.copy()
        self._Pr("S'uv", self.Suv)

    def CalW(self):
        self.W = np.ceil(self.g/self._M)
        for i in range(self._n):
            self.W[i][i] = 0
        self._Pr("W(U,V)", self.W)

    def CalD(self):
        for row in range(self._n):
            for col in range(self._n):
                if col == row :
                    self.g[row][col] = self._t[col]
                else:
                    tmp = self.W[row][col]
                    self.g[row][col] = self._M*tmp - self.Suv[row][col] + self._t[col]
        self.D = self.g
        self._Pr("D(U,V)", self.D)

    def CalTimeConstrain(self, c):
        self.Cg = self._g.copy()
        c = self.D > c
        tmp = np.minimum(self.Cg, self.W - 1)
        print(tmp)
        print(c)
        for U in range(self._n):
            for V in range(self._n):
                if c[U][V] :
                    self.Cg[U][V] = tmp[U][V]
        self.Cg = self.Cg.transpose()
        exNode = np.zeros(self._n)
        self.Cg = np.vstack((self.Cg, exNode))
        exNode = np.array([np.inf]*(self._n+1)).reshape((self._n+1),1)
        self.Cg = np.hstack((self.Cg,exNode))
        self._Pr("Constrains graph", self.Cg)

    def Retiming_Cg(self):
        self.Result = self._ShortestPath(self.Cg)
        self._Pr("Result", self.Result)

    def Retiming(self):
        self.Result = self._ShortestPath(self._g)
        self._Pr("Result", self.Result)

if __name__ == "__main__" :
    app = retime("graph.txt")
    #app.Init()
    #app.CalTimeConstrain(10)
    #app.Retiming_Cg()
    #app = retime("p2.txt")
    app.Retiming()
