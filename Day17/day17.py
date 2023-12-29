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
    out = []
    for line in lines:
        out.append(list(map(int, list(line))))
    return out


def get_neighbors(matrix: List[List[int]], i: int, j: int) -> List[Tuple[int, int]]:
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


def get_neighbors_and_values(
    matrix: List[List[int]], i: int, j: int
) -> Tuple[List[Tuple[int, int]], List[int]]:
    neighbors = get_neighbors(matrix, i, j)
    vals = [matrix[x][y] for (x, y) in neighbors]
    return neighbors, vals


def is_valid_prev(curr: Tuple, prev, origin: Dict[Tuple, Tuple]):
    t = 0

    di, dj = curr[0] - prev[0], curr[1] - prev[1]

    if (curr[0], curr[1]) == (12, 12):
        print()

    while t < 2:
        curr = prev
        if curr not in origin:
            return True
        prev = origin[curr]
        new_di, new_dj = curr[0] - prev[0], curr[1] - prev[1]
        if new_di != di or new_dj != dj:
            return True
        t += 1
    return False


def dijkstra(matrix, start):
    start_loss = 0
    D = defaultdict(lambda: float("inf"))
    pq = [(start_loss, (*start, 0, 0, 0))]
    visited = set()

    res = None

    while pq:
        dist, elem = heappop(pq)
        x, y, di, dj, n = elem

        if (x, y) == (len(matrix) - 1, len(matrix[0]) - 1):
            res = deepcopy(elem), dist
            break

        if elem in visited:
            continue
        visited.add(elem)

        # keep going in curr dir
        if n < 3 and (x + di, y + dj) in get_neighbors(matrix, x, y):
            new_dist, new_state = (
                dist + matrix[x + di][y + dj],
                (x + di, y + dj, di, dj, n + 1),
            )
            if new_state in visited or new_dist >= D[new_state]:
                continue
            else:
                D[new_state] = new_dist
                heappush(pq, (new_dist, new_state))

        # turn
        for i, j in get_neighbors(matrix, x, y):
            ddi, ddj = i - x, j - y
            if (ddi, ddj) != (di, dj) and (ddi, ddj) != (-di, -dj):
                new_dist, new_state = (dist + matrix[i][j], (i, j, ddi, ddj, 1))

                if new_state in visited or new_dist >= D[new_state]:
                    continue
                else:
                    D[new_state] = new_dist
                    heappush(pq, (new_dist, new_state))

    return res


def dijkstra2(matrix, start):
    start_loss = 0
    D = defaultdict(lambda: float("inf"))
    pq = [(start_loss, (*start, 0, 0, 0))]
    visited = set()

    res = None

    while pq:
        dist, elem = heappop(pq)
        x, y, di, dj, n = elem

        if (x, y) == (len(matrix) - 1, len(matrix[0]) - 1) and n >= 4:
            res = deepcopy(elem), dist
            break

        if elem in visited:
            continue
        visited.add(elem)

        # keep going in curr dir
        if n < 10 and (x + di, y + dj) in get_neighbors(matrix, x, y):
            new_dist, new_state = (
                dist + matrix[x + di][y + dj],
                (x + di, y + dj, di, dj, n + 1),
            )
            if new_state in visited or new_dist >= D[new_state]:
                continue
            else:
                D[new_state] = new_dist
                heappush(pq, (new_dist, new_state))
        # turn
        for i, j in get_neighbors(matrix, x, y):
            ddi, ddj = i - x, j - y
            if (
                (di, dj) == (0, 0)
                or (ddi, ddj) != (di, dj)
                and (ddi, ddj) != (-di, -dj)
                and n >= 4
            ):
                new_dist, new_state = (dist + matrix[i][j], (i, j, ddi, ddj, 1))

                if new_state in visited or new_dist >= D[new_state]:
                    continue
                else:
                    D[new_state] = new_dist
                    heappush(pq, (new_dist, new_state))
    return res


def run(G):
    res = dijkstra(G, (0, 0))
    return res[1]


def runp2(G):
    res = dijkstra2(G, (0, 0))
    return res[1]


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

    sample_a_answer = 102
    sample_b_answer = 94

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
    dt = datetime(2023, 12, 17)
    submit_answer(answer_a, "a", dt)
    submit_answer(answer_b, "b", dt)
