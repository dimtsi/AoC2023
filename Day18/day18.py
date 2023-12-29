import os
from collections import Counter, defaultdict, deque
from datetime import datetime
from functools import reduce, lru_cache
from itertools import chain
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

    ll = []
    for l in lines:
        d, n, cod = l.split(" ")
        ll.append((d, int(n), cod))
    return ll


def all_neighbors(
    matrix: List[List[str]], i: int, j: int, diagonal: bool = False
) -> List[Tuple[int, int]]:
    neighbors = []

    num_rows = len(matrix)
    num_cols = len(matrix[i])

    if i - 1 >= 0:
        neighbors.append((i - 1, j))
    if i + 1 < num_rows:
        neighbors.append((i + 1, j))
    if j - 1 >= 0:
        neighbors.append((i, j - 1))
    if j + 1 < num_cols:
        neighbors.append((i, j + 1))
    return neighbors


def move(x, y, d, n):
    m = {"R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)}

    new_pos = (x + n * m[d][0], y + n * m[d][1])
    return new_pos


def paint(x0, y0, x1, y1, G):
    try:
        G[x0][y0] = "#"
        G[x1][y1] = "#"
    except:
        pass

    if x1 == x0:
        dr = 0
    else:
        dr = (x1 - x0) // abs(x1 - x0)
    if y1 == y0:
        dc = 0
    else:
        dc = (y1 - y0) // abs(y1 - y0)

    curr = x0, y0

    while curr != (x1, y1):
        new_x, new_y = curr[0] + dr, curr[1] + dc
        G[new_x][new_y] = "#"
        curr = (new_x, new_y)
    return G


def build_grid(lines):
    curr = (0, 0)
    G = [curr]
    b = 0
    for d, n, _ in lines:
        new_pos = move(*curr, d, n)
        G.append(new_pos)
        curr = new_pos
        b += n

    print()
    max_r = max(G, key=lambda x: x[0])[0]
    max_c = max(G, key=lambda x: x[1])[1]

    min_r = min(G, key=lambda x: x[0])[0]
    min_c = min(G, key=lambda x: x[1])[1]

    # Move to 0,0
    for i, (ii, jj) in enumerate(G):
        G[i] = ii - min_r, jj - min_c

    new_max_r = max(G, key=lambda x: x[0])[0]
    new_max_c = max(G, key=lambda x: x[1])[1]

    new_min_r = min(G, key=lambda x: x[0])[0]
    new_min_c = min(G, key=lambda x: x[1])[1]

    GG = [["." for c in range(new_max_c + 1)] for r in range(new_max_r + 1)]

    new_g = deepcopy(GG)
    for i in range(1, len(G)):
        curr, prev = G[i], G[i - 1]
        paint(*curr, *prev, new_g)
    return new_g


def flood(
    G: List[List[str]], start: Tuple[int, int], not_to_search: Set[Tuple[int, int]]
):
    q = deque([start])
    visited = set()
    while q:
        curr = q.popleft()
        if curr in visited or curr in not_to_search:
            continue
        visited.add(curr)
        next_ = [
            (i, j)
            for i, j in all_neighbors(G, *curr)
            if (i, j) not in not_to_search and G[i][j] == "."
        ]
        for n in next_:
            if n not in visited:
                q.append(n)
    return visited


def is_border(G: List[List[str]], i: int, j: int):
    if i in [0, len(G) - 1]:
        return True
    if j in [0, len(G[0]) - 1]:
        return True
    return False


def get_connected_to_border(G):
    border_conn = set()
    for i in range(len(G)):
        for j in range(len(G[0])):
            if is_border(G, i, j) and G[i][j] == "." and (i, j) not in border_conn:
                start = (i, j)
                border_conn |= flood(G, start, border_conn)
    return border_conn


def run(lines):
    new_g = build_grid(lines)
    border_conn = get_connected_to_border(new_g)

    flattened = list(chain.from_iterable(new_g))

    res = len(flattened) - len(border_conn)
    return res


def poly_area(x, y):
    return np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1))) // 2


def runp2(lines):
    gg = {"0": "R", "1": "D", "2": "L", "3": "U"}

    dirs = [(gg[l[-1][-2]], int(l[-1][2:-2], 16), "") for l in lines]
    curr = (0, 0)
    G = [curr]

    b = 0
    for d, n, _ in dirs:
        new_pos = move(*curr, d, n)
        b += n
        G.append(new_pos)
        curr = new_pos

    assert G[-1] == G[0]

    A = int(poly_area(*(zip(*G))))
    insA = A - b // 2 + 1

    out = insA + b
    return out


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

    sample_a_answer = 62
    sample_b_answer = 952408144115

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
    dt = datetime(2023, 12, 18)
    submit_answer(answer_a, "a", dt)
    submit_answer(answer_b, "b", dt)
