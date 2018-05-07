# -*- coding: utf-8 -*-


MOD = int(1e9 + 7)


class Matrix:
    def __init__(self, x, y):
        self.row = x
        self.col = y
        self.ite = [[0 for j in range(y)] for i in range(x)]

    def normalize(self):
        if self.row != self.col:
            return False
        for i in range(self.row):
            self.ite[i][i] = 1
        return True


def matrix_multi(x, y):
    z = Matrix(x.row, y.col)
    for i in range(x.row):
        for k in range(x.col):
            if x.ite[i][k] == 0:
                continue
            else:
                pass
            for j in range(y.col):
                z.ite[i][j] = (z.ite[i][j] + x.ite[i][k] * y.ite[k][j]) % MOD

    return z


def fast_power(x, n):
    answer = Matrix(x.row, x.col)
    if answer.normalize() is False:
        print('error')
        exit(0)
    while n > 0:
        if n & 1:
            answer = matrix_multi(answer, x)
        x = matrix_multi(x, x)
        n >>= 1
    return answer


def output_matrix(x):
    print('\n新矩阵有{0}行，{1}列: '.format(x.row, x.col))
    for i in range(x.row):
        for j in range(x.col):
            print(x.ite[i][j], end='    ')
        print()


def main():
    n, x = map(int, input('分别输入矩阵的行列、矩阵的幂次，以空格隔开: ').split())
    matrix = Matrix(n, n)
    for i in range(n):
        matrix.ite[i] = list(map(int, input('输入矩阵第{0}行的n个元素，以空格隔开: '.format(i + 1)).split()))

    output_matrix(fast_power(matrix, x))


if __name__ == '__main__':
    main()
