
This code helps solving linear minimization problems by the symplex method, as
detailed in

    https://en.wikipedia.org/wiki/Simplex_algorithm

The example given on that page is the following:

----------------------------------------
    Minimize

        Z = − 2 x − 3 y − 4 z

    Subject to

        3 x + 2 y + z ≤ 10
        2 x + 5 y + 3 z ≤ 15
        x, y, z ≥ 0
----------------------------------------

We first add two slack variables x4, x5, to transform the constraints into
equalities, call x, y, z = x1, x2, x3 and get the somewhat standard table with
the cost function to minimize at the bottom, on the 3rd line:


          A1      A2      A3    A4    A5
    1   3 x1  + 2 x2    + x3  + x4         = 10     <-- 1st constraint
    2   2 x1  + 5 x2  + 3 x3        + x5   = 15     <-- 2nd constraint
    3  -2 x1  - 3 x2  - 4 x3                = 0     <-- cost foo, with right-side
                                                        hosting -z0, not z0. Keep
                                                        it in mind, at the end will
                                                        flip sign back!!!

The game is to keep performing more (or less) inspired pivots over certain
row+col entries, thereby reaching different vertices of the symplex, until we
end up in one with all coefs of the cost function postive (implying that a
further incrementation of any coefficient will not lower the cost foo any more),
and that will give us the minimal value.

The goal of this posting, however, is not to go into the theory behind the
algorithm, but to give a tool to play around and experiment with a certain ease
(more so than performing the computations by hand) and presenting the table in
reasonable shape (nicely aligned, and with coefficients as rational numbers) at
each step.

The python code is split in two files, a library called comp_frac.py
(computations with fractions) and the applications file, sample_problems.py,
which uses the library. The lib needs two python packages:

    pandas : for nice tabular display only
    fractions  : for doing fraction instead of floating point arithmetic

To get the start table above and then solve the problem, we import the lib as
cf in the applications file and use it:

----------------------------------------

import comp_frac as cf

# load the input matrix as a list of lists of the coefficients:
a = [[3, 2, 1, 1, 0, 10],
     [2, 5, 3, 0, 1, 15],
     [-2, -3, -4, 0, 0, 0]]

s0 = cf.inittab(a) # s0 is an object holding the first state, this call also displays it

#             A1      A2      A3    A4    A5
#       1   3 x1  + 2 x2    + x3  + x4         = 10
#       2   2 x1  + 5 x2  + 3 x3        + x5   = 15
#       3  -2 x1  - 3 x2  - 4 x3                = 0

# The symplex web page presents a solution reached in one pivot step. That
# could be done too, but we can easily reach the same answer in a few steps:


s1 = cf.xpiv(s0, 1, 1) # pivot s0 state over col=1, row=1 --> 2nd state s1 + display

#          A1         A2         A3        A4    A5
#       1  x1   + 2/3 x2   + 1/3 x3  + 1/3 x4         = 10/3
#       2      + 11/3 x2   + 7/3 x3  - 2/3 x4  + x5   = 25/3
#       3       - 5/3 x2  - 10/3 x3  + 2/3 x4         = 20/3

s2 = cf.xpiv(s1, 2, 2) # pivot s1 state over col=2, row=2 --> 3rd state

#          A1    A2          A3         A4         A5
#       1  x1         - 1/11 x3  + 5/11 x4  - 2/11 x5    = 20/11
#       2      + x2   + 7/11 x3  - 2/11 x4  + 3/11 x5    = 25/11
#       3            - 25/11 x3  + 4/11 x4  + 5/11 x5   = 115/11

# and last two pivots, producing the final 5th state (4th is omitted)
s3 = cf.xpiv(s2, 3, 2) # pivot s2 state over col=3, row=2
s4 = cf.xpiv(s3, 4, 1) # pivot s3 state over col=4, row=1

#              A1         A2    A3    A4        A5
#       1  7/3 x1   + 1/3 x2        + x4  - 1/3 x5    = 5
#       2  2/3 x1   + 5/3 x2  + x3        + 1/3 x5    = 5
#       3  2/3 x1  + 11/3 x2              + 4/3 x5   = 20

----------------------------------------

Finally, all coeffs of the cost function are positive, the current minimal value
is -20 (not 20, we flip the sign!!), reached at x1=x2=x5=0 and x3=x4=5. The min
value, computed from the original expression is Z = − 2 x − 3 y − 4 z = -4 * 5 = -20.

The method followed, hopefully accurately, is described in the 2008 book by
Paul R Thie and Gerard E Keough:
    "An Introduction to Linear Programming and Game Theory"

This example will go first, without the comments, in sample_problems.py.
