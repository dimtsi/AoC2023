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


def get_neighbors(
    matrix: List[List[int]], i: int, j: int, diagonal: bool = False
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
    # diagonal
    if diagonal:
        if i - 1 >= 0 and j - 1 >= 0:
            neighbors.append((i - 1, j - 1))
        if i - 1 >= 0 and j + 1 < num_cols:
            neighbors.append((i - 1, j + 1))
        if i + 1 < num_rows and j - 1 >= 0:
            neighbors.append((i + 1, j - 1))
        if i + 1 < num_rows and j + 1 < num_cols:
            neighbors.append((i + 1, j + 1))
    return neighbors


def get_neighbors_and_values(
    matrix: List[List[int]], i: int, j: int, diagonal=False
) -> Tuple[List[Tuple[int, int]], List[int]]:
    neighbors = get_neighbors(matrix, i, j, diagonal)
    vals = [matrix[x][y] for (x, y) in neighbors]
    return neighbors, vals


def parse(filename: str):
    with open(filename, "r") as f:
        lines: List[str] = f.read().strip().split("\n")
    G = [list(l) for l in lines]
    # list(map(int, re.findall("-?\d+", line)))

    return G


def dijkstra(matrix: List[List[int]], start, max_n):

    visited = set()
    even_visited = set()
    dists = defaultdict(lambda: float("inf"), {start: 0})
    pq = [(0, start)]
    while pq:
        dist, curr = heappop(pq)  # bfs
        if curr in visited:
            continue
        if dist % 2 == 0:
            even_visited.add(curr)
        visited.add(curr)
        dists[curr] = dist

        neighbors = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        for dr, dc in neighbors:
            i, j = curr[0] + dr, curr[1] + dc
            val = matrix[i % len(matrix)][j % len(matrix[0])]
            if val != "#" and dist < max_n and dist + 1 and (i, j) not in visited:
                heappush(pq, (dist + 1, (i, j)))

    out = [(pos, dist) for pos, dist in dists.items() if max_n % 2 == dist % 2]
    return out


def run(lines):
    max_n = 64 if len(lines) >= 100 else 6
    # max_n = 500
    start = None
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] == "S":
                start = (i, j)
                break

    visited = dijkstra(lines, start, max_n)
    out = len(visited)

    return out


def runp2(lines):

    max_n = 26501365
    start = None
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] == "S":
                start = (i, j)
                break

    # Because in the input horizontal/vertical lines from the path are empty,
    # The edge of the diamond will always be reachable for any given garden (diamond shape).
    # This can be solved using a quadratic formula where x, is the number of steps and y is the number of steps found.
    # Sol: ax^2 + bx + c = 0

    size = len(lines)
    edge = size // 2

    # y1 = ((a*0)^2 + (a*0)) + c == c
    # y2 = (a*1^2) + b*1 + c == a + b + c
    # y3 = ((a*2^2) + (b*2) + c = 4a + 2*b + c
    # y1 = c
    # y2 = (a + b + c) => a = y2 - b - c => 4y2 = 4a + 4b + 4c
    # y3 - 4y2 = 2b - 4b -3c => -2b = y3 - 4y2 +3c => b = (y3 -4y2 + 3c) // 2
    y1, y2, y3 = [len(dijkstra(lines, start, edge + i * size)) for i in range(3)]

    c = y1
    b = (4 * y2 - y3 - 3 * c) // 2
    a = y2 - (b + c)

    poly = lambda n: a * (n**2) + b * n + c
    # Check validity
    # assert len(dijkstra(lines, start, edge + 2 * size)) == poly((edge + 2 * size) // size)
    # assert len(dijkstra(lines, start, edge + 3 * size)) == poly((edge + 3 * size) // size)

    res = poly((max_n - edge) // size)
    return res


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    lines = parse(filename)
    answer_a = run(lines)

    filename = "input.txt"
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

    sample_a_answer = 16
    sample_b_answer = 616951804315987

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
    dt = datetime(2023, 12, 21)
    submit_answer(answer_a, "a", dt)
    submit_answer(answer_b, "b", dt)
