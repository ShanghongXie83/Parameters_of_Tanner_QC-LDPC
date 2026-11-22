# Tanner QC-LDPC verification tools

These scripts reproduce the finite computations used in the proof of
the minimum-distance bound $d \ge 2J+4$ for
$J \ge 3$ and $1 \le L-J \le \min(5,J-1)$.
Each script runs independently and uses only the Python standard library.

Here `Moore(p,a,b)` denotes the code with circulant
size $p$ and with $a$ and $b$ of multiplicative orders $L$ and $J$,
respectively.

## Candidate screening

[screen_candidates.py](screen_candidates.py) enumerates the signed
root-multiplicity multisets for the 69 pairs $(J,L)$ left by the
proof. For each multiset, the script checks prime divisors of its
second moment against $p>2L$, the requirement that the least common multiple of $J$ and $L$ divides $p-1$, and the remaining moment conditions.

```sh
python screen_candidates.py
```

Output

```text
Pairs (J, L): 69
Candidate multisets: 19532
Survivors after moment screening:
  (p, J, L) = (13, 4, 6): 2 multisets
  (p, J, L) = (19, 6, 9): 5 multisets
  (p, J, L) = (31, 10, 15): 36 multisets
```

## Weight verification for the four representative codes

[four_codes_verify.py](four_codes_verify.py) verifies the absence of
codewords of weight $2J+2$ in the four codes used in the two cases of
the proof.

- For $p=13$ and $p=19$, the script uses coordinate transitivity and
  enumerates the required information words in a systematic basis.
- For $p=31$, it recomputes the 36 surviving multisets and checks that
  none can be realized by the values of a normalized polynomial on
  the column subgroup.
- For $p=211$, it computes the Tanner graph girth and applies the
  distance bound for girth 12.

```sh
python four_codes_verify.py
```

Output

```text
Moore(13,4,5): J=4; no codeword of weight 10 (information-set enumeration)
Moore(19,4,8): J=6; no codeword of weight 14 (information-set enumeration)
Moore(31,9,27): J=10; no codeword of weight 22 (root-multiplicity certificate)
Moore(211,55,14): J=3; no codeword of weight 8 (Tanner bound with girth 12)
```

In the proof, these exclusions combine with the lower bound
$d \ge 2J+2$ and the even-weight property to give $d \ge 2J+4$.
