from typing import (
    List,
    Tuple,
    Dict,
    Optional,
)
import re


def parse(filename: str):
    with open(filename, "r") as f:
        lines: List[str] = f.read().strip().split("\n")

    out = 0
    for l in lines:
        nums = re.findall("\d", l)
        first, last = nums[0], nums[-1]
        joined = "".join([first, last])
        nums_int = int(joined)
        out += nums_int

    return out


def ret_num(num: str, map: Dict[str, int]):
    if num in map:
        return str(map[num])
    else:
        return num


def parse_2(filename: str):
    with open(filename, "r") as f:
        lines: List[str] = f.read().strip().split("\n")

    map_n = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }

    map_m = set(map_n.keys()) | set(str(x) for x in map_n.values())

    repl = []

    for l in lines:
        matches = []
        for i in range(len(l)):
            for m in map_m:
                if l[i:].startswith(m):
                    matches.append(m)

        if matches:
            repl.append(
                [ret_num(matches[0], map_n), ret_num(matches[-1], map_n)]
            )

    new_repl = [int("".join(x)) for x in repl]
    out = sum(new_repl)
    return out


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    answer_a = parse(filename)

    if "sample" in filename:
        filename = "sample2.txt"
    answer_b = parse_2(filename)

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 142
    sample_b_answer = 281

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
