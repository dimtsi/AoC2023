import itertools
import math
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


class N:
    def __init__(self, id_, neighs: List):
        self.id_ = id_[1:] if id_[0] in "%&" else id_
        self.t = id_[0] if id_[0] in "%&" else id_
        self.neighs = neighs
        self.sources = []  # type: ignore
        self.status = False
        self.pulse = False
        self.history = []  # type: ignore

    def __repr__(self):
        return f"Node: {self.id_}, status: {self.pulse}"

    def action(self, p, G, q):
        if self.t == "%":
            self.action_ff(p, G, q)
        elif self.t == "&":
            self.action_mem(p, G, q)
        elif self.t == "broadcaster":
            self.action_broadcast(p, G, q)
        elif self.t == "button":
            self.action_button(p, G, q)
        elif self.t in G:
            self.action_output(p, G, q)
        else:
            print(self.t, self.id_)
            raise Exception

    def action_ff(self, p, G, q):
        if not p:
            new_status = not self.status
            sent_pulse = True if new_status else False
            self.status = new_status
            self.pulse = sent_pulse
            for target in self.neighs:
                q.append((self.id_, target, self.pulse))

    def action_mem(self, p, G, q):
        latest_pulses = [G[k].pulse for k in self.sources]
        if all(latest_pulses):
            new_pulse = False
        else:
            new_pulse = True
        for target in self.neighs:
            q.append((self.id_, target, new_pulse))
        self.pulse = new_pulse

    def action_broadcast(self, p, G, q):
        for target in self.neighs:
            q.append((self.id_, target, False))

    def action_button(self, p, G, q):
        q.append((self.id_, "broadcaster", False))

    def action_output(self, p, G, q):
        self.history.append(p)
        self.pulse = p
        # print(f"output: {Counter(self.history)}, {self.history}")


def parse(filename: str):
    with open(filename, "r") as f:
        lines: List[str] = f.read().strip().split("\n")
        # list(map(int, re.findall("-?\d+", line)))
    return lines


def push(G):
    q = deque([("button", "broadcaster", False)])
    history = []
    n_high = 0
    n_low = 0
    while q:
        elem = q.popleft()
        src, target, pulse = elem

        history.append((src, pulse))
        G[target].action(pulse, G, q)
        if pulse:
            n_high += 1
        else:
            n_low += 1
    return n_low, n_high, history


def run(lines):
    G = {}
    for line in lines:
        id_, vals = line.split(" -> ")
        v_l = vals.strip().split(", ")
        kk = id_[1:] if id_[0] in "%&" else id_
        if kk in G:
            raise Exception
        G[kk] = N(id_, v_l)

    # Output modules
    all_neighs = [g.neighs for g in G.values()]
    all_neighs = set(itertools.chain(*all_neighs))
    outbound = set(all_neighs) - set(G.keys())
    for ob in outbound:
        G[ob] = N(ob, [])

    # Add sources for mem modules
    for line in lines:
        id_, vals = line.split(" -> ")
        v_l = vals.strip().split(", ")
        kk = id_[1:] if id_[0] in "%&" else id_
        for v in v_l:
            G[v].sources.append(kk)

    # RUN
    total_low, total_high = 0, 0
    H = []
    for _ in range(1000):
        n_low, n_high, history = push(G)
        total_low += n_low
        total_high += n_high
        H.extend(history)
    res = total_low * total_high

    for line in H[:500]:
        with open("mine.txt", "a") as f:
            f.write(str(line) + "\n")
    return res


def runp2(lines):
    G = {}
    for line in lines:
        id_, vals = line.split(" -> ")
        v_l = vals.strip().split(", ")
        kk = id_[1:] if id_[0] in "%&" else id_
        if kk in G:
            raise Exception
        G[kk] = N(id_, v_l)

    # Output modules
    all_neighs = [g.neighs for g in G.values()]
    all_neighs = set(itertools.chain(*all_neighs))
    outbound = set(all_neighs) - set(G.keys())
    for ob in outbound:
        G[ob] = N(ob, [])

    # Add sources for mem modules
    for line in lines:
        id_, vals = line.split(" -> ")
        v_l = vals.strip().split(", ")
        kk = id_[1:] if id_[0] in "%&" else id_
        for v in v_l:
            G[v].sources.append(kk)

    # RUN
    # rx has a single conjunction source, which in turn has only conjuction sources.
    # We will track periodicity for this particular source's sources
    rx_src = G[G["rx"].sources[0]].sources
    print(rx_src)

    periods = {k: [] for k in rx_src}
    # We must find the periods for all sources and all must be positive

    found = {}

    t = 0
    while True:
        t += 1
        _, _, history = push(G)
        H = set(history)
        for src in rx_src:
            if (src, True) in H:
                periods[src].append(t)

        for src in rx_src:
            if len(periods[src]) > 3 and src not in found:
                last, prev, prev_prev = periods[src][-3:][::-1]
                if last - prev == prev - prev_prev:
                    found[src] = -(last - prev)
        if len(found) == len(rx_src):
            break
    res = math.lcm(*list(found.values()))
    return res


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    lines = parse(filename)
    answer_a = run(lines)

    lines = parse(filename)
    answer_b = runp2(lines) if "sample" not in filename else 1

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":
    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample2.txt"
    input = "input.txt"

    sample_a_answer = 11687500
    sample_b_answer = 1

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
    dt = datetime(2023, 12, 20)
    submit_answer(answer_a, "a", dt)
    submit_answer(answer_b, "b", dt)
