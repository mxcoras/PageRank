# PageRank

PageRank算法的Python实现

# 单机版说明：
首先因为只允许使用Python标准库的原因，numpy包是不能使用的，我们对矩阵乘法进行了封装，具体实现在matrix.py当中，我们实现了矩阵与矩阵乘法与数字与矩阵乘法，之后的算法实现就可以使用这几个封装函数`def __mul__(self, B)`和`def __rmul__(self, B)`来进行矩阵计算。
generator.py是生成迁移矩阵并将其表示成三元组的形式，具体实现如下：
```
    matrix_num = [i for i in range(N)]  # 用于加速列表推导式
    degree = [random.randint(6, 15) for i in range(N)]
    matrix = [(i, degree[i], sorted(random.sample(matrix_num, degree[i])))
              for i in range(N)]
```
这个部分是生成了生成了一个N*N大小的伴随矩阵，然后伴随矩阵中的节点的度是在6-15中随机取一个整数，作为对应网页的出度，生成迁移矩阵之后进行将迁移矩阵转化成三元组的工作。
```
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
```
这个部分是将之前生成的伴随矩阵转化成格式为[[(src, degree, [dest, ...]), ...], ...]的三元组，以节省内存空间。在文件的最后有伴随矩阵及其三元组的大小的对比。
接下来就是使用pagerank算法计算rank vector
这个迭代的过程在满足|r(t+1) – r(t)|<sub>2</sub><e，其中e为我们设置的收敛标准epsilon，这里的二范数即为求两个vector的差的模，具体判断函数为：
```
def error(rank: list, last: list) -> float:
    """计算r_new与r_old差的模，即停止条件"""
    mysum = sum(list(map(lambda x: (x[0]-x[1])**2, zip(rank, last))))
    mysum = math.sqrt(mysum)
    return mysum
```
迭代过程见pagerank函数：
```
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
    M = generator(N, step)
    t = perf_counter()
    rank = [1/N for i in range(N)]
    iterations = 0
    while True:
        rnew = [0 for i in range(N)]
        pointer = 0
        for m in M:  # 遍历每个分块
            for line in m:  # 查询该分块的每一行
                for j in line[2]:  # 遍历每行dest字段包含的节点
                    rnew[j] += rank[line[0]]/line[1]  # 对r_new进行累加
            pointer += step
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
```
需要注意的是，为了防止出现spider trap,需要设置一个1-beta的随机跳转概率
运行main.py文件之后可以得到结果
