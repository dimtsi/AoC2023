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
        lines: List[str] = f.read().strip().split("\n\n")

    shapes = []

    for line in lines:
        shape = []
        rows = line.split("\n")
        for row in rows:
            shape.append(list(row))
        shapes.append(shape)

    return shapes


def check_refl(shape, old_refl=None):
    if old_refl:
        old_hor, old_ver = old_refl
    VER = HOR = 0
    rows = True
    s = np.array(shape)
    for i, row in enumerate(s[: len(s) - 1]):
        if list(s[i]) == list(s[i + 1]):
            first, second = i, i + 1
            cand = True
            while first >= 0 and second <= len(s) - 1:
                try:
                    if list(s[first]) != list(s[second]):
                        cand = False
                        break
                except Exception as e:
                    print(e)
                    pass
                first -= 1
                second += 1

            if cand:
                if old_refl:
                    if i + 1 == old_hor:
                        continue
                HOR = i + 1
                VER = 0
                return HOR, VER

    s = np.array(shape).T
    for i, row in enumerate(s[: len(s) - 1]):
        if list(s[i]) == list(s[i + 1]):
            first, second = i, i + 1
            cand = True
            while first >= 0 and second <= len(s) - 1:
                try:
                    if list(s[first]) != list(s[second]):
                        cand = False
                        break
                except Exception as e:
                    print(e)
                    pass
                first -= 1
                second += 1

            if cand:
                if old_refl:
                    if i + 1 == old_ver:
                        continue
                VER = i + 1
                HOR = 0
                return HOR, VER

    # assert (HOR == 0) ^ (VER == 0)
    return HOR, VER


def run(lines):
    score = 0
    for shape in lines:
        hor, ver = check_refl(shape)

        if not ((hor == 0) ^ (ver == 0)):
            print()
        score += (100 * hor) + ver

    return score


def replace_and_check(shape):
    or_hor, or_ver = check_refl(shape)

    for i, row in enumerate(shape):
        for j, c in enumerate(row):
            new_shape = deepcopy(shape)
            if c == ".":
                new_shape[i][j] = "#"
            elif c == "#":
                new_shape[i][j] = "."
            new_hor, new_ver = check_refl(new_shape, (or_hor, or_ver))
            if (new_hor == 0) and (new_ver == 0):
                continue
            return new_hor, new_ver


def run2(lines):
    score = 0
    scores = []
    for shape in lines:
        hor, ver = replace_and_check(shape)

        score += (100 * hor) + ver

    return score


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    lines = parse(filename)
    answer_a = run(lines)

    lines = parse(filename)
    answer_b = run2(lines)

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":
    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 405
    sample_b_answer = 400

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
    dt = datetime(2023, 12, 13)
    submit_answer(answer_a, "a", dt)
    submit_answer(answer_b, "b", dt)
