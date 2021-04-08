def PageRank():
    # TODO
    pass

class Matrix:
    """
    封装了矩阵乘法，包括矩阵乘矩阵，数乘矩阵
    """
    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col
        self.A = [[0 for i in range(col)] for j in range(row)]

    def value(self, value:list):
        if len(value) == self.row and len(value[0]) == self.col:
            self.A = value

    def __getitem__(self, i):
        return self.A[i]

    def __mul__(self, B):
        """
        重载乘法运算符，用于矩阵乘矩阵
        """
        if self.col != B.row:
            return Matrix(1, 1)
        C = Matrix(self.row, B.col)
        for i in range(C.row):
            for j in range(C.col):
                for p in range(B.row):
                    C[i][j] += self.A[i][p] * B[p][j]
        return C

    def __rmul__(self, B):
        """
        反向重载乘法运算符，用于数乘矩阵
        """
        for i in range(self.row):
            self.A[i] = list(map(lambda x: x*B, self.A[i]))
        return self

    def print(self):
        print(self.A)

"""
使用示例
A = Matrix(4, 3)
B = Matrix(3, 2)
A1 = [[5, 2, 4], [3, 8, 2], [6, 0, 4], [0, 1, 6]]
B1 = [[2, 4], [1, 3], [3, 2]]
A.value(A1)
B.value(B1)
C = A*B
C.print()
D = 2*A
D.print()
"""

"""
稀疏矩阵的数据结构（未分块）
[(src, degree, [dest, ...]),
(src, degree, [dest, ...]),
(src, degree, [dest, ...])]
"""
import math

def error(rank:list, last:list)->float:
    mysum = 0.0
    for i in range(len(rank)):
        mysum += (rank[i] - last[i])**2
    mysum = math.sqrt(mysum)
    print(1)
    return mysum

M1 = [
    (0, 4, [0, 1]),
    (1, 2, [0]),
    (3, 6, [0, 1]),
    (4, 2, [1]),
    (5, 3, [1])
]

M2 = [
    (0, 4, [3]),
    (2, 2, [3]),
    (3, 6, [2, 3]),
    (5, 3, [2])
]

M3 = [
    (0, 4, [5]),
    (1, 2, [5]),
    (2, 2, [4]),
    (3, 6, [4, 5]),
    (4, 2, [5]),
    (5, 3, [4])
]

M = [M1, M2, M3]
beta = 0.8
N = 6
r = [1/N for i in range(N)]
while True:
    rnew = [0 for i in range(N)]
    step = 0
    for m in M: # 遍历每个分块
        for line in m: # 查询该分块的每一行
            for j in range(step, step+1): # 查询该分块包含的节点是否包含在该行的dest字段
                if j in line[2]:
                    rnew[j] += r[j]/line[1] # 对r_new进行累加
        step += 2
    rnew = list(map(lambda x: x*beta + (1 - beta)/N, rnew)) # r_new乘beta再加(1-beta)/N，防止spider trap
    if error(rnew, r) < 0.01: # 判断收敛条件
        r = rnew
        break
    r = rnew # 更新rank值
print(r)