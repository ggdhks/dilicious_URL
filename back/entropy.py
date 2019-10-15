#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
1. Linguistic Feature - Feature Engineering
'''
import math
from itertools import groupby
from collections import Counter

''' Calculate the standard value '''


def std(list_):
    if len(list_) > 0:
        return list_.std()  # standard value
    else:
        return 0  # Remove Nan, set Nan to 0


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


def shannonEntropy(domain):
    # Length of the domain name, float
    domainLen = float(len(domain))
    # Create a new counter from an iterable, their counts from the most common to the least. 
    # e.g. ('abcc') -> [('c', 2), ('a', 1), ('b', 1)]
    count = Counter(i for i in domain).most_common()
    # Calculate the Shannon Entropy
    shannon_entropy = -sum(j / domainLen * (math.log(j / domainLen)) for i, j in count)
    return domainLen, count, shannon_entropy


'''
# Test 
if __name__ == "__main__":

    domain = "1233aeeqw13"
    cv = count_vowels(domain)
    cd = count_digits(domain)
    crl = count_repeat_letter(domain)
    cod = consecutive_digits(domain)
    coc = consecutive_consonant(domain)
    l, c, e = shannonEntropy(domain)

    print(cv, cd, crl, cod, coc, l, c, e)   
    # (3, 6, 1, 6, 2, 11.0, [('3', 3), ('e', 2), ('1', 2), ('a', 1), ('q', 1), ('2', 1), ('w', 1)], 1.8462202193216335)
'''
