"""
2020/12/16
@Yuya Shimizu

素数を求める
エラトステネスの篩
"""
import math
def get_prime(n):
    if n <= 1:
        return []
    prime = [2]
    limit = int(math.sqrt(n))

    #奇数リストの生成
    data = [i + 1 for i in range(2, n, 2)]
    while limit > data[0]:
        prime.append(data[0])
        data = [j for j in data if j % data[0] != 0]

    return prime + data

prime = get_prime(200)



with open('prime_list.txt', 'w') as f:
    print(*prime, sep='\n',file=f)

