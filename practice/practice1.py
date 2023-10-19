import argparse
from collections.abc import *


def format_number(num: int) -> str:
    """
    Given a non-negative number, return a string with the number formatted with a comma as the
    thousands separator. E.g. 1000000 -> "1,000,000"
    # https://pythonprinciples.com/challenges/Thousands-separator/

    :param num: Non-negative integer to format
    :return: Formatted number string
    """
    if num < 0:
        raise ValueError("Negative number passed to format_number")

    i = 0
    comma = []
    for c in reversed(f"{num}"):
        if i > 0 and i % 3 == 0:
            comma.append(",")
        comma.append(c)
        i += 1

    return "".join(reversed(comma))


def first_recurring_char(s: str) -> str:
    """
    Given a string, write a function “recurring char” to find the strings first recurring character. Return “None” if
    there is no recurring character.

    :param s:
    :return:
    """
    chars = {}
    for ch in s:
        if ch in chars:
            return ch
        else:
            chars[ch] = 1
    return "None"


def sum_to_n(integers: list, n: int) -> Generator[list]:
    """
    Given a list of integers, and an integer N, write a function “sum_to_n” to find all combinations that sum to the
    value N.

    Example:

    sum_to_n([2,3,4], 9) -> [
        [2, 2, 2, 3],
        [2, 3, 4],
        [3, 3, 3]
    ]

    :param integers: The allowable list of addends.
    :param n: The desired sum.
    :return: A generator of lists of the combinations of addends that sum to N.
    """

    def inner_sum_to_n(integers: list,
                       n: int,
                       candidate_sum: int,
                       candidate_index: int,
                       candidate_answer: list) -> Generator[list]:
        """
        Recursive function. This is an inner function because it is not meant to be used outside of `sum_to_n`.

        Given a list `candidate_answer` of integers whose sum is less than N,
         which combinations of integers can cause the sum to equal N?

        :param integers: The allowable list of addends.
        :param n: The desired sum.
        :param candidate_sum: The sum of the current `candidate_answer`
        :param candidate_index: The index in `integers` of the next number to try.
        :param candidate_answer: The current list of addends.
        :return: A generator of lists of the combinations of addends that sum to N.
        """

        for j in range(candidate_index, len(integers)):
            i = integers[j]
            new_sum = candidate_sum + i
            if new_sum > n:
                # since integers is sorted, all future sums will also be > N, so stop inner loop
                break
            if new_sum == n:
                yield candidate_answer + [i]
                # since integers is sorted, all future sums will also be > N, so stop inner loop
                break
            if new_sum < n:
                new_candidate_answer = candidate_answer + [i]
                yield from inner_sum_to_n(integers, n, new_sum, j, new_candidate_answer)

    # Search only integers < N
    to_search = sorted(set([i for i in integers if i <= n]))
    yield from inner_sum_to_n(to_search, n, 0, 0, [])


if __name__ == "__main__":
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("n", help="string to evaluate")
    parser.add_argument("ints", help="comma separated list of ints")
    args = parser.parse_args()

    print(json.dumps(list(sum_to_n([int(s) for s in args.ints.split(",")], int(args.n)))))
