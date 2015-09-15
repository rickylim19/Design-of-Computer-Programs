#! /usr/bin/env python
# -*- coding: utf-8 -*-

def fibonacci():
    """
    generate fibonacci number
    0, 1, 1, 2, 3, 5, 8, 13, ...
    """
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

if __name__ == "__main__":
    f = fibonacci()
    test10 = list(next(f) for n in xrange(10))
    assert test10 == [0,1,1,2,3,5,8,13,21,34] 
    print "test pass"
