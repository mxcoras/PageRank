# PageRank

PageRank算法的Python实现
# 使用数据库实现PageRank算法
这个部分的大体思路和之前的非数据库版本的差不多，主要区别在于处理网页数据的时候，由于存在硬盘的读写使用了python自带的sqlite数据库，以减少内存的消耗，同时在效率上没有非常大的损失。根据测试，使用sqlite可以减少90%以上的内存消耗，这在大数据量下是非常有意义的。
主要的区别就是在操作转移矩阵的时候涉及到了数据库的操作
```
 conn = sqlite3.connect("generator.db")
    c = conn.cursor()
    c.execute("""create table matrix
                (src int primary key not null,
                degree int not null,
                dest text not null
                );""")
```
这个部分创建了一个名为generator.db的数据库文件，然后新建了一个一个以源网页src为主键的表，格式为src:int degree:int dest:text
dest本来预期使用json格式来方便处理，但是在sqlite当中并没有这个数据类型，于是使用了text类型来存储dest数据，最终迁移矩阵的格式为[[(src, degree, [dest, ...]), ...], ...]
```
    for i in range(N):
        c.execute(f"insert into matrix (src, degree, dest) \
            values ({i}, {degree[i]}, '{sorted(random.sample(matrix_num, degree[i]))}')")
    # matrix = [(i, degree[i], sorted(random.sample(matrix_num, degree[i])))
    #           for i in range(N)]
```
和非数据库版本主要区别在于
```
        c.execute(f"insert into matrix (src, degree, dest) \
            values ({i}, {degree[i]}, '{sorted(random.sample(matrix_num, degree[i]))}')")
```
这个是在数据库中对matrix进行操作
```
    part_size = step
    part_num = N // part_size
    # part = [[] for i in range(part_num)]
    c.execute(f"""create table part
                (part_num int not null,
                src int not null,
                degree int not null,
                dest text default '[]' not null,
                primary key(part_num, src));""")
    for k in range(N):
        query = c.execute(f"select src, degree, dest from matrix where src = {k}").fetchone()
        m = (query[0], query[1], eval(query[2]))
        left = 0
        old_seq = m[2][0] // part_size
        for i in range(len(m[2])):
            new_seq = m[2][i] // part_size
            if old_seq != new_seq:
                # new_m = (m[0], m[1], m[2][left:i])
                # part[old_seq].append(new_m)
                query = c.execute(f"insert into part (part_num, src, degree, dest) \
                    values ({old_seq}, {m[0]}, {m[1]}, '{m[2][left:i]}')")
                if new_seq == part_num - 1:
                    # new_m = (m[0], m[1], m[2][i:])
                    # part[new_seq].append(new_m)
                    query = c.execute(f"insert into part (part_num, src, degree, dest) \
                        values ({new_seq}, {m[0]}, {m[1]}, '{m[2][i:]}')")
                    break
                else:
                    left = i
                    old_seq = new_seq
    conn.commit()
    conn.close()
```
这部分都是将原来的对矩阵的操作语句换成了数据库操作语句
pagerank.py中主要的区别在于这一句：
```
            m = c.execute(f"select src, degree, dest from part \
                        where part_num = {i}").fetchall()
```
这里是将符合partnum={i}这一条件的元组挑选出来
其他的大体上与非数据库版本相同