import os
from collections import Counter, defaultdict, deque
from datetime import datetime
from functools import reduce, lru_cache
from typing import (
    List,
    Tuple,
    Set,
    Dict,
    Iterable,
    DefaultDict,
    Optional,
    Union,
    Generator,
)
from copy import deepcopy
from heapq import heappop, heappush
import string

import re

import numpy as np


def parse(filename: str):
    with open(filename, "r") as f:
        R, P = f.read().strip().split("\n\n")
        # list(map(int, re.findall("-?\d+", line)))

    return R.strip().split("\n"), P.strip().split("\n")


def f(rule, R, P):
    if rule in {"A", "R"}:
        return rule
    elif rule in R.keys():
        return f(R[rule], R, P)

    rs = deque(rule.replace("{", "").replace("}", "").split(","))
    x, m, a, s = list(map(int, re.findall("\d+", P)))

    while len(rs) > 1:
        y = rs.popleft()
        if ":" in y:
            cond, res = y.split(":")
            if eval(cond):
                if res in {"A", "R"}:
                    return res
                else:
                    return f(R[res], R, P)
    assert len(rs) == 1
    if rs[-1] in {"A", "R"}:
        return rs[-1]
    return f(R[rs[-1]], R, P)


def run(R, P):
    RR = {}

    for r in R:
        k, v = r.split("{")
        RR[k] = "{" + v

    ress = []
    score = 0
    for p in P:
        ress.append(f("in", RR, p))
        if ress[-1] == "A":
            score += sum(list(map(int, re.findall("\d+", p))))

    return score


def f2(rule, R, ranges):
    print(rule)
    print(ranges)
    if rule == "A":
        res = reduce(lambda x, y: x * y, ([x[1] - x[0] + 1 for x in ranges.values()]))
        return res
        # scores += sum([x[1] - x[0] + 1 for x in ranges.values()])
    elif rule == "R":
        return 0
    elif rule in R.keys():
        res = f2(R[rule].replace("{", "").replace("}", ""), R, ranges)
        return res
    # "eq"
    assert rule[1] in "<>"

    if rule == "m>2090:A,rfg":
        print()

    eq, otherwise = rule.split(",", 1)

    elem = eq[0]
    avail = ranges[elem]
    min_valid, max_valid = avail
    op, lim = eq[1], int(re.findall("\d+", eq.split(":")[0])[0])
    target = eq.split(":")[1]

    # <
    ranges_T = deepcopy(ranges)
    ranges_F = deepcopy(ranges)
    scores = 0

    if op == "<":
        if max_valid < lim:
            ranges_T[elem] = ranges[elem]
            scores += f2(target, R, ranges_T)
        elif min_valid < lim <= max_valid:
            ranges_T[elem] = [min_valid, lim - 1]
            scores += f2(target, R, ranges_T)
            ranges_F[elem] = [lim, max_valid]
            scores += f2(otherwise, R, ranges_F)
        else:
            assert min_valid > lim
            scores += f2(otherwise, R, ranges_F)

    else:
        assert op == ">"
        if min_valid > lim:
            ranges_T[elem] = ranges[elem]
            scores += f2(target, R, ranges_T)
        elif min_valid <= lim < max_valid:
            ranges_F[elem] = [min_valid, lim]
            scores += f2(otherwise, R, ranges_F)
            ranges_T[elem] = [lim + 1, max_valid]
            scores += f2(target, R, ranges_T)
        else:
            assert max_valid < lim
            scores += f2(otherwise, R, ranges_F)

    print(f"res: {scores}")
    return scores


def runp2(R, P):
    RR = {}

    for r in R:
        k, v = r.split("{")
        RR[k] = "{" + v

    RANGES = {k: [1, 4000] for k in "xmas"}
    score = f2("in", RR, RANGES)

    return score


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    R, P = parse(filename)
    answer_a = run(R, P)

    R, P = parse(filename)
    answer_b = runp2(R, P)

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":
    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 19114
    sample_b_answer = 167409079868000

    answer_a, answer_b = main(sample)
    assert (
        answer_a == sample_a_answer
    ), f"AnswerA incorrect: Actual: {answer_a}, Expected: {sample_a_answer}"
    print("sampleA correct")
    if answer_b:
        assert (
            answer_b == sample_b_answer
        ), f"AnswerB incorrect: Actual: {answer_b}, Expected: {sample_b_answer}"
        print("sampleB correct")

    # Test on your input and submit
    answer_a, answer_b = main(input)
    print(f"Your input answers: \nA: {answer_a}\nB: {answer_b}")
    dt = datetime(2023, 12, 19)
    submit_answer(answer_a, "a", dt)
    submit_answer(answer_b, "b", dt)
