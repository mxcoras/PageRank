from generator import generator
import math


def error(rank: list, last: list) -> float:
    mysum = 0.0
    for i in range(len(rank)):
        mysum += (rank[i] - last[i])**2
    mysum = math.sqrt(mysum)
    return mysum


def PageRank(N: int, step: int, beta: float, epsilon: float):
    M = generator(N)
    rank = [1/N for i in range(N)]
    while True:
        rnew = [0 for i in range(N)]
        pointer = 0
        for m in M:  # 遍历每个分块
            for line in m:  # 查询该分块的每一行
                for j in range(pointer, pointer+step):  # 查询该分块包含的节点是否包含在该行的dest字段
                    if j in line[2]:
                        rnew[j] += rank[j]/line[1]  # 对r_new进行累加
            pointer += 2
        # r_new乘beta再加(1-beta)/N，防止spider trap
        rnew = list(map(lambda x: x*beta + (1 - beta)/N, rnew))
        if error(rnew, rank) < epsilon:  # 判断收敛条件
            rank = rnew
            break
        rank = rnew  # 更新rank值


"""
稀疏矩阵的数据结构（未分块）
[(src, degree, [dest, ...]),
(src, degree, [dest, ...]),
(src, degree, [dest, ...])]
"""

# PageRank算法demo

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
    (5, 3, [5])
]

M = [M1, M2, M3]
beta = 0.8
N = 6
r = [1/N for i in range(N)]
while True:
    rnew = [0 for i in range(N)]
    step = 0
    for m in M:  # 遍历每个分块
        for line in m:  # 查询该分块的每一行
            for j in range(step, step+2):  # 查询该分块包含的节点是否包含在该行的dest字段
                if j in line[2]:
                    rnew[j] += r[j]/line[1]  # 对r_new进行累加
        step += 2
    # r_new乘beta再加(1-beta)/N，防止spider trap
    rnew = list(map(lambda x: x*beta + (1 - beta)/N, rnew))
    if error(rnew, r) < 0.01:  # 判断收敛条件
        r = rnew
        break
    r = rnew  # 更新rank值
print(r)
