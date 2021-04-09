import random


def generator(N: int) -> list:
    """
    生成大小为N*N的迁移矩阵，以嵌套列表的方式返回
    注意不能使用numpy
    """
    matrix_num = [i for i in range(N)] # 用于加速列表推导式
    XofC = [random.randint(6, 15) for i in range(N)]
    matrix = [(i, XofC[i], random.sample(matrix_num, XofC[i]))
              for i in range(N)]
    # TODO
    # 将matrix分块，以一个列表的形式返回
    # return [M1, M2, M3, ...]


"""
生成原始矩阵

N = eval(input("请输入行数(行数不得少于15)： "))

matrix = [0 for i in range(N)]

# 查阅过资料，random库中的随机数分布就是均匀分布

XofC = random.randint(6, 15)
print("随机数d为：{}".format(XofC))

matrix_num = []
for j in range(N):
    matrix_num.append(j)

rand = random.sample(matrix_num, XofC)

for k in rand:
    matrix[k] = (1/XofC)

print(matrix)
"""
