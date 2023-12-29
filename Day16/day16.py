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
        lines: List[str] = f.read().strip().split("\n")
        # list(map(int, re.findall("-?\d+", line)))
    lines = [list(l) for l in lines]  # type: ignore
    return lines


CACHE = {}


def move(start_dir, start_i, start_j, score, G, energ):
    new_states = deque([(start_dir, start_i, start_j)])
    while new_states:
        dir, i, j = new_states.popleft()
        curr = G[i][j]

        if (dir, i, j) in CACHE:
            continue

        if dir == "N":
            if curr == "|" and i > 0:
                new_states.append(("N", i - 1, j))
            if curr == "\\" and j > 0:
                new_states.append(("W", i, j - 1))
            if curr == "/" and j < len(G[0]) - 1:
                new_states.append(("E", i, j + 1))
            if curr == "-" and j > 0:
                new_states.append(("W", i, j - 1))
            if curr == "-" and j < len(G[0]) - 1:
                new_states.append(("E", i, j + 1))
            if curr == "." and i > 0:
                new_states.append(("N", i - 1, j))

        elif dir == "S":
            if curr == "|" and i < len(G) - 1:
                new_states.append(("S", i + 1, j))
            if curr == "\\" and j < len(G[0]) - 1:
                new_states.append(("E", i, j + 1))
            if curr == "/" and j > 0:
                new_states.append(("W", i, j - 1))
            if curr == "-" and j > 0:
                new_states.append(("W", i, j - 1))
            if curr == "-" and j < len(G[0]) - 1:
                new_states.append(("E", i, j + 1))
            if curr == "." and i < len(G) - 1:
                new_states.append(("S", i + 1, j))

        elif dir == "E":
            if curr == "|" and i < len(G) - 1:
                new_states.append(("S", i + 1, j))
            if curr == "|" and i > 0:
                new_states.append(("N", i - 1, j))
            if curr == "\\" and i < len(G) - 1:
                new_states.append(("S", i + 1, j))
            if curr == "/" and i > 0:
                new_states.append(("N", i - 1, j))

            if curr == "-" and j < len(G[0]) - 1:
                new_states.append(("E", i, j + 1))
            if curr == "." and j < len(G[0]) - 1:
                new_states.append(("E", i, j + 1))

        elif dir == "W":
            if curr == "|" and i < len(G) - 1:
                new_states.append(("S", i + 1, j))
            if curr == "|" and i > 0:
                new_states.append(("N", i - 1, j))

            if curr == "\\" and i > 0:
                new_states.append(("N", i - 1, j))

            if curr == "/" and i < len(G) - 1:
                new_states.append(("S", i + 1, j))

            if curr == "-" and j > 0:
                new_states.append(("W", i, j - 1))
            if curr == "." and j > 0:
                new_states.append(("W", i, j - 1))
        else:
            assert False
        CACHE[(dir, i, j)] = score
        energ.add((i, j))

    return energ


def run(lines):
    G = lines
    global CACHE
    CACHE = {}
    poss = move("E", 0, 0, 0, G, set())
    p1_res = len(poss)
    return p1_res


def runp2(lines):
    global CACHE
    G = lines
    max_score = 0
    for i in range(len(G)):
        for j in range(len(G[0])):
            pos_to_expl = []
            if i in [0, len(G) - 1] or j in [0, len(G[0]) - 1]:
                if i == 0:
                    pos_to_expl.append("S")
                if j == 0:
                    pos_to_expl.append("E")
                if j == len(G[0]) - 1:
                    pos_to_expl.append("W")
                if i == len(G) - 1:
                    pos_to_expl.append("N")

                for pos in pos_to_expl:
                    CACHE = {}
                    poss = move(pos, i, j, 0, G, set())
                    max_score = max(max_score, len(poss))
    return max_score


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

    sample_a_answer = 46
    sample_b_answer = 51

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
    dt = datetime(2023, 12, 16)
    submit_answer(answer_a, "a", dt)
    submit_answer(answer_b, "b", dt)
