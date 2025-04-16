'''
[+] about computations with fractions, very handy in some circs as for example
    with linear programming and maxi/mini finding around convex bodies of eqns
'''

import pandas as pd
from fractions import Fraction as Fr

# ----------------------------------------------------------------------------
# block about symplex method in linear programming, where pandas are used for
# printing Fr components nicely aligned like a constraints table, which ain't
# of the same kind, all columns, but... they can be done in this environment...
# ----------------------------------------------------------------------------
def vis(f, i): # produce a visual string of the term '+/- f x_i' to be inserted into the pandas display of the system [to look acceptable [darn!!!]]
    '''
    indices begin from 1, 1st will not show sign unless negative! [1st col]
    next cols will show either +/- signs btwn the terms.
    '''
    if f == 0:
        ret = ''
    elif f == 1:
        ret = 'x%d' % i
    elif f == -1:
        ret = '-x%d' % i
    else:
        ret = '%s x%d' % (f, i) # generic form, valid for 1st col, now adjust for next cols
    if len(ret) and i > 1: # add the '+ ' prefix or adj the negative sign...
        if ret[0] != '-':
            ret = '+ ' + ret
        else:
            ret  ='- ' + ret[1:]

    return ret


class FracMat:
    def __init__(self, a):
        self.m = len(a)
        self.n = len(a[0]) - 1
        self.a = []
        for i in range(self.m):
            self.a.append([Fr(x) for x in a[i]])

    def show(self, vb=0):
        tups = []
        for i in range(self.m):
            row = []
            for k in range(self.n): # add the x_k * mat_coeff parts
                row.append(vis(self.a[i][k], k+1))
            row.append(' = %s' % (self.a[i][self.n]))
            tups.append(row)
        print()
        pdf = pd.DataFrame(tups, columns=['A%d' % k for k in range(1, self.n + 1)] + [''])
        pdf.index = pdf.index.values + 1 # make row indices start from 1, as with the col indices.
        if vb: print('='* 30 + ' new problem ' + '='*30)
        print(pdf)


def inittab(a): # get a=list-of-lists like np.array struct [see sample_problems.py]
    s0 = FracMat(a)
    s0.show(vb=1)
    return s0


def piv(a, c, r):
    '''
    pivot over col=c, row=r [both indices starting at 1 ] the previous FracMat
    into a new object of same kind and return it
    '''
    ra = [] # ret-a [after pivoting]
    m, n = a.m, a.n
    ra = [a.a[i] for i in range(m)] # dump all lines of a

    ic, ir = c-1, r-1 # array-idxs to work within ra...
    ri = [ra[ir][k]/ra[ir][ic] for k in range(n+1)] # the i-row to keep var x_ic

    tups = [] # dump all data in here 1st, then...
    for i in range(ir): # subtract ri multiplied by the appropriate factor from row-i, preceding ri:
        row = [ra[i][k] - ra[i][ic]*ri[k] for k in range(n+1)]
        tups.append(row)
    tups.append(ri)
    for i in range(ir+1, m): # subtract ri multiplied by the appropriate factor from row-i, following ri:
        row = [ra[i][k] - ra[i][ic]*ri[k] for k in range(n+1)]
        tups.append(row)

    return FracMat(tups)


def xpiv(a, c, r): # do piv(a, c, r) and also broadcast things and return the result [in 1 call]
    'do piv(a, c, r), return new state and display'
    print('\n... pivot over x%d in eqn %d' % (c, r))
    new_a = piv(a, c, r)
    new_a.show()
    return new_a
