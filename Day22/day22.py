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
        lines: List[str] = f.read().strip().split("\n")

    dims = {}
    for i, line in enumerate(lines):
        ns = list(map(int, re.findall("-?\d+", line)))
        coords = list([[ns[0], ns[3]], [ns[1], ns[4]], [ns[2], ns[5]]])
        for c in coords:
            assert c[1] >= c[0]
        dims[chr(i + 65)] = coords

    return dims


def can_fall(id_, G, occ, apply_drop=True, removed=set()):
    xr, yr, zr = G[id_]
    curr_z = min(zr)
    if curr_z == 1:
        return False

    below_ids = occ[curr_z - 1] - removed
    falling = True
    for neigh in below_ids:
        xr_n, yr_n = G[neigh][:2]  # only xys
        if (xr[1] < xr_n[0] or xr[0] > xr_n[1]) or (yr[1] < yr_n[0] or yr[0] > yr_n[1]):
            continue
        else:
            falling = False
            break
    if falling and apply_drop:
        occ[zr[1]].remove(id_)
        occ[curr_z - 1].add(id_)
        G[id_][2] = [zr[0] - 1, zr[1] - 1]
    return falling


def run(G):
    or_g = deepcopy(G)
    # max_x = max(max(v[0]) for v in G.values())
    # max_y = max(max(v[1]) for v in G.values())
    max_z = max(max(v[2]) for v in G.values())

    # min_x = min(min(v[0]) for v in G.values())
    # min_y = min(min(v[1]) for v in G.values())
    # min_z = min(min(v[2]) for v in G.values())

    occ = defaultdict(set)
    for id_, brick in G.items():
        zmin, zmax = brick[2]
        for z in range(zmin, zmax + 1):
            occ[z].add(id_)
    or_occ = deepcopy(occ)
    prev_score = 0
    # Get Stable Positions
    while True:
        score = 0
        for i in range(1, max_z + 1):
            if i in occ and occ[i]:
                ids = list(occ[i])
                for z_id in ids:
                    score += can_fall(z_id, G, occ)
        if score == 0:
            print("no change")
            break

    ans = 0
    for id_ in G.keys():
        minz, maxz = G[id_][2]
        new_occ = deepcopy(occ)
        new_g = deepcopy(G)
        # Remove entry
        new_g.pop(id_)
        for i in range(minz, maxz + 1):
            if id_ not in new_occ[i]:
                assert False
            new_occ[i].remove(id_)
        # Check disintegration
        # print()
        falling = False
        falling_id = None
        for i in range(minz, maxz + 1 + 1):
            ids = list(new_occ[i])
            for z_id in ids:
                if can_fall(z_id, new_g, new_occ, apply_drop=False):
                    falling = True
                    falling_id = z_id
                    break
            if falling:
                break

        # print(falling)
        if falling:
            # print(id_, falling_id)
            continue
        ans += 1

    return ans


def get_parents(G, occ):

    parents = defaultdict(set)
    for id_ in G.keys():
        xr, yr, zr = G[id_]
        if zr[1] == 1 or zr[0] == 1:
            continue
        cands = occ[zr[0] - 1]
        for cand in cands:
            if cand == id_:
                continue
            xr_n, yr_n = G[cand][:2]  # only xys
            if not (
                (xr[1] < xr_n[0] or xr[0] > xr_n[1])
                or (yr[1] < yr_n[0] or yr[0] > yr_n[1])
            ):
                parents[id_].add(cand)

    return parents


def chain_r(parents, G):
    children = defaultdict(set)
    for c, ps in parents.items():
        for p in ps:
            children[p].add(c)

    scores = {}
    for id_ in G.keys():
        removed = set(id_)
        n_removed = 1
        while n_removed > 0:
            n_removed = 0
            for iid in set(G.keys()) - removed:
                if parents[iid] and parents[iid].issubset(removed):
                    n_removed += 1
                    removed.add(iid)
        scores[id_] = deepcopy(removed)
    return scores


def runp2(G):
    or_g = deepcopy(G)
    max_z = max(max(v[2]) for v in G.values())

    occ = defaultdict(set)
    for id_, brick in G.items():
        zmin, zmax = brick[2]
        for z in range(zmin, zmax + 1):
            occ[z].add(id_)

    # Get Stable Positions
    while True:
        score = 0
        for i in range(1, max_z + 1):
            if i in occ and occ[i]:
                ids = list(occ[i])
                for z_id in ids:
                    score += can_fall(z_id, G, occ)
        if score == 0:
            print("no change")
            break
    parents = get_parents(G, occ)
    scores = chain_r(parents, G)

    res = sum([len(x) - 1 for x in scores.values()])
    return res


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

    sample_a_answer = 5
    sample_b_answer = 7

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
    dt = datetime(2023, 12, 22)
    submit_answer(answer_a, "a", dt)
    submit_answer(answer_b, "b", dt)
