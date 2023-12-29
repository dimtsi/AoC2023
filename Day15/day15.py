import os
from collections import Counter, defaultdict, deque, OrderedDict
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
        lines: List[str] = f.read().strip().split("\n")[0]  # type: ignore

    return lines


def run(lines):
    score = 0
    for l in lines.split(","):
        n = 0
        for c in l:
            n += ord(c)
            n *= 17
            n %= 256
        score += n
        print()

    return score


def hash_(s):
    n = 0
    for c in s:
        n += ord(c)
        n *= 17
        n %= 256
    return n


def runp2(lines):
    G = defaultdict(OrderedDict)
    for l in lines.split(","):
        if "=" in l:
            label, val = l.split("=")
            box = hash_(label)
            G[box][label] = val

        elif l.endswith("-"):
            label = l.split("-")[0]
            box = hash_(label)
            if label in G[box]:
                G[box].pop(label)
        else:
            assert False

    score = 0
    for box, vals in G.items():
        for i, val in enumerate(vals.values()):
            score += (box + 1) * (i + 1) * int(val)

    return score


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    lines = parse(filename)
    answer_a = run(lines)  # type: ignore

    lines = parse(filename)
    answer_b = runp2(lines)  # type: ignore

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":
    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 1320
    sample_b_answer = 145

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
    dt = datetime(2023, 12, 15)
    submit_answer(answer_a, "a", dt)
    submit_answer(answer_b, "b", dt)
