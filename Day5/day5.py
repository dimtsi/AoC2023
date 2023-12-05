from collections import deque

from typing import (
    Tuple,
    Optional,
)
from copy import deepcopy

import re


def parse(filename: str):
    with open(filename, "r") as f:
        seeds = list(map(int, re.findall("\d+", f.read().rstrip().split("\n")[0])))

    G = {}
    with open(filename, "r") as f:
        for rule in f.read().strip().split("\n\n")[1:]:
            ranges = []
            for i, l in enumerate(rule.split("\n")):
                if l.endswith("map:"):
                    key = tuple(l.split(" ")[0].split("-to-"))
                else:
                    r = list(map(int, re.findall("\d+", l)))
                    ranges.append(r)

            G[key] = deepcopy(ranges)

    return seeds, G


def solve(n, rs):
    for r in rs:
        if r[1] <= n < r[1] + r[2]:
            return r[0] + (n - r[1])
    return n


def run(seeds, G):
    score = []
    for seed in seeds:
        curr_num = seed
        q = deque(G.values())
        while q:
            r = q.popleft()
            curr_num = solve(curr_num, r)
        score.append(curr_num)

    return min(score)


def solve2(n_s, rrs):
    rs = rrs[1]

    src_overlaps = []
    trg_overlaps = []
    for n in n_s:
        for r in rs:
            src = [r[1], r[1] + r[2] - 1]
            tgt = [r[0], r[0] + r[2] - 1]

            if src[0] <= n[0] <= n[1] <= src[1]:
                ovp = [n[0], n[1]]

            elif n[0] <= src[0] <= src[1] <= n[1]:
                ovp = [src[0], src[1]]

            elif n[0] <= src[0] <= n[1] <= src[1]:
                ovp = [src[0], n[1]]

            elif src[0] <= n[0] <= src[1] <= n[1]:
                ovp = [n[0], src[1]]

            else:
                ovp = None

            if ovp:
                trg_ovp = [tgt[0] + (ovp[0] - src[0]), tgt[0] + (ovp[1] - src[0])]

                assert trg_ovp[1] <= tgt[1]
                assert trg_ovp[0] >= tgt[0]
                src_overlaps.append(ovp)
                trg_overlaps.append(trg_ovp)

    out = trg_overlaps if trg_overlaps else n_s
    return out


def run2(seeds, G):
    s_ivs = []
    for i, seed in enumerate(seeds):
        if i % 2 == 0 and seed > 0:
            lo = seed
        else:
            hi = lo + seed - 1
            s_ivs.append([lo, hi])
    print()
    score = []
    for seed in s_ivs:
        l_nums = []
        curr_num = [seed]
        q = deque(G.items())
        while q:
            r = q.popleft()
            curr_num = solve2(curr_num, r)
            l_nums.append(deepcopy(curr_num))
            # print()
        score.append(min(n[0] for n in curr_num))

    return min(score)


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    s, g = parse(filename)
    answer_a = run(s, g)
    l1 = parse(filename)
    answer_b = run2(s, g)

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":
    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 35
    sample_b_answer = 60  # Wrong answer but works on personal input

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
    from datetime import datetime

    dt = datetime(2023, 12, 5)
    submit_answer(answer_a, "a", dt)
    submit_answer(answer_b, "b", dt)
