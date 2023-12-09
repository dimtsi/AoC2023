from collections import deque
from typing import (
    List,
    Tuple,
    Optional,
    Deque,
)
from copy import deepcopy

import re


def parse(filename: str):
    with open(filename, "r") as f:
        lines: List[str] = f.read().strip().split("\n")
    res = []
    for line in lines:
        points = list(map(int, re.findall("-?\d+", line)))
        res.append(points)
    return res


def find_history(l: List[int], p2=False):
    H = [l[:]]

    curr = deepcopy(l)
    while not all(x == 0 for x in curr):
        next_ = [curr[i + 1] - curr[i] for i in range(len(curr) - 1)]
        H.append(next_)
        curr = next_

    i = 1
    if not p2:
        h = list(reversed(H))
        while i < len(h):
            h[i].append(h[i - 1][-1] + h[i][-1])
            i += 1
        return h[-1][-1]
    else:
        h = [deque(hh) for hh in list(reversed(H))]  # type: ignore
        while i < len(h):
            h[i].appendleft(h[i][0] - h[i - 1][0])  # type: ignore
            i += 1
        return h[-1][0]


def run(lines: List[List[int]], p2=False):
    h_s = []
    for line in lines:
        h_s.append(find_history(line, p2))

    res = sum(h_s)
    return res


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    lines = parse(filename)
    answer_a = run(lines)

    if "sample" in filename:
        filename = "sample2.txt"
    lines = parse(filename)
    answer_b = run(lines, p2=True)

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":
    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 114
    sample_b_answer = 2

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

    submit_answer(answer_a, "a")
    submit_answer(answer_b, "b")
