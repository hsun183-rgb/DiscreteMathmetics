ELEMENTS = (1, 2, 3, 4, 5)
SIZE = len(ELEMENTS)


# 1. 관계행렬 입력 기능
def read_matrix():
    matrix = []
    print("5×5 관계행렬을 입력하세요. 예: 1 0 1 0 0")

    for row_number in ELEMENTS:
        while True:
            values = input(f"{row_number}행: ").split()
            if len(values) == SIZE and all(value in ("0", "1") for value in values):
                matrix.append([int(value) for value in values])
                break
            print("0 또는 1을 공백으로 구분하여 5개 입력하세요.")

    return matrix


def print_matrix(matrix):
    for row in matrix:
        print(" ".join(map(str, row)))


# 2.동치관계 판별 기능
def find_reflexive_violation(matrix):
    for i, a in enumerate(ELEMENTS):
        if matrix[i][i] == 0:
            return f"({a}, {a})이 관계에 없습니다."
    return None


def find_symmetric_violation(matrix):
    for i, a in enumerate(ELEMENTS):
        for j, b in enumerate(ELEMENTS):
            if matrix[i][j] == 1 and matrix[j][i] == 0:
                return f"({a}, {b})은 있지만 ({b}, {a})은 없습니다."
    return None


def find_transitive_violation(matrix):
    for i, a in enumerate(ELEMENTS):
        for j, b in enumerate(ELEMENTS):
            for k, c in enumerate(ELEMENTS):
                if matrix[i][j] == 1 and matrix[j][k] == 1 and matrix[i][k] == 0:
                    return f"({a}, {b})과 ({b}, {c})은 있지만 ({a}, {c})은 없습니다."
    return None


# 3. 동치류 출력 기능
def equivalence_class(matrix, i):
    """원소 ELEMENTS[i]의 동치류 [a] = {x | a R x}"""
    return [b for b, related in zip(ELEMENTS, matrix[i]) if related == 1]


def print_equivalence_classes(matrix):
    print("각 원소의 동치류")
    for i, a in enumerate(ELEMENTS):
        members = [str(b) for b in equivalence_class(matrix, i)]
        print(f"[{a}] = {{{', '.join(members)}}}")


def show_analysis(matrix):
    violations = {
        "반사성": find_reflexive_violation(matrix),
        "대칭성": find_symmetric_violation(matrix),
        "추이성": find_transitive_violation(matrix),
    }

    for property_name, reason in violations.items():
        if reason is None:
            print(f"{property_name}: 만족")
        else:
            # 추가 기능 1: 성질을 위반한 구체적인 예시 출력
            print(f"{property_name}: 불만족 - {reason}")

    if all(reason is None for reason in violations.values()):
        print("동치관계입니다.")
        print_equivalence_classes(matrix)
    else:
        print("동치관계가 아닙니다.")

    return violations


# 4. 폐포 구현 기능
def reflexive_closure(matrix):
    closed = [row[:] for row in matrix]
    for i in range(SIZE):
        closed[i][i] = 1
    return closed


def symmetric_closure(matrix):
    closed = [row[:] for row in matrix]
    for i in range(SIZE):
        for j in range(SIZE):
            if matrix[i][j] == 1:
                closed[j][i] = 1
    return closed


def transitive_closure(matrix):
    closed = [row[:] for row in matrix]

    # 워셜 알고리즘: 중간 원소 k를 거쳐 i에서 j까지 갈 수 있는지 확인
    for k in range(SIZE):
        for i in range(SIZE):
            for j in range(SIZE):
                if closed[i][k] == 1 and closed[k][j] == 1:
                    closed[i][j] = 1

    return closed


def equivalence_closure(matrix):
    # 반사 → 대칭 → 추이 순서로 적용하면 항상 동치관계가 됨
    return transitive_closure(symmetric_closure(reflexive_closure(matrix)))


def get_added_pairs(before, after):
    added = []
    for i, a in enumerate(ELEMENTS):
        for j, b in enumerate(ELEMENTS):
            if before[i][j] == 0 and after[i][j] == 1:
                added.append((a, b))
    return added


def show_closure_result(name, original, closed):
    print(f"\n[{name} 폐포]")
    print("변환 전 행렬")
    print_matrix(original)
    print("변환 후 행렬")
    print_matrix(closed)

    # 추가 기능 2: 폐포를 만들면서 새로 추가된 순서쌍 출력
    added = get_added_pairs(original, closed)
    print("추가된 순서쌍:", ", ".join(map(str, added)) if added else "없음")

    print("\n폐포 변환 후 재판별")
    show_analysis(closed)


def main():
    original = read_matrix()
    print("\n[입력 관계 판별]")
    violations = show_analysis(original)

    closures = (
        ("반사성", "반사", reflexive_closure),
        ("대칭성", "대칭", symmetric_closure),
        ("추이성", "추이", transitive_closure),
    )

    for property_name, closure_name, make_closure in closures:
        if violations[property_name] is not None:
            closed = make_closure(original)
            show_closure_result(closure_name, original, closed)

    # 세 폐포를 모두 적용해 동치관계로 만든 뒤 재판별 + 동치류 출력
    if any(reason is not None for reason in violations.values()):
        final = equivalence_closure(original)
        show_closure_result("반사+대칭+추이(동치)", original, final)


if __name__ == "__main__":
    main()
