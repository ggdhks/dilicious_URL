#!/usr/bin/python
# -*- coding: utf-8 -*-


import math
from collections import Counter

''' Calculate the standard value '''
def std(list_):
    if len(list_) > 0:
        return list_.std()  # standard value
    else:
        return 0            # Remove Nan, set Nan to 0


''' Calculate the mean value '''
def ave(list_):
    if len(list_) > 0:
        return list_.mean()  # average value
    else:
        return 0  # Remove Nan, set Nan to 0


''' Count the number of vowels '''
def count_vowels(domain):
    vowels = list('aeiou')
    return sum(vowels.count(i) for i in domain.lower())


''' Count the number of digits '''
def count_digits(domain):
    digits = list('0123456789')
    return sum(digits.count(i) for i in domain.lower())


''' Count the number of repeated letter '''
def count_repeat_letter(domain):
    count = Counter(i for i in domain.lower() if i.isalpha()).most_common()
    cnt = 0
    for letter, ct in count:
        if ct > 1:
            cnt += 1
    return cnt  # 'qwweee' -> 2


''' Count consecutive digit '''
def consecutive_digits(domain):  # e.g., domain = '1233qw13'
    digit_map = [int(i.isdigit()) for i in domain]  # digit_map = [1, 1, 1, 1, 0, 0, 1, 1]
    consecutive = [(k, len(list(g))) for k, g in groupby(digit_map)]  # consecutive = [(1, 4), (0, 2), (1, 2)]
    count_consecutive = sum(j for i, j in consecutive if j > 1 and i == 1)  # count_consecutive = 6
    return count_consecutive


''' Count consecutive consonant '''
def consecutive_consonant(domain):  # e.g., domain = '1233qw13'
    consonant = set(
        ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z'])
    digit_map = [int(i in consonant) for i in domain]  # digit_map = [0, 0, 0, 0, 1, 1, 0, 0]
    consecutive = [(k, len(list(g))) for k, g in groupby(digit_map)]  # consecutive = [(0, 4), (1, 2), (0, 2)]
    count_consecutive = sum(j for i, j in consecutive if j > 1 and i == 1)  # count_consecutive = 2
    return count_consecutive

''' Shannon entropy function '''
def shannon_entropy(string):
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
