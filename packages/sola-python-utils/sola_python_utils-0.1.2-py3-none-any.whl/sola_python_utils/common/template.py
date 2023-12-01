import sys

sys.setrecursionlimit(500000)


def readInt() -> int:
    return int(sys.stdin.readline().rstrip())


def readIntLine() -> list[int]:
    return list(map(int, sys.stdin.readline().rstrip().split()))


def readString() -> str:
    return sys.stdin.readline().rstrip()


def readStringLine() -> list[str]:
    return list(sys.stdin.readline().rstrip().split())
