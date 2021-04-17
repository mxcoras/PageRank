# import random
# import sqlite3
from time import perf_counter
from multiprocessing import Process
from bin.pagerank import PageRank
from lib.generator import generator


def main():
    N = 1000000
    part_count = 10
    t = perf_counter()
    ps = []
    for i in range(part_count):
        p = Process(target=generator, args=(i*(N//part_count),
                    (i+1)*(N//part_count), N, (N//part_count)))
        ps.append(p)
    for i in range(part_count):
        ps[i].start()
    for i in range(part_count):
        ps[i].join()
    print(f"矩阵生成用时：{perf_counter() - t}秒。")
    myrank = list(enumerate(PageRank(N, N//part_count)))
    myrank.sort(key=lambda x: x[1], reverse=True)
    print("排名\t编号\tPageRank值")
    for i in range(10):
        print(f"{i+1}\t{myrank[i][0]}\t{myrank[i][1]}")


if __name__ == "__main__":
    main()
