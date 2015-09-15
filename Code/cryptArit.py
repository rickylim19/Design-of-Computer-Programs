#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Write a function, solve(formula) that solves cryptarithmetic puzzles.
# The input should be a formula like 'ODD + ODD == EVEN', and the 
# output should be a string with the digits filled in, or None if the
# problem is not solvable.

from __future__ import division
import string, re
import itertools
import time

def timedcall(fn, *args):
    """
    Return the time when function finally returns
    """
    t0 = time.clock()
    result = fn(*args)
    t1 = time.clock()
    return t1-t0, result

def timedcalls(n, fn, *args):
    """
    Return the min, avg, max of the time when function is being called n-times
    """
    times = [timedcall(fn, *args)[0] for i in xrange(n)]
    return min(times), average(times), max(times)

def solve(formula):
    """
    Given a formula like 'ODD + ODD == EVEN', fill in digits to solve it.
    Input formula is a string; output is a digit-filled-in string or None.
    """
    for f in fill_in(formula):
        if valid(f):
            #print f
            return f

def fill_in(formula):
    """
    Generate all possible fillings-in of letters in formula with digits.
    """

    letters = ''.join(set(re.findall(r'[A-Z]', formula)))
    for d in itertools.permutations('0123456789', len(letters)):
        table = string.maketrans(letters, ''.join(d))
        yield formula.translate(table)
    
    
def valid(f):
    """
    Formula is valid iff it has no numbers with leading zero, and evals true
    """
    try:
        return not re.search(r'\b0[0-9]', f) and eval(f) is True
    except ArithmeticError:
        return False

def compile_word(word):
    """
    compile a word of uppercase as numeric digits:
    e.g >>>compile_word('YOU') => '(1*U+10*O+100*Y)'
    for non-uppercase words, unchanged:
    e.g >>>compule_word('+') => '(+)'
    """

    if word.isupper():
        compiled_word = ["%s*%c" % (10**i, c) 
                          for i, c in enumerate(word[::-1])]
        return "(" + "+".join(compiled_word) + ")"
    else:
        return word
        
def compile_formula(formula, verbose=False):
    """
    compile formula into a lmabda function, and 
    returns letters found as a str
    e.g >>>compile_formula('YOU == ME**2')
    ('lambda Y,M,E,U,O:(1*U+10*O+100*Y) == (1*E+10*M)**2', 'YMEUO')
    """
    letters = ''.join(set(re.findall(r'[A-Z]', formula)))
    tokens = re.split(r'([A-Z]+)', formula)
    terms = ''.join(map(compile_word, tokens))
    params = ','.join(letters)
    f = 'lambda %s:%s' %(params, terms)
    if verbose: print f
    return eval(f), letters

def faster_solve(formula):
    """
    Input formula is a string
    Output is a digit-filled string or None
    This version the formula is precompile
    """
    f, letters = compile_formula(formula, verbose=True)
    for digits in itertools.permutations((0,1,2,3,4,5,6,7,8,9), len(letters)):
        try:
            if f(*digits) is True:
                table = string.maketrans(letters, ''.join(map(str,digits)))
                return formula.translate(table)
        except ArithmeticError:
            pass
    
examples = """TWO + TWO == FOUR
A**2 + B**2 == C**2
X/X == X
GLITTERS is not GOLD
sum(range(AA)) == BB
ODD + ODD == EVEN
PLUTO not in set([PLANETS])
ONE < TWO < THREE""".splitlines()


def test():
    t0 = time.clock()
    for example in examples:
        print;
        print 13*" ", example
        print "%6.4f sec:  %s" % timedcall(solve, example)
    print "%6.4f tot." % (time.clock()-t0)
    assert compile_word("YOU") == "(1*U+10*O+100*Y)"
    assert compile_word("+") == "+"
    assert faster_solve('ODD+ODD==EVEN') == '655+655==1310'
    print "tests passed"
    
test()
