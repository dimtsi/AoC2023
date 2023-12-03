from functools import reduce
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

    G = [list(line) for line in lines]

    return G


def get_neighbors(matrix: List[List[int]], i: int, j: int) -> List[Tuple[int, int]]:
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
    if i - 1 >= 0 and j - 1 >= 0:
        neighbors.append((i - 1, j - 1))
    if i - 1 >= 0 and j + 1 < num_cols:
        neighbors.append((i - 1, j + 1))
    if i + 1 < num_rows and j - 1 >= 0:
        neighbors.append((i + 1, j - 1))
    if i + 1 < num_rows and j + 1 < num_cols:
        neighbors.append((i + 1, j + 1))
    return neighbors


def run(G, p2=False):
    G = deepcopy(G)
    PART_NUMS = []
    P: Dict[str, Tuple[List[Tuple], int]] = {}
    # for every part num key= {id: [position_idxs: List[Tuple], number_val: int]}

    id_cnt = 0
    for i in range(len(G)):
        # Reset at every row
        is_part = False
        curr_digits = []
        curr_num_idxs = []

        for j in range(len(G)):
            val = G[i][j]
            # Digit
            if G[i][j].isdigit():
                curr_digits.append(val)
                curr_num_idxs.append((i, j))
                if not is_part:
                    for ii, jj in get_neighbors(G, i, j):
                        # if symbol --> IS PART NUMBER and stop search for neighbors in subsequent digits
                        if G[ii][jj] != "." and not G[ii][jj].isdigit():
                            is_part = True
                            break
            # Else
            else:
                # If previous is number stop search and cache number if it is a part number
                if j > 0 and G[i][j - 1].isdigit():
                    joined_num = int("".join(curr_digits))
                    if is_part:
                        PART_NUMS.append(joined_num)
                        P[f"P{id_cnt}"] = curr_num_idxs, joined_num
                        id_cnt += 1
                curr_digits = []
                curr_num_idxs = []
                is_part = False

        # Handle edge case --> Part number at the end of the line
        last = G[i][len(G[i]) - 1]
        if last.isdigit():
            joined_num = int("".join(curr_digits))
            if is_part:
                PART_NUMS.append(joined_num)
                P[f"P{id_cnt}"] = curr_num_idxs, joined_num
                id_cnt += 1

    if not p2:
        return sum(PART_NUMS)

    # P2
    # Construct new grid by replacing part numbers with their ID
    GG = deepcopy(G)
    for id_, (poss, val) in P.items():
        for ii, jj in poss:
            GG[ii][jj] = id_

    # Find gears and calculate score
    score = 0
    for i in range(len(GG)):
        for j in range(len(GG[i])):
            curr = GG[i][j]

            if curr == "*":
                neighs = get_neighbors(GG, i, j)

                parts = set()
                for ii, jj in neighs:
                    val = GG[ii][jj]
                    if val.startswith("P"):
                        parts.add(val)

                if len(parts) == 2:
                    nums = [P[n][1] for n in parts]
                    score += reduce(lambda x, y: x * y, nums)

    print(score)
    return score


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    lines = parse(filename)
    answer_a = run(lines)
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

    sample_a_answer = 4361
    sample_b_answer = 467835

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
