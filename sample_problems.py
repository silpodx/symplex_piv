import comp_frac as cf

problem1 = '''
The one described in detail, with comments, in read_me.txt

    Minimize

        Z = − 2 x − 3 y − 4 z

    Subject to

        3 x + 2 y + z ≤ 10
        2 x + 5 y + 3 z ≤ 15
        x, y, z ≥ 0
'''

a = [[3, 2, 1, 1, 0, 10],
     [2, 5, 3, 0, 1, 15],
     [-2, -3, -4, 0, 0, 0]]

s0 = cf.inittab(a)

s1 = cf.xpiv(s0, 1, 1)
s2 = cf.xpiv(s1, 2, 2)
s3 = cf.xpiv(s2, 3, 2)
s4 = cf.xpiv(s3, 4, 1)

# --> min is -20, etc. -------------------------------------------------


problem2 = '''
----------------------------------------
Example 3.5.1 [p.87]  w slack already in
----------------------------------------
Minimize -2 x1 - 3 x2 - 3 x3
Subj to: 3 x1 + 2 x2         + x4           = 60
         - x1 +   x2  + 4 x3      + x5      = 10
         2 x1 - 2 x2  + 5 x3           + x6 = 50
+ all x >= 0.
'''

a = [[3, 2, 0, 1, 0, 0, 60],
     [-1, 1, 4, 0, 1, 0, 10],
     [2, -2, 5, 0, 0, 1, 50],
     [-2, -3, -2, 0, 0, 0, 0]]

s0 = cf.inittab(a)
s1 = cf.xpiv(s0, 2, 2)
s2 = cf.xpiv(s1, 1, 1)

# --> min = -70 at x1=8, x2=18, x3=0 -----------------------------------
