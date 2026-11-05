"""Núcleo matemático: algoritmo voraz (Fibonacci-Sylvester), verificações e testes em lote."""
import math
from fractions import Fraction

cdiv = lambda a, b: -(-a // b)          # teto de a/b com inteiros (sem ponto flutuante)

def decompose(p, q):
    """Algoritmo voraz (Fibonacci-Sylvester) da Proposição 12."""
    r, steps = Fraction(p, q), []
    while r:
        a, b = r.numerator, r.denominator
        k = cdiv(b, a)                       # k = teto(q/p)
        nxt = r - Fraction(1, k)
        steps.append(dict(p=a, q=b, k=k, p1=a * k - b, q1=b * k, rest=nxt))
        r = nxt
    return steps

def verify(p, q, st):
    ks = [s["k"] for s in st]
    return {
        "Soma das frações unitárias = p/q": sum(Fraction(1, k) for k in ks) == Fraction(p, q),
        "Denominadores distintos e crescentes": all(x < y for x, y in zip(ks, ks[1:])),
        "Em cada passo: 1/k ≤ p/q < 1/(k−1)  (k = ⌈q/p⌉)":
            all(Fraction(1, s["k"]) <= Fraction(s["p"], s["q"]) < Fraction(1, s["k"] - 1) for s in st),
        "Numerador p1 = pk − q é estritamente menor que p (indução)": all(s["p1"] < s["p"] for s in st),
        "Resto < 1/k (termos seguintes são menores que 1/k)": all(s["rest"] < Fraction(1, s["k"]) for s in st),
        "Número de termos ≤ p": len(st) <= p,
    }

def terms(st): return " + ".join(f"1/{s['k']}" for s in st)

def run_tests(N):
    total = ok = 0; hist = {}; fails = []; mt = (0, 0, 0); md = (0, 0, 0)
    for q in range(2, N + 1):
        for p in range(1, q):
            if math.gcd(p, q) != 1: continue
            st = decompose(p, q); total += 1
            if all(verify(p, q, st).values()): ok += 1
            else: fails.append(f"{p}/{q}")
            hist[len(st)] = hist.get(len(st), 0) + 1
            if len(st) > mt[0]: mt = (len(st), p, q)
            dg = len(str(st[-1]["k"]))
            if dg > md[0]: md = (dg, p, q)
    return dict(total=total, ok=ok, fails=fails[:20], hist=dict(sorted(hist.items())),
                maxterms=mt, maxdigits=md)

def table_2n():
    return [(n, terms(decompose(2, n))) for n in range(5, 102, 2)]

def parse(args):
    p, q = int(args.get("p", 5)), int(args.get("q", 7))
    if not (0 < p < q <= 10**12): raise ValueError("Use inteiros com 0 < p < q ≤ 10^12.")
    return p, q

def ser(st):
    return [dict(p=str(s["p"]), q=str(s["q"]), k=str(s["k"]), p1=str(s["p1"]), q1=str(s["q1"]),
                 rn=str(s["rest"].numerator), rd=str(s["rest"].denominator)) for s in st]
