import random


def generator(N: int, step: int) -> list:
    """生成大小为N*N的迁移矩阵，以三元组表示并分块

    Args: 
        N: 转移矩阵尺寸，大于15
        step: 每个分块的大小，必须分为至少两块

    Returns:
        分块的迁移矩阵，返回类型为list。
    
    """
    matrix_num = [i for i in range(N)]  # 用于加速列表推导式
    degree = [random.randint(6, 15) for i in range(N)]
    matrix = [(i, degree[i], sorted(random.sample(matrix_num, degree[i])))
              for i in range(N)]
    """
    没有节点指向自己的情况：
    matrix = []
    for i in range(N):
        matrix_num.remove(i)
        matrix.append((i, degree[i], sorted(random.sample(matrix_num, degree[i]))))
        matrix_num.append(i) 
    """
    part_size = step
    part_num = N // part_size
    part = [[] for i in range(part_num)]
    for m in matrix:
        left = 0
        old_seq = m[2][0] // part_size
        for i in range(len(m[2])):
            new_seq = m[2][i] // part_size
            if old_seq != new_seq:
                new_m = (m[0], m[1], m[2][left:i])
                part[old_seq].append(new_m)
                if new_seq == part_num - 1:
                    new_m = (m[0], m[1], m[2][i:])
                    part[new_seq].append(new_m)
                    break
                else:
                    left = i
                    old_seq = new_seq
    return part
