def input_matrix():
    n = int(input("정방행렬의 차수를 입력하세요: "))
    mat = []
    for i in range(n):
        while True:
            row = list(map(float, input(f"{i+1}행: ").split()))
            if len(row) == n:
                mat.append(row)
                break
            print(f"숫자를 {n}개 입력해주세요.")
    return mat


def det(m):
    n = len(m)
    if n == 1:
        return m[0][0]
    if n == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]

    # 첫 번째 행 기준 여인수 전개
    result = 0
    for c in range(n):
        minor = [r[:c] + r[c+1:] for r in m[1:]]
        result += (-1) ** c * m[0][c] * det(minor)
    return result


def inverse_det(m):
    n = len(m)
    d = det(m)
    if abs(d) < 1e-10:
        raise ValueError("역행렬이 존재하지 않습니다.")
    if n == 1:
        return [[1 / m[0][0]]]

    # 여인수 행렬 구하기
    cof = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = [r[:j] + r[j+1:] for k, r in enumerate(m) if k != i]
            cof[i][j] = (-1) ** (i + j) * det(minor)

    # 전치 후 det로 나누기
    return [[cof[j][i] / d for j in range(n)] for i in range(n)]


def inverse_gauss(m):
    n = len(m)
    # [A | I] 만들기
    aug = [m[i][:] + [1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

    for i in range(n):
        # 피벗이 0이면 행 교환
        if abs(aug[i][i]) < 1e-10:
            for r in range(i + 1, n):
                if abs(aug[r][i]) >= 1e-10:
                    aug[i], aug[r] = aug[r], aug[i]
                    break
            else:
                raise ValueError("역행렬이 존재하지 않습니다.")

        p = aug[i][i]
        aug[i] = [x / p for x in aug[i]]

        for r in range(n):
            if r != i:
                f = aug[r][i]
                aug[r] = [aug[r][j] - f * aug[i][j] for j in range(2 * n)]

    return [row[n:] for row in aug]


def multiply(a, b):
    n = len(a)
    res = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                res[i][j] += a[i][k] * b[k][j]
    return res

def is_identity(m):
    n = len(m)
    I = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    return is_same(m, I)

def print_matrix(m):
    for row in m:
        print([round(x, 4) for x in row])

def is_same(a, b):
    n = len(a)
    return all(abs(a[i][j] - b[i][j]) < 1e-10 for i in range(n) for j in range(n))


A = input_matrix()

print("\n[입력한 행렬]")
print_matrix(A)

try:
    inv1 = inverse_det(A)
    inv2 = inverse_gauss(A)

    print("\n[행렬식으로 구한 역행렬]")
    print_matrix(inv1)

    print("\n[가우스-조던 소거법으로 구한 역행렬]")
    print_matrix(inv2)

    print("\n[두 방법 비교]")
    if is_same(inv1, inv2):
        print("두 결과가 동일합니다.")
    else:
        print("두 결과가 다릅니다.")

    # 검산: A × A^-1 = I 인지 확인
    print("\n[추가: 역행렬 검산]")
    check = multiply(A, inv1)
    print("A × A^-1:")
    print_matrix(check)

    if is_identity(check):
        print("단위행렬이 나오므로 검증 성공")
    else:
        print("검증 실패")

except ValueError as e:
    print("\n오류:", e)