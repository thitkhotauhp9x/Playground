from playground.creators.tool.creator import tool_creator


@tool_creator
def add(a, b):
    return a + b


def main():
    result = add(1, 2)
    print(result)


if __name__ == "__main__":
    main()
