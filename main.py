from bin.pagerank import PageRank


def main():
    myrank = list(enumerate(PageRank(100000, 100)))
    myrank.sort(key=lambda x: x[1], reverse=True)
    print("排名\t编号\tPageRank值")
    for i in range(10):
        print(f"{i+1}\t{myrank[i][0]}\t{myrank[i][1]}")


if __name__ == "__main__":
    main()
