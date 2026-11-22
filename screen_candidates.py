"""Enumerate and screen the candidate root-multiplicity multisets."""

from collections import defaultdict
from functools import lru_cache
from itertools import product
from math import lcm


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


def prime_divisors(n):
    """Yield the distinct prime divisors of a positive integer."""
    factor = 2
    while factor * factor <= n:
        if n % factor == 0:
            yield factor
            while n % factor == 0:
                n //= factor
        factor += 1
    if n > 1:
        yield n


def moment_filter():
    pairs = [
        (J, J + gap)
        for gap in range(1, 6)
        for J in range(max(3, gap + 1), 6 * gap)
    ]
    survivors = defaultdict(set)
    candidate_count = 0

    for J, L in pairs:
        gap = L - J
        common_multiple = lcm(J, L)
        last_moment = (L - 1) // gap
        for total in range(1, J + 2):
            parts = partitions(total, gap)
            # Positive and negative partitions form an ordered pair.
            for positive, negative in product(parts, repeat=2):
                support_size = len(positive) + len(negative)
                if not J + 1 <= support_size <= L:
                    continue
                candidate_count += 1
                values = (
                    tuple(-part for part in reversed(negative))
                    + (0,) * (L - support_size)
                    + positive
                )
                moments = [
                    sum(value**exponent for value in values)
                    for exponent in range(2, last_moment + 1)
                ]
                for p in prime_divisors(moments[0]):
                    if p <= 2 * L or (p - 1) % common_multiple:
                        continue
                    if all(moment % p == 0 for moment in moments):
                        survivors[p, J, L].add(values)

    return len(pairs), candidate_count, survivors


def main():
    pair_count, candidate_count, survivors = moment_filter()
    print(f"Pairs (J, L): {pair_count}")
    print(f"Candidate multisets: {candidate_count}")
    print("Survivors after moment screening:")
    for triple, values in sorted(survivors.items()):
        print(f"  (p, J, L) = {triple}: {len(values)} multisets")


if __name__ == "__main__":
    main()
