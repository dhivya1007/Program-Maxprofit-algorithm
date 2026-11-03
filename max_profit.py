"""Max Profit Problem.

Buildings are built one after another (no parallel construction). A building
earns money for every time unit it is operational, i.e. from the moment it
finishes until time n. We try every build order with a memoised DP over the
current time and collect every (T, P, C) mix that reaches the maximum earnings.
"""
import sys
from functools import lru_cache

# name: (build time, earnings per time unit)
BUILDINGS = {"T": (5, 1500), "P": (4, 1000), "C": (10, 2000)}


def max_profit(n):
    @lru_cache(maxsize=None)
    def best(t):
        # Option: stop building from time t onwards.
        top, mixes = 0, {(0, 0, 0)}
        for idx, (build_time, rate) in enumerate(BUILDINGS.values()):
            finish = t + build_time
            if finish >= n:  # would earn nothing
                continue
            gain = (n - finish) * rate
            sub_top, sub_mixes = best(finish)
            total = gain + sub_top
            new = set()
            for m in sub_mixes:
                m = list(m)
                m[idx] += 1
                new.add(tuple(m))
            if total > top:
                top, mixes = total, new
            elif total == top:
                mixes = mixes | new
        return top, frozenset(mixes)

    top, mixes = best(0)
    return top, sorted(mixes, reverse=True)


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else int(input("Time Unit: "))
    earnings, solutions = max_profit(n)
    print(f"Earnings: ${earnings}")
    print("Solutions")
    for i, (t, p, c) in enumerate(solutions, 1):
        print(f"{i}. T: {t} P: {p} C: {c}")


if __name__ == "__main__":
    main()