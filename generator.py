from random import randint

def generator(N:int) -> list:
    """
    生成大小为N*N的迁移矩阵，以嵌套列表的方式返回
    注意不能使用numpy
    """
    # TODO
    pass

import random

N = eval(input("请输入行数(行数不得少于15)： "))

matrix = []
for i in range(N):
    matrix.append(0)

#查阅过资料，random库中的随机数分布就是均匀分布

XofC = random.randint(6,15)
print("随机数d为：{}".format(XofC))

matrix_num = []
for j in range(N):
    matrix_num.append(j)

rand = random.sample(matrix_num,XofC)

for k in rand:
    matrix[k]=(1/XofC)

print(matrix)
