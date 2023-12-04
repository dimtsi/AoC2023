from typing import (
    List,
    Tuple,
    Optional,
)
import re


def parse(filename: str):
    with open(filename, "r") as f:
        lines: List[str] = f.read().strip().split("\n")

        l = []

        for line in lines:
            id_, cards = line.split(": ")
            all, mine = cards.split(" | ")

            l.append(
                [
                    int(re.findall("\d+", id_)[0]),
                    list(map(int, re.findall("\d+", all))),
                    list(map(int, re.findall("\d+", mine))),
                ]
            )

    return l


def part1(lines: List[List]):
    score = 0
    for id_, all_, mine_ in lines:
        match = set(all_) & set(mine_)

        l_m = len(match) - 1
        if len(match) > 0:
            score += 2**l_m

    return score


def part2(lines: List[List]):
    sack = {}
    for id_, _, _ in lines:
        sack[id_] = 1

    for id_, all_, mine_ in lines:
        match = set(all_) & set(mine_)

        l_m = len(match)
        match_ids = [i for i in range(id_ + 1, id_ + 1 + l_m)]

        for m in match_ids:
            sack[m] += sack[id_]

    score = sum(sack.values())
    return score


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    lines = parse(filename)
    answer_a = part1(lines)
    lines = parse(filename)
    answer_b = part2(lines)

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":
    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 13
    sample_b_answer = 30

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
