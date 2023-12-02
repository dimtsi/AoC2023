from collections import defaultdict

from typing import (
    List,
    Tuple,
    Dict,
    Optional,
)
from copy import deepcopy


def parse(filename: str):

    with open(filename, "r") as f:
        lines: List[str] = f.read().strip().split("\n")

        G = {}

        for line in lines:
            g_sets = []
            g_id, l_cubes = line.split(": ")
            g_id = g_id.split(" ")[1]
            for g_i in l_cubes.split("; "):
                g_cubes: Dict = defaultdict(lambda: 0)

                for g in g_i.split(", "):
                    n, col = g.split(" ")
                    g_cubes[col] += int(n)

                g_sets.append(deepcopy(g_cubes))

            G[g_id] = deepcopy(g_sets)
        print()

    return G


def part1(G: Dict[str, List[Dict]]):
    MAX_R, MAX_G, MAX_B = 12, 13, 14

    score = 0

    for g_id, g_sets in G.items():
        invalid = False
        for vals in g_sets:
            if (
                vals["red"] > MAX_R
                or vals["green"] > MAX_G
                or vals["blue"] > MAX_B
            ):
                invalid = True
                break
        if not invalid:
            score += int(g_id)

    return score


def part2(G: Dict[str, List[Dict]]):

    score = 0

    for g_id, g_sets in G.items():
        max_red = max([g["red"] for g in g_sets])
        max_green = max([g["green"] for g in g_sets])
        max_blue = max([g["blue"] for g in g_sets])

        power = max_red * max_green * max_blue
        score += power

    return score


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    lines = parse(filename)
    answer_a = part1(deepcopy(lines))
    lines = parse(filename)
    answer_b = part2(deepcopy(lines))

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 8
    sample_b_answer = 2286

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
