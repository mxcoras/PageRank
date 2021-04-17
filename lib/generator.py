import sqlite3
import random
from time import perf_counter


def generator(L: int, R: int, N: int, part_size: int):
    """生成大小为N*N的迁移矩阵，以三元组表示并分块

    Args:
        L: 生成起始位置
        R: 生成结束位置
        N: 转移矩阵尺寸，大于15
        part_size: 每个分块的大小，必须分为至少两块

    Returns:
        分块的迁移矩阵，返回类型为list
        格式为[[(src, degree, [dest, ...]), ...], ...]
    
    """
    table = L // part_size
    t = perf_counter()
    # conn = mysql.connector.connect(user='root', password='123456', database='generator')
    conn = sqlite3.connect(f"db/generator{table}.db")
    c = conn.cursor()
    c.execute(f"""create table part
                (part_num int not null,
                src int not null,
                degree int not null,
                dest text not null,
                primary key(part_num, src));""")
    conn.commit()
    # matrix_num = [i for i in range(N)]  # 用于加速列表推导式
    # degree = [random.randint(6, 15) for i in range(N)]
    part_num = N // part_size
    # conn2 = sqlite3.connect(f"db/degree{table}.db")
    # c2 = conn2.cursor()
    for k in range(L, R):
        # if k % 1000000 == 0:
        #     print(k)
        # degree = c2.execute(f"select deg from degree where id = {k}").fetchone()[0]
        numbers = []
        degree = random.randint(6, 15)
        for i in range(degree):
            num = -1
            while num in numbers or num == -1:
                num = random.randrange(0, N)
            numbers.append(num)
        m = (k, degree, sorted(numbers))
        left = 0
        old_seq = m[2][0] // part_size
        for i in range(len(m[2])):
            new_seq = m[2][i] // part_size
            if old_seq != new_seq:
                c.execute(f"insert into part (part_num, src, degree, dest) \
                    values ({old_seq}, {m[0]}, {m[1]}, '{m[2][left:i]}')")
                if new_seq == part_num - 1:
                    c.execute(f"insert into part (part_num, src, degree, dest) \
                        values ({new_seq}, {m[0]}, {m[1]}, '{m[2][i:]}')")
                    break
                else:
                    left = i
                    old_seq = new_seq
    conn.commit()
    conn.close()
    # print(f"矩阵生成用时：{perf_counter() - t}秒。")
    # print(f"原始稀疏矩阵占用内存：{sys.getsizeof(matrix)/1024}KB")
    # print(f"三元组分块表示的稀疏矩阵占用内存：{sys.getsizeof(part)/1024}KB")
