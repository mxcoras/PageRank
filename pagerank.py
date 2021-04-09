from generator import generator
import math


def error(rank: list, last: list) -> float:
    """计算r_new与r_old差的模，即停止条件"""
    mysum = 0.0
    for i in range(len(rank)):
        mysum += (rank[i] - last[i])**2
    mysum = math.sqrt(mysum)
    return mysum


def PageRank(N: int, step: int, beta=0.8, epsilon=0.01) -> list:
    """PageRank算法

    Args:
        N: 转移矩阵尺寸，大于15
        step: 每个分块的大小，必须分为至少两块
        beta: beta值，0.8<=beta<=0.9，默认为0.8
        epsilon: 收敛标准，默认为0.01

    Returns:
        迭代到收敛标准时的PageRank值，返回类型为list。

    """
    M = generator(N, step)
    rank = [1/N for i in range(N)]
    while True:
        rnew = [0 for i in range(N)]
        pointer = 0
        for m in M:  # 遍历每个分块
            for line in m:  # 查询该分块的每一行
                for j in range(pointer, pointer + step):  # 查询该分块包含的节点是否包含在该行的dest字段
                    if j in line[2]:
                        rnew[j] += rank[line[0]]/line[1]  # 对r_new进行累加
            pointer += step
        # r_new乘beta再加(1-beta)/N，防止spider trap
        rnew = list(map(lambda x: x*beta + (1 - beta)/N, rnew))
        if error(rnew, rank) < epsilon:  # 判断收敛条件
            rank = rnew
            break
        rank = rnew  # 更新rank值
    return rank


if __name__ == "__main__":
    myrank = PageRank(1000, 100, 0.8, 0.01)
