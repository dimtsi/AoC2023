from collections import deque

from typing import (
    List,
    Tuple,
    Dict,
    Optional,
    Deque,
)
from copy import deepcopy


from math import lcm


def parse(filename: str):
    with open(filename, "r") as f:
        instr, rules = f.read().strip().split("\n\n")
    G = {}
    for line in rules.split("\n"):
        id_, neighs = line.split(" = ")
        neighs = neighs[1:-1]
        G[id_] = neighs.split(", ")

    return instr, G


def run(instr: str, G: Dict[str, List[str]]):
    steps = 0
    I = deque(instr)

    curr = "AAA"
    while curr != "ZZZ":
        move = I.popleft()
        I.append(move)

        if move == "L":
            curr = G[curr][0]
        elif move == "R":
            curr = G[curr][1]
        steps += 1

    return steps


def find_period(start: str, I: Deque[str], G: Dict[str, List[str]]) -> List[int]:
    reached_z: List[int] = []
    steps = 0
    curr = start

    while len(reached_z) < 10:  # 10 iterations to validate periodicity during debugging
        move = I.popleft()
        I.append(move)

        if move == "L":
            curr = G[curr][0]
        elif move == "R":
            curr = G[curr][1]

        if curr.endswith("Z"):
            reached_z.append(steps + 1)
        steps += 1
    return reached_z


def runp2(instr: str, G: Dict[str, List[str]]) -> int:

    I = deque(instr)
    starts = [k for k in G if k.endswith("A")]
    periods = []

    for i, start in enumerate(starts):
        reached_z: List[int] = find_period(start, deepcopy(I), G)
        periods.append(reached_z[-1] - reached_z[-2])

    out = lcm(*periods)
    return out


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    instr, G = parse(filename)
    answer_a = run(instr, G)

    if "sample" in filename:
        filename = "sample2.txt"
    instr, G = parse(filename)
    answer_b = runp2(instr, G)

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":
    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 6
    sample_b_answer = 6

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
