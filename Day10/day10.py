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
    G = [list(l) for l in lines]

    return G


PIPES = {"|", "-", "L", "J", "7", "F"}

BLOCKS = {
    "N": ["-", "L", "J"],
    "S": ["-", "F", "7"],
    "E": ["|", "L", "F"],
    "W": ["|", "J", "7"],
}

N_MOVES = ["L", "J", "|"]
S_MOVES = ["7", "F", "|"]
E_MOVES = ["-", "F", "L"]
W_MOVES = ["-", "7", "J"]


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


def pipe_neighbors(
    G: List[List[str]], i: int, j: int, diagonal: bool = False
) -> List[Tuple[int, int]]:
    neighbors = []

    num_rows = len(G)
    num_cols = len(G[i])
    p = G[i][j]
    # N
    if i - 1 >= 0 and p in N_MOVES:
        targ = G[i - 1][j]
        if targ not in BLOCKS["N"]:
            neighbors.append((i - 1, j))
    # S
    if i + 1 < num_rows and p in S_MOVES:
        targ = G[i + 1][j]
        if targ not in BLOCKS["S"]:
            neighbors.append((i + 1, j))
    # W
    if j - 1 >= 0 and p in W_MOVES:
        targ = G[i][j - 1]
        if targ not in BLOCKS["W"]:
            neighbors.append((i, j - 1))
    # E
    if j + 1 < num_cols and p in E_MOVES:
        targ = G[i][j + 1]
        if targ not in BLOCKS["E"]:
            neighbors.append((i, j + 1))
    return neighbors


def find_loop(G, start):
    steps = 0
    start_neighs = pipe_neighbors(G, *start)
    if start_neighs:
        new_start = start_neighs[0]  # Start on single edge
    else:
        return False, set()
    visited = {new_start}
    path = deque()
    curr = new_start
    found = False
    while steps < 100000 and not found:
        if curr == start:
            return True, path
        visited.add(curr)
        path.append(curr)
        neighs = [n for n in pipe_neighbors(G, *curr) if G[n[0]][n[1]] in PIPES]
        if start in neighs and steps > 0:
            path.appendleft(start)
            return True, path
        if len(neighs) == 0 or set(neighs).issubset(visited):
            return False, path
        for i, j in neighs:
            if (i, j) not in visited and (i, j) != start:
                curr = (i, j)
                steps += 1
                break
    return False, path


def run(G):
    for i in range(len(G)):
        for j in range(len(G[0])):
            if G[i][j] == "S":
                start = (i, j)

    for p in PIPES:
        G[start[0]][start[1]] = p
        is_loop, path = find_loop(G, start)
        if is_loop:
            break

    if not is_loop:
        assert False

    out = len(path) // 2
    return out, G, path


def is_border(G: List[List[str]], i: int, j: int):
    if i in [0, len(G) - 1]:
        return True
    if j in [0, len(G[0]) - 1]:
        return True
    return False


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
            (i, j) for i, j in all_neighbors(G, *curr) if (i, j) not in not_to_search
        ]
        for n in next_:
            if n not in visited:
                q.append(n)
    return visited


def print_g(G: List[List[str]]):
    rows = []
    for i in range(len(G)):
        rows.append("".join(G[i]))

    for row in rows:
        print(row)


def run2(G: List[List[str]], path: List[Tuple[int, int]]):
    LOOP = set(path)

    # Find connected to border
    border_conn: Set[Tuple[int, int]] = set()
    for i in range(len(G)):
        for j in range(len(G[0])):
            if is_border(G, i, j) and (i, j) not in LOOP and (i, j) not in border_conn:
                start = (i, j)
                border_conn |= flood(G, start, LOOP | border_conn)

    for i in range(len(G)):
        for j in range(len(G[1])):
            if (i, j) not in LOOP and G[i][j] in PIPES:
                G[i][j] = "."
        print("".join(G[i]))

    GG = np.array(G)

    BASINS = set()
    for i in range(len(GG)):
        is_encl = False
        for j in range(len(GG[0])):
            if (i, j) in border_conn:
                continue
            val = GG[i][j]
            if val not in PIPES and is_encl and (i, j) not in BASINS:
                basin = flood(G, (i, j), border_conn | LOOP)
                BASINS |= basin
            if val in "|JL":
                is_encl = not is_encl

    out = len(BASINS)
    return out


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    lines = parse(filename)
    answer_a, _, _ = run(lines)

    if "sample" in filename:
        filename = "sample4.txt"
    lines = parse(filename)
    _, GG, pathP = run(lines)
    answer_b = run2(deepcopy(GG), deepcopy(pathP))

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":
    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 8
    sample_b_answer = 10

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
    dt = datetime(2023, 12, 10)
    submit_answer(answer_a, "a", dt)
    submit_answer(answer_b, "b", dt)
