#!/usr/bin/env python
# -*- coding: utf-8 -*-

def poker(hands):
    """
    Return a list of best hands
    poker[hand, hand, ...] => [hand, ..]
    """
    return allmax(hands, key = hand_rank)

def allmax(iterable, key = None):
    """
    Return a list of all items equal to the max of the iterable
    """
    result, maxval = [], None
    key = key or (lambda x: x)
    for x in iterable:
        xval = key(x)
        if not result or xval > maxval:
            result, maxval = [x], xval
        elif xval == maxval:
            result.append(x)
    return result

count_rankings = {(5, ): 10, (4, 1): 7, (3, 2): 6, (3, 1, 1): 3,
                  (2, 2, 1): 2, (2, 1, 1, 1, 1): 1, (1, 1, 1, 1, 1): 0}

def hand_rank(hand):
    """
    Return a value indicating the ranking of a hand
    There are 9 ranks (a value of 0-8), the highest is straight flush (sf)
    """

    groups = group(['--23456789TJQKA'.index(r) for r,s in hand])
    counts, ranks = unzip(groups)
    if ranks == (14, 5, 4, 3, 2):
        ranks = (5, 4, 3, 2, 1)
    straight = max(ranks) - min(ranks) == 4 and len(ranks) == 5
    flush = len(set(s for r,s in hand)) == 1
    return max(count_rankings[counts], 4 * straight + 5 * flush), ranks


def group(items):
    """
    Return [(count1, value1), (count2, value2), ...]
    the highest count the first (count1, value1) 
    """
    groups = [(items.count(i), i)for i in set(items)]
    return sorted(groups, reverse=True)

def unzip(pairs):
    """
    [(3,7), (4,8)] => [(3,4), (7,8)]
    """
    return zip(*pairs)
    
def test():
    """
    Test cases for the functions in poker program
    """
    sf = "6C 7C 8C 9C TC".split() # straight flush
    fk = "9D 9H 9S 9C 7D".split() # four of a kind
    fh = "TD TC TH 7C 7D".split() # full house
    tp = "5S 5D 9H 9C 6S".split() # two pair
    s1 = "AS 2S 3S 4S 5C".split() # A-5 straight
    s2 = "2C 3C 4C 5S 6S".split() # 2-6 straight
    ah = "AS 2S 3S 4S 6C".split() # A high
    sh = "2S 3S 4S 6C 7D".split() # 7 high
    assert poker([sf, fk]) == [['6C', '7C', '8C', '9C', 'TC']]
    assert poker([s1, s2]) == [['2C', '3C', '4C', '5S', '6S']]
    print "tests pass"

if __name__ == "__main__":
    test()
