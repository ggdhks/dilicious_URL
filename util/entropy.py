#!/usr/bin/python
# -*- coding: utf-8 -*-


import math
from collections import Counter


def shannon_entropy(string):
    print(string)
    shannon_entropy = 0
    length = 0
    norm_entropy = 0
    if string != '':
        # Length of the domain name, float
        length = float(len(string))
        # Create a new counter from an iterable, their counts from the most common to the least.
        # e.g. ('abcc') -> [('c', 2), ('a', 1), ('b', 1)]
        count = Counter(i for i in string).most_common()
        # Calculate the Shannon Entropy
        shannon_entropy = -sum(j / length * (math.log(j / length)) for i, j in count)
        # norm_entropy = shannon_entropy / length
    return shannon_entropy, length
