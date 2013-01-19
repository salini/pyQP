#!/usr/bin/env python

from pyQP import solve_qp_as_cvxopt
import numpy as np



def do_test(P,q, G,h, A,b):
    print "-------------------------------------------------------------"
    try:
        x = solve_qp_as_cvxopt(P,q, G,h, A,b)
        print "x", x
        print "cost", np.dot(x, np.dot(P, x)) + np.dot(q, x)
        print " "
    except Exception as e:
        print e, "\n"



P = np.eye(4)

q = np.array([1.,.2, -.2,.1])
G = np.zeros((0, 4))
h = np.zeros(0)
A = np.zeros((0, 4))
b = np.zeros(0)


print "#normal"
do_test(P,q, G,h, A,b)

print "#problem with P, cannot cholesky"
P[0,0] = 0
do_test(P,q, G,h, A,b)

print "#normal with eq const"
P[0,0] = 1
A = np.array([[1,0,0,0],
              [0,1,0,0]])
b = np.array([.4,.4])
do_test(P,q, G,h, A,b)

print "#problem with linearly dependent eq const"
A = np.array([[1,0,0,0],
              [1,0,0,0]])
b = np.array([-.4,-.4])
do_test(P,q, G,h, A,b)


print "#normal with ineq const"
A = np.zeros((0, 4))
b = np.zeros(0)
G = np.array([[0,0,1,0],
              [0,0,0,1]])
h = np.array([-.1, 0.])
do_test(P,q, G,h, A,b)


print "#problem with infeasible problem due to incompatible ineq"
G = np.array([[0,0, 1,0],
              [0,0,-1,0]])
h = np.array([-.1, -.5])
do_test(P,q, G,h, A,b)
#PROBLEM HERE: no excpetion raised, but incompatibilities in ineq const

print "end of test on exceptions"
