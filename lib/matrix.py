class Matrix:
    """封装了矩阵乘法，包括矩阵乘矩阵，数乘矩阵
    使用示例：

    >>> A = Matrix(4, 3)
    >>> B = Matrix(3, 2)
    >>> A1 = [[5, 2, 4], [3, 8, 2], [6, 0, 4], [0, 1, 6]]
    >>> B1 = [[2, 4], [1, 3], [3, 2]]
    >>> A.value(A1)
    >>> B.value(B1)
    >>> C = A*B
    >>> C.print()
    >>> D = 2*A
    >>> D.print()

    """

    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col
        self.A = [[0 for i in range(col)] for j in range(row)]

    def value(self, value: list):
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
