import math
from collections.abc import Mapping, Sequence


def hcs[T](items: Sequence[T], probs: Sequence[float]) -> Mapping[T, float]:
    # Highest-Confidence Selection
    if len(items) != len(probs):
        raise ValueError("items and probs must have same length")
    data: dict[T, float] = dict.fromkeys(items, 0.0)

    for item, prob in zip(items, probs):
        data[item] = max(data[item], 100 * math.exp(prob))
    return data


def moe[T](items: Sequence[T], probs: Sequence[float]) -> Mapping[T, float]:
    # Mixture-of-Experts
    if len(items) != len(probs):
        raise ValueError("items and probs must have same length")

    data: dict[T, float] = dict.fromkeys(items, 0.0)

    sum_probs = 0.0
    for item, prob in zip(items, probs):
        data[item] = data[item] + math.exp(prob)
        sum_probs += math.exp(prob)

    # sum_probs = sum(probs)

    for item, prob in data.items():
        data[item] = prob * 100 / sum_probs

    return data


def moe_without_probs[T](items: Sequence[T]) -> Mapping[T, float]:
    data: dict[T, float] = dict.fromkeys(items, 0.0)
    for item in items:
        data[item] += 1
    for item, prob in data.items():
        data[item] = prob * 100 / len(items)
    return data


def poe[T](items: Sequence[T], probs: Sequence[float]) -> Mapping[T, float]:
    # Product of Experts
    if len(items) != len(probs):
        raise ValueError("items and probs must have same length")

    data: dict[T, list[float]] = {item: [] for item in items}

    for item, prob in zip(items, probs):
        data[item].append(math.exp(prob))

    data2: dict[T, float] = dict.fromkeys(data, 0.0)

    sum_probs = 0.0

    for item_, prob_ in data.items():
        data2[item_] = math.prod(prob_)
        sum_probs += data2[item_]

    for item, prob in data2.items():
        data2[item] = prob * 100 / sum_probs

    return data2
