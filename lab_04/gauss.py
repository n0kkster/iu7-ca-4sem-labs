def Gauss(A, B) -> list[float]:
    n = len(A)
    if n != len(B):
        raise ValueError("Матрица и вектор правой части должны иметь одинаковую длину")

    for i in range(n):
        for j in range(i + 1, n):
            coeff = -(A[j][i] / A[i][i])
            for k in range(i, n):
                A[j][k] += coeff * A[i][k]
            B[j] += coeff * B[i]

    for i in range(n - 1, -1, -1):
        for j in range(i - 1, -1, -1):
            coeff = -(A[j][i] / A[i][i])
            A[j][i] += coeff * A[i][i]
            B[j] += coeff * B[i]

    res = [B[i] / A[i][i] for i in range(n)]
    return res