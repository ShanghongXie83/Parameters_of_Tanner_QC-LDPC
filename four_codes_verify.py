"""Verify the absence of codewords of weight 2J+2 in four Tanner codes."""

from collections import deque
from functools import lru_cache, reduce
from itertools import combinations, product
from operator import xor


CASES = ((13, 4, 5), (19, 4, 8), (31, 9, 27), (211, 55, 14))


def orbit(p, generator):
    values = [1]
    while (value := generator * values[-1] % p) != 1:
        values.append(value)
    return values


def parity_checks(p, a, b):
    A, B = orbit(p, a), orbit(p, b)
    columns = [
        tuple(row * p + (x + slope * u) % p for row, slope in enumerate(B))
        for u in A for x in range(p)
    ]
    rows = [[] for _ in range(p * len(B))]
    for index, checks in enumerate(columns):
        for check in checks:
            rows[check].append(index)
    return len(A), len(B), columns, rows


def bitmask(indices):
    return sum(1 << index for index in indices)


def girth_at_coordinate_zero(columns, rows):
    """The coordinates are transitive under (u,x) -> (cu,cx+t)."""
    n = len(columns)
    neighbors = [tuple(n + check for check in col) for col in columns] + rows
    distance = [-1] * len(neighbors)
    parent = [-1] * len(neighbors)
    distance[0] = 0
    queue = deque([0])
    girth = len(neighbors) + 1
    while queue:
        node = queue.popleft()
        if 2 * distance[node] >= girth:
            break
        for adjacent in neighbors[node]:
            if distance[adjacent] < 0:
                parent[adjacent] = node
                distance[adjacent] = distance[node] + 1
                queue.append(adjacent)
            elif adjacent != parent[node]:
                girth = min(girth, distance[node] + distance[adjacent] + 1)
    return girth


def information_set_search(row_masks, n, cutoff):
    """Exclude nonzero weights through the cutoff by information-set enumeration."""
    rows = list(row_masks)
    pivots = []
    for col in range(n):
        bit = 1 << col
        index = len(pivots)
        pivot = next((i for i in range(index, len(rows)) if rows[i] & bit), None)
        if pivot is None:
            continue
        rows[index], rows[pivot] = rows[pivot], rows[index]
        for i in range(len(rows)):
            if i != index and rows[i] & bit:
                rows[i] ^= rows[index]
        pivots.append(col)

    pivot_set = set(pivots)
    basis = []
    for col in range(n):
        if col not in pivot_set:
            bit = 1 << col
            basis.append(bit | bitmask(p for i, p in enumerate(pivots) if rows[i] & bit))
    assert all((word & row).bit_count() % 2 == 0 for word in basis for row in row_masks)
    k = len(basis)
    radius = cutoff * k // n
    # By coordinate transitivity, some image of a support of weight at
    # most cutoff meets the information set in at most radius positions.
    for size in range(1, radius + 1):
        for words in combinations(basis, size):
            if reduce(xor, words).bit_count() <= cutoff:
                return False
    return True


@lru_cache(maxsize=None)
def partitions(total, multiplicity_cap, minimum=1, repetitions=0):
    """Return nondecreasing partitions with bounded part multiplicities."""
    if total == 0:
        return ((),)

    result = []
    for part in range(minimum, total + 1):
        count = repetitions + 1 if part == minimum else 1
        if count <= multiplicity_cap:
            tails = partitions(total - part, multiplicity_cap, part, count)
            result.extend((part,) + tail for tail in tails)
    return tuple(result)


def p31_moment_candidates(p, J, L):
    """Recompute the moment survivors for the fixed p=31 case."""
    gap = L - J
    exponents = range(2, (L - 1) // gap + 1)
    survivors = set()
    for total in range(1, J + 2):
        for positive, negative in product(partitions(total, gap), repeat=2):
            support_size = len(positive) + len(negative)
            if not J + 1 <= support_size <= L:
                continue
            values = (
                tuple(-part for part in reversed(negative))
                + (0,) * (L - support_size)
                + positive
            )
            if all(sum(value**v for value in values) % p == 0 for v in exponents):
                survivors.add(values)
    return survivors


def normalized_polynomials(p, J, L, candidates):
    """Find q(x) = sum(c_i * (x**i - x), i=2..L-J) matching a survivor."""
    if any(0 not in values for values in candidates):
        raise ValueError("The q(1)=0 normalization requires a zero value.")

    A = [u for u in range(1, p) if pow(u, L, p) == 1]
    if len(A) != L:
        raise ValueError("The subgroup of order L has the wrong size.")
    target_values = {tuple(sorted(value % p for value in v)) for v in candidates}
    terms_by_point = [
        tuple((pow(u, exponent, p) - u) % p for exponent in range(2, L - J + 1))
        for u in A
    ]

    matches = []
    for coefficients in product(range(p), repeat=L - J - 1):
        values = tuple(sorted(
            sum(c * term for c, term in zip(coefficients, terms)) % p
            for terms in terms_by_point
        ))
        if values in target_values:
            matches.append(coefficients)
    return matches


def verify_case(p, a, b):
    L, J, columns, rows = parity_checks(p, a, b)
    weight = 2 * J + 2
    if p in (13, 19):
        if not information_set_search(list(map(bitmask, rows)), len(columns), weight):
            raise RuntimeError(f"Moore({p},{a},{b}): found a nonzero word through weight {weight}")
        method = "information-set enumeration"
    elif p == 31:
        # Since J >= 4, a support of size 2J+2 cannot lie on a smooth
        # conic. Its signed multiplicities must pass both tests below.
        candidates = p31_moment_candidates(p, J, L)
        if len(candidates) != 36:
            raise RuntimeError("Unexpected number of moment survivors for p=31")
        if normalized_polynomials(p, J, L, candidates):
            raise RuntimeError(f"Moore({p},{a},{b}): polynomial test was inconclusive")
        method = "root-multiplicity certificate"
    else:
        girth = girth_at_coordinate_zero(columns, rows)
        if girth < 12 or 2 * (J * J - J + 1) <= weight:
            raise RuntimeError(f"Moore({p},{a},{b}): girth bound was inconclusive")
        method = f"Tanner bound with girth {girth}"

    print(f"Moore({p},{a},{b}): J={J}; no codeword of weight {weight} ({method})")


if __name__ == "__main__":
    for case in CASES:
        verify_case(*case)
