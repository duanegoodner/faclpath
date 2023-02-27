from collections import defaultdict


specifics = {"a": 7, "b": 9}
lookup = defaultdict(lambda: 10)
for key, val in specifics.items():
    lookup[key] = val


print(lookup["r"])

