import sqlite3
from bin.pagerank import PageRank


def main():
    conn = sqlite3.connect("C:/Users/MxCorAS/Documents/DB/generator.db")
    c = conn.cursor()
    c.execute(f"""create table part
                (part_num int not null,
                src int not null,
                degree int not null,
                dest text default '[]' not null,
                primary key(part_num, src));""")
    conn.commit()
    conn.close()
    myrank = list(enumerate(PageRank(10000000, 10000)))
    myrank.sort(key=lambda x: x[1], reverse=True)
    print("排名\t编号\tPageRank值")
    for i in range(10):
        print(f"{i+1}\t{myrank[i][0]}\t{myrank[i][1]}")


if __name__ == "__main__":
    main()
