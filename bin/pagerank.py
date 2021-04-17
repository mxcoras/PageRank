# from lib.generator import generator
from time import perf_counter
import sqlite3
import math


def error(rank: list, last: list) -> float:
    """计算r_new与r_old差的模，即停止条件"""
    mysum = sum(list(map(lambda x: (x[0]-x[1])**2, zip(rank, last))))
    mysum = math.sqrt(mysum)
    return mysum


def PageRank(N: int, step: int, beta=0.8, epsilon=10e-8) -> list:
    """PageRank算法

    Args:
        N: 转移矩阵尺寸，大于15
        step: 每个分块的大小，必须分为至少两块
        beta: beta值，0.8<=beta<=0.9，默认为0.8
        epsilon: 收敛标准，默认为0.01

    Returns:
        迭代到收敛标准时的PageRank值，返回类型为list。

    """
    t = perf_counter()
    rank = [1/N for i in range(N)]
    iterations = 0
    while True:
        rnew = [0 for i in range(N)]
        for i in range(N//step):
            conn = sqlite3.connect(f'db/generator{i}.db')
            c = conn.cursor()
            m = c.execute(f"select src, degree, dest from part").fetchall()
            for line in m:  # 查询该分块的每一行
                for j in list(map(lambda x: int(x), line[2][1:-1].split(', '))):  # 遍历每行dest字段包含的节点
                    rnew[j] += rank[line[0]]/line[1]  # 对r_new进行累加
            conn.close()
        # r_new乘beta再加(1-beta)/N，防止spider trap
        rnew = list(map(lambda x: x*beta + (1 - beta)/N, rnew))
        iterations += 1
        if error(rnew, rank) < epsilon:  # 判断收敛条件
            rank = rnew
            break
        rank = rnew  # 更新rank值
    print(f"迭代完成，共迭代{iterations}次。")
    print(f"PageRank算法用时：{perf_counter() - t}秒。")
    return rank
