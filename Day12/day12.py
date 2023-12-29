import os
from collections import Counter, defaultdict, deque
from datetime import datetime
from functools import reduce, lru_cache, cache
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
        lines: List[str] = f.read().strip().split("\n")
    return lines


@lru_cache(None)
def combs(s, vals: Tuple[int], is_prev_hash, is_prev_dot, n_hash, n_dot):
    if s == "":
        if len(vals) > 1:
            res = 0
        elif n_hash == 0 and not vals:
            res = 1
        elif vals[0] == n_hash:
            res = 1
        else:
            res = 0
        # if res == 1:
        # print(history)
        # ALL_RES.append(history)
        return res

    score = 0
    if s[0] == ".":
        if is_prev_hash and n_hash != vals[0]:
            return 0
        score += combs(
            s[1:], vals[1:] if is_prev_hash else vals[:], False, True, 0, n_dot + 1
        )
    elif s[0] == "#":
        if not vals or n_hash + 1 > vals[0]:
            return 0
        score += combs(s[1:], vals[:], True, False, n_hash + 1, 0)
    elif s[0] == "?":
        score += combs("#" + s[1:], vals[:], is_prev_hash, is_prev_dot, n_hash, n_dot)
        score += combs("." + s[1:], vals[:], is_prev_hash, is_prev_dot, n_hash, n_dot)
    else:
        assert False
    return score


def run(lines):
    score = 0
    for line in lines:
        s, vals = line.split(" ")
        ns = tuple(map(int, re.findall("\d+", vals)))
        new_score = combs(s, ns, False, False, 0, 0)
        score += new_score
    return score


def runp2(lines):
    score = 0
    for line in lines:
        s, vals = line.split(" ")
        ns = tuple(map(int, re.findall("\d+", vals)))

        new_s = "?".join([s] * 5)
        new_ns = ns * 5

        new_score = combs(new_s, new_ns, False, False, 0, 0)
        score += new_score
    return score


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    lines = parse(filename)
    answer_a = run(lines)

    lines = parse(filename)
    answer_b = runp2(lines)

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":
    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 21
    sample_b_answer = 525152

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
    dt = datetime(2023, 12, 12)
    submit_answer(answer_a, "a", dt)
    submit_answer(answer_b, "b", dt)
