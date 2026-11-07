from math import isclose, sqrt


def find_next_square(sq):
    edge_length = sqrt(sq)
    if isclose(edge_length - int(edge_length), 0):
        return int((edge_length + 1) ** 2)
    return -1


def main():
    print(find_next_square(121))
    print(find_next_square(625))
    print(find_next_square(114))


if __name__ == "__main__":
    main()
