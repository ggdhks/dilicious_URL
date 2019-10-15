#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import pickle

accepted_chars = 'abcdefghijklmnopqrstuvwxyz '
pos = dict([(char, idx) for idx, char in enumerate(accepted_chars)])
'''
{' ': 26, 
 'a': 0, 'c': 2, 'b': 1, 'e': 4, 'd': 3, 'g': 6, 'f': 5, 
 'i': 8, 'h': 7, 'k': 10, 'j': 9, 'm': 12, 'l': 11, 'o': 14, 
 'n': 13, 'q': 16, 'p': 15, 's': 18, 'r': 17, 'u': 20, 
 't': 19, 'w': 22, 'v': 21, 'y': 24, 'x': 23, 'z': 25}
'''

""" Return only the subset of chars from accepted_chars.
    This helps keep the  model relatively small by ignoring punctuation , 
    infrequenty symbols, etc. """


def normalize(line):
    return [c.lower() for c in line if c.lower() in accepted_chars]
    '''
    l = 'Go,ogle'
    normalize(l) =  ['g', 'o', 'o', 'g', 'l', 'e']
    '''


""" Return all n grams from l after normalizing """


def ngram(n, l):
    filtered = normalize(l)  # ['g', 'o', 'o', 'g', 'l', 'e']
    for start in range(0, len(filtered) - n + 1):  # [0,5)
        fssn = filtered[start:start + n]
        '''
        ['g', 'o']
        ['o', 'o']
        ['o', 'g']
        ['g', 'l']
        ['l', 'e']
        '''
        yield ''.join(fssn)
        '''
        go
        oo
        og
        gl
        le
        '''

        '''
        yield: generator 
        https://www.ibm.com/developerworks/cn/opensource/os-cn-python-yield/index.html
        '''

        '''
        join: 

        list=['1','2','3','4','5']
        print(''.join(list)) # 12345

        seq = {'hello':'nihao','good':2,'boy':3,'doiido':4}
        print('-'.join(seq)) #  hello-good-boy-doiido
        '''


""" Return the average transition prob from l through log_prob_mat. """


def avg_transition_prob(l, log_prob_mat):
    log_prob = 0.0
    transition_ct = 0
    for a, b in ngram(2, l):
        log_prob += log_prob_mat[pos[a]][pos[b]]  # 10, 20, 30, 40, 50
        transition_ct += 1  # 1,2,3,4,5
    # The exponentiation translates from log probs to probs.
    return math.exp(log_prob / (transition_ct or 1))  # e^(50/5) = 22026.4657948
    '''
    avg_transition_prob('google', counts)
    22026.4657948

    '''


def train():
    """ Write a simple model as a pickle file """
    k = len(accepted_chars)  # 27
    # Assume we have seen 10 of each character pair.  
    # This acts as a kind of prior or smoothing factor.  
    # This way, if we see a character transition live that we've never observed in the past, 
    # we won't assume the entire string has 0 probability.
    counts = [[10 for i in xrange(k)] for i in xrange(k)]
    '''
    >>>xrange(8)
    xrange(8)
    >>> list(xrange(8))
    [0, 1, 2, 3, 4, 5, 6, 7]
    '''
    '''
    row: 27, column: 27
    [[10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 
     [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 
     [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 
     [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 
     [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 
     [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 
     [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 
     [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 
     [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 
     [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 
     [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 
     [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 
     [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 
     [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 
     [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 
     [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 
     [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 
     [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 
     [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 
     [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 
     [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 
     [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 
     [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 
     [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 
     [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 
     [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 
     [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]]
    '''

    # Count transitions from big text file, taken 
    # from http://norvig.com/spell-correct.html
    for line in open('big.txt'):
        for a, b in ngram(2, line):
            counts[pos[a]][pos[b]] += 1  # counts[6][9] 10+1

    # Normalize the counts so that they become log probabilities.  
    # We use log probabilities rather than straight probabilities to avoid
    # numeric underflow issues with long texts.
    # This contains a justification:
    # http://squarecog.wordpress.com/2009/01/10/dealing-with-underflow-in-joint-probability-calculations/
    for i, row in enumerate(counts):  # i = [0, 27), row = [[10,10, ...], ...]
        s = float(sum(row))  # calculate the sum of row 270
        for j in xrange(len(row)):  # j = [0,27)
            row[j] = math.log(row[j] / s)  # row[j] = log(row[j]/row)

    # Find the probability of generating a few arbitrarily choosen good and
    # bad phrases.
    good_probs = [avg_transition_prob(l, counts) for l in open('good.txt')]
    bad_probs = [avg_transition_prob(l, counts) for l in open('bad.txt')]
    '''
    good_probs
    [0.023938216157629255, 0.04042616464762285, 0.08440340229255157, 0.04781617151196871, 0.03183972300719031, 1.0]
    
    bad_probs
    [0.008561562894460492, 0.01362579078861479, 0.004986258448037159, 0.00661346073476083, 0.013302288260578346]
    '''

    # Assert that we actually are capable of detecting the junk.
    assert min(good_probs) > max(bad_probs)  # 0.023938216157629255 > 0.01362579078861479

    # And pick a threshold halfway between the worst good and best bad inputs.
    thresh = (min(good_probs) + max(bad_probs)) / 2  # 0.018782003473122023
    pickle.dump({'mat': counts, 'thresh': thresh}, open('gib_model.pki', 'wb'))  #


if __name__ == '__main__':
    train()
