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

    shapes = []
    for line in lines:
        shapes.append(list(line))

    return shapes


def print_g(G):
    for row in G:
        print("".join(row))


def run(lines):
    lines = np.array(lines)
    dir = "N"

    if dir == "N":
        G = deepcopy(lines)
        score = 0
        while True:
            moved = 0
            for i in range(1, len(G)):
                for j in range(len(G[1])):
                    if G[i][j] == "O" and G[i - 1][j] == ".":
                        G[i - 1][j] = "O"
                        G[i][j] = "."
                        moved += 1

            if moved == 0:
                break

        out = G
    # for row in G:
    #     print("".join(row))

    score = 0
    for i, row in enumerate(out):
        # print(row)
        n_o = Counter(row)["O"]
        score += (len(G) - i) * n_o

    return score


def round(G):
    total_moved = 0
    dir = "N"

    # N
    while True:
        moved = 0
        for i in range(1, len(G)):
            for j in range(len(G[1])):
                if G[i][j] == "O" and G[i - 1][j] == ".":
                    G[i - 1][j] = "O"
                    G[i][j] = "."
                    moved += 1
                    total_moved += 1
        if moved == 0:
            break
    # W
    while True:
        moved = 0
        for i in range(len(G)):
            for j in range(1, len(G[1])):
                if G[i][j] == "O" and G[i][j - 1] == ".":
                    G[i][j - 1] = "O"
                    G[i][j] = "."
                    moved += 1
                    total_moved += 1
        if moved == 0:
            break

    # S
    while True:
        moved = 0
        for i in range(len(G) - 1):
            for j in range(len(G[1])):
                if G[i][j] == "O" and G[i + 1][j] == ".":
                    G[i + 1][j] = "O"
                    G[i][j] = "."
                    moved += 1
                    total_moved += 1
        if moved == 0:
            break

    # E
    while True:
        moved = 0
        for i in range(len(G)):
            for j in range(len(G[1]) - 1):
                if G[i][j] == "O" and G[i][j + 1] == ".":
                    G[i][j + 1] = "O"
                    G[i][j] = "."
                    moved += 1
                    total_moved += 1
        if moved == 0:
            break
    return G


cyc_1 = """
.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....
"""

cyc_2 = """
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O
"""

cyc_3 = """
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O
"""


def run2(lines):
    original = np.array(lines)
    period = None
    t = 0
    g = deepcopy(np.array(lines))
    cache = defaultdict(list)
    while True:
        o_pos = []
        for i, row in enumerate(g):
            for j, c in enumerate(row):
                if c == "O":
                    o_pos.append((i, j))

        o_pos_tup = frozenset(o_pos)

        if period:
            if 1000000000 % period == t % period:
                break
        if o_pos_tup in cache and not period:
            cache[o_pos_tup].append(t)
            if len(cache[o_pos_tup]) > 3:
                if (
                    cache[o_pos_tup][-1] - cache[o_pos_tup][-2]
                    == cache[o_pos_tup][-2] - cache[o_pos_tup][-3]
                ):
                    period = cache[o_pos_tup][-1] - cache[o_pos_tup][-2]
        else:
            cache[o_pos_tup].append(t)

        t += 1
        g = round(g)

    score = 0
    for i, row in enumerate(g):
        n_o = Counter(row)["O"]
        score += (len(g) - i) * n_o

    return score


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    lines = parse(filename)
    answer_a = run(lines)

    lines = parse(filename)
    answer_b = run2(lines)
    print(answer_a, answer_b)
    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":
    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "input.txt"
    input = "input.txt"

    sample_a_answer = 136
    sample_b_answer = 64

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
    dt = datetime(2023, 12, 14)
    submit_answer(answer_a, "a", dt)
    submit_answer(answer_b, "b", dt)
