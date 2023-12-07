import functools
import os
from collections import Counter

from typing import (
    List,
    Tuple,
    Optional,
    Generator,
    Iterable,
)
from copy import deepcopy


C = list(reversed(["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]))
R_N = {c: i + 1 for i, c in enumerate(C)}


def parse(filename: str):
    out = []
    with open(filename, "r") as f:
        lines: List[str] = f.read().strip().split("\n")

    for l in lines:
        h, x = l.split(" ")
        out.append([h, int(x)])
    return out


class Hand:
    def __init__(self, id_, bid, original_id):

        self.id_ = id_
        self.original_id = original_id
        # We custom sort to have the count in R_N Poker equality order as well e.g "55KKA" --> [("K", 2), ("5", 2), ("A", 1)]
        self.sorted_cnt: List[Tuple[str, int]] = sorted(
            Counter(id_).most_common(), key=lambda x: (-x[1], -R_N[x[0]])
        )
        self.bid = bid

    def __repr__(self):
        return str(self.sorted_cnt)


def convert_joker(hand: Hand) -> Hand:

    l_id = list(hand.id_)
    if "J" in hand.id_:
        if hand.id_ == "JJJJJ":
            return Hand("AAAAA", hand.bid, hand.original_id)

        l_h = [list(x) for x in hand.sorted_cnt]
        most_freq = l_h[0][0]
        repl_val = most_freq if (most_freq != "J") else l_h[1][0]
        j_idx = l_id.index("J")
        l_id[j_idx] = repl_val
        new_id = "".join(l_id)
        new_hand = Hand(new_id, hand.bid, hand.original_id)
        return convert_joker(new_hand)
    else:
        return hand


def comp_h(H_1: Hand, H_2: Hand) -> int:

    h1, h2 = H_1.sorted_cnt, H_2.sorted_cnt

    # Combo first
    winner = 0
    for i in range((max(len(h1), len(h2)))):
        if h1[i][1] > h2[i][1]:
            winner = 1
            break

        elif h1[i][1] < h2[i][1]:
            winner = -1
            break

    if winner != 0:
        # print(f"comparing {H_1.id_, H_2.id_}: result: {winner} ")
        return winner

    # Kickers
    for i in range(5):
        if R_N[H_1.original_id[i]] > R_N[H_2.original_id[i]]:
            winner = 1
            break

        elif R_N[H_1.original_id[i]] < R_N[H_2.original_id[i]]:
            winner = -1
            break

    if winner == 0:
        assert False
    return winner


def run(lines, p2=False):

    h_s = []
    if p2:
        R_N["J"] = -1
    for id_, b in lines:
        h = Hand(id_, b, id_)
        if p2:
            j_h = convert_joker(h)
            h_s.append(j_h)
        else:
            h_s.append(h)

    s_h = sorted(h_s, key=functools.cmp_to_key(comp_h))
    score = 0
    for i, h in enumerate(s_h, 1):
        score += i * h.bid

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

    sample_a_answer = 6440  # 250634643
    sample_b_answer = 5905

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
