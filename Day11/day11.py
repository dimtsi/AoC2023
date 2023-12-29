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
    lines = [list(x) for x in lines]  # type: ignore
    return lines


def manh(p1, p2):
    a_x, a_y = p1
    b_x, b_y = p2
    dist = abs(a_x - b_x) + abs(a_y - b_y)
    return dist


def expand(G):
    G = deepcopy(np.array(G))
    GG = deepcopy(np.array(G))

    inserted = 0
    for i, row in enumerate(G):
        for j, val in enumerate(row):
            if "#" not in row:
                GG = np.concatenate(
                    [
                        GG[: i + 1 + inserted, :],
                        GG[i + inserted, :].reshape(1, -1),
                        GG[i + 1 + inserted :, :],
                    ],
                    axis=0,
                )
                inserted += 1
                break
    inserted = 0
    for j, val in enumerate(G[0]):
        if "#" not in G[:, j]:
            try:
                GG = np.concatenate(
                    [
                        GG[:, : j + 1 + inserted],
                        GG[:, j + inserted].reshape(-1, 1),
                        GG[:, j + 1 + inserted :],
                    ],
                    axis=1,
                )
            except:
                pass
            inserted += 1

    print("".join(x) for x in GG)
    return GG


def run(G):
    G = expand(G)
    gal = set()
    for i in range(len(G)):
        for j in range(len(G[i])):
            if G[i][j] == "#":
                gal.add((i, j))

    DISTS = {}
    for start in gal:
        for target in gal - {start}:
            key = tuple(sorted([start, target]))
            if key not in DISTS:
                DISTS[key] = manh(start, target)
    out = sum(DISTS.values())
    return out


def get_new_locations(G, gals, n):
    G = deepcopy(np.array(G))

    new_gals = {gal: gal for gal in gals}

    empty_r = []
    empty_c = []

    for i, row in enumerate(G):
        if "#" not in row:
            empty_r.append(i)

    for j, val in enumerate(G[0]):
        if "#" not in G[:, j]:
            empty_c.append(j)

    for i, j in gals:
        cols_l = [col for col in empty_c if col < j]
        rows_u = [row for row in empty_r if row < i]

        new_gals[(i, j)] = (i + len(rows_u) * (n - 1), j + len(cols_l) * (n - 1))

    return new_gals


def runp2(G, n):
    gal = set()
    for i in range(len(G)):
        for j in range(len(G[i])):
            if G[i][j] == "#":
                gal.add((i, j))

    new_locs = set(get_new_locations(G, gal, n).values())

    DISTS = {}
    for start in new_locs:
        for target in new_locs - {start}:
            key = tuple(sorted([start, target]))
            if key not in DISTS:
                DISTS[key] = manh(start, target)
    out = sum(DISTS.values())

    return out


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    lines = parse(filename)
    answer_a = run(lines)

    lines = parse(filename)
    answer_b = runp2(lines, n=10 if "sample" in filename else 1_000_000)

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":
    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 374
    sample_b_answer = 1030

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
    dt = datetime(2023, 12, 11)
    submit_answer(answer_a, "a", dt)
    submit_answer(answer_b, "b", dt)
