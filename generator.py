import random


def generator(N: int) -> list:
    """
    生成大小为N*N的迁移矩阵，
    以三元组表示并分块，
    将所有分块使用嵌套列表的方式返回
    """
    matrix_num = [i for i in range(N)]  # 用于加速列表推导式
    XofC = [random.randint(6, 15) for i in range(N)]
    matrix = [(i, XofC[i], sorted(random.sample(matrix_num, XofC[i])))
              for i in range(N)]
    par_siz = 100
    par_num = N // par_siz
    par = [[] for i in range(par_num)]
    for m in matrix:
        left = 0
        old_seq = m[2][0] // par_siz
        for i in range(len(m[2])):
            new_seq = m[2][i] // par_siz
            if old_seq != new_seq:
                new_m = (m[0], m[1], m[2][left:i])
                par[old_seq].append(new_m)
                if new_seq == par_num - 1:
                    new_m = (m[0], m[1], m[2][i:])
                    par[new_seq].append(new_m)
                    break
                else:
                    left = i
                    old_seq = new_seq
    return par
