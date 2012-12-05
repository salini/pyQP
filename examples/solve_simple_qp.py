#!/usr/bin/python
#author=joseph salini
#date=2 dec 2012


################################################################################
#                                                                              #
# This simple example comes from the example in the source code of the         #
# QuadProg++ library.                                                          #
# Here it shows how to use the interface to solve quadratic problems with      #
# python.                                                                      #
#                                                                              #
################################################################################

from pyQP.pyQP import _solve_quadprog, solve_qp, solve_qp_as_cvxopt

#Given:
# G =  4 -2   g0^T = [6 0]
#     -2  4
#
# Solve:
# min f(x) = 1/2 x G x + g0 x
# s.t.
#   x_1 + x_2 - 3  =   0
#
#   x_1            >=  0
#         x_2      >=  0
#   x_1 + x_2 - 2  >=  0
#
# The solution is x^T = [1 2] and f(x) = 12




################################################################################
# Here, we directly use the the quadprog interface.
# The inputs arguments needs to be correctly formated
################################################################################
from numpy import array, zeros, matrix, float64

G   = array([[ 4,-2],
             [-2, 4]], dtype=float64)
g0  = array([6, 0], dtype=float64)

CE_T  = array([[1,1]], dtype=float64).T.copy() # careful, the input argument is transposed
ce0   = array([-3], dtype=float64)

CI_T  = array([[1,0],
             [0,1],
             [1,1]], dtype=float64).T.copy()   # careful, the input argument is transposed
ci0   = array([0,0,-2], dtype=float64)

X = _solve_quadprog(G, g0, CE_T, ce0, CI_T, ci0, g0.shape[0])
print X


################################################################################
# Here, we use solve_qp, which takes more type of arguments as input.
# Its job is to format the arguments correctly, and to use the solver above.
################################################################################
P   = array([[ 4,-2],
             [-2, 4]])
q  = [6, 0]

X = solve_qp(P, q, CE_T, ce0, CI_T, ci0)
print X


################################################################################
# Here, we use solve_qp_as_cvxopt:
# The problem is defined as follows:
#   min (x.T P x + q.T x)
#   s.t.    A x =  b
#           G x <= h
################################################################################
A = [[1,1]]
b = [3]

G = -array([[1,0],
            [0,1],
            [1,1]])
h = -array([0,0,2])

X = solve_qp_as_cvxopt(P, q, G, h, A, b)
print X



