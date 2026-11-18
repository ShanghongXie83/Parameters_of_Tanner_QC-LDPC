# Supplementary Material for Proposition 27

This package contains the complete proof of Proposition 27 and the computer certificates used in Theorem 31. Its notation, hypotheses, and result numbers agree with the accompanying manuscript.

## Files

| File | Contents |
| --- | --- |
| `Supplementary_Material_for_Proposition_27.pdf` | Complete proof of Proposition 27 and interpretation of the computer certificates. |
| `verify.py` | Exact verification program. |
| `results.json` | Complete program output and numerical certificates. |
| `README.md` | File descriptions and reproduction instructions. |

## Correspondence with the manuscript

The supplement uses $J$ and $L$ for the orders of $b$ and $a$, respectively. Parameter triples in the certificates are ordered as $(p,J,L)$. The field `dimension` records the binary dimension $k$.

- Lemma 8: product-set equality and coset structure.
- Lemma 9: even-direction bound and Redei-polynomial construction.
- Theorem 25: characterization of supports of Hamming weight 2j.
- Proposition 27, parts (i)--(iii): odd column occupancy, the quadratic quotient, and the two root polynomials.
- Lemma 28: root-multiplicity and moment constraints, including the square-sum bound.
- Theorem 31: d >= 2j+4 for J >= 3 and 1 <= L-J <= min{5,J-1}.
- Proposition 17: girth-based distance bound used at the exceptional prime.

The PDF recalls Lemma 9 and its polynomial notation; the proof of that lemma is in the manuscript. Proposition 27 and its part labels agree with the manuscript.

## Reproduction

The program requires Python, SymPy, and NumPy with `bitwise_count` support. Install the dependencies with the following command.

```text
python -m pip install numpy sympy
```

Generate `results.json` next to the program:

```text
python verify.py
```

Recompute all certificates and compare them with the supplied output without modifying it:

```text
python verify.py --check
```

Run without `-O` or `-OO`, so that verification assertions remain enabled. The program reports success only after all checks pass. The boundary-code calculation enumerates all 536870912 kernel vectors in bounded integer-array batches; runtime depends on the machine.

## Certificates

| Output field | Contents and proof role |
| --- | --- |
| `status` | Successful completion of all checks. |
| `proof_references` | Corresponding manuscript result numbers and supplementary PDF filename. |
| `summary` | Principal counts and conclusions. |
| `symbolic_checks` | Hessian, coefficient-minor, and quadratic-restriction identities for Proposition 27, and the square-sum identity for Lemma 28. |
| `moment_screen` | 69 parameter pairs, 19532 integer multisets, and 43 candidates passing the prime and moment conditions. |
| `polynomial_screen` | Complete normalized polynomial searches for the three remaining parameter triples. |
| `boundary_code` | Binary matrix rank, kernel basis, complete weight distribution, and a weight-16 codeword for the length-78 boundary code. |
| `coefficient_check` | Exact exceptional-prime obstruction 1055 = 5*211. |
| `p211_ball` | Nodes and parent relations of the radius-five tree at (p,J,L) = (211,3,5). |

The polynomial searches test 13, 361, and 923521 polynomials for (p,J,L) = (13,4,6), (19,6,9), and (31,10,15), respectively. Only the first case gives matches: q(x) = plus or minus 2(x^2-x). Complete binary-kernel enumeration gives minimum distance 16 in that case. At the exceptional prime 211, the radius-five tree layers have sizes 1, 3, 12, 24, 96, 192, with zero non-tree edges.

These calculations certify the finite branches of Theorem 31. The PDF explains the reduction to those branches, the binary-coordinate encoding, and the deductions from the certificates. The calculations use exact symbolic expressions, integers, rational numbers, and finite-field residues.
