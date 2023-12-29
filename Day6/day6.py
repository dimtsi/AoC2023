from functools import reduce
from typing import (
    Tuple,
    Optional,
)


import re
import numpy as np


def parse(filename: str, p2=False):
    with open(filename, "r") as f:
        out = []
        lines = f.read().strip().split("\n")
        for l in lines:
            out.append(list(map(int, re.findall("\d+", l))))
    out = np.array(out).T
    out = [list(x) for x in out]
    if p2:
        with open(filename, "r") as f:
            lines = f.read().strip().split("\n")
        out = [re.findall("\d+", l) for l in lines]
        out = [[int("".join(o)) for o in out]]  # type: ignore

    return out


def run(lines, p2=False):
    res = []
    for d, rec in lines:
        wins = 0
        for i in range(1, d):
            dist = i * (d - i)
            if dist > rec:
                wins += 1

        res.append(wins)

    if p2:
        return res[0]
    else:
        return reduce(lambda x, y: x * y, res)


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    lines = parse(filename)
    answer_a = run(lines)
    lines = parse(filename, p2=True)
    answer_b = run(lines, p2=True)

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":
    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 288
    sample_b_answer = 71503

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
