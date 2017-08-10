#! /usr/bin/python

import re, string
import sys, os
import itertools

#############
# Calculates the Omega Index as described in Collins and Dent 1988
#############
# Takes two solution files as parameters and compares them. Each file should be delimited by tabs or spaces,
# where the first column contains the object IDs and subsequent columns list the cluster/community IDs for each object, e.g.:
'''
A       1
B       1
C       1
D       1       2
E       2
F       2
G       2
H       3
I       3
J       4
'''
# Note that objects can belong to more than one cluster/community, i.e. overlap is allowed.
# Note also that this is very slow with large networks, e.g. > 2000 objects/nodes, because it involves looking at every pairing of objects (AB, AC, AD...IJ).


# read file
# return dictionary associating objects w/ clusters
def readfile(file):
    f = open(file, 'r')
    scan = f.readlines()
    clustdict = {}
    for eachline in scan:
        eachline = re.sub('\s*\n', '', eachline)
        eachline = re.sub('\s+', '#', eachline)
        newline = eachline.split('#')
        objkey = newline[0]
        clustdict[objkey] = newline[1:]
    return clustdict

# cross-tabulation of # times each pair of objects is clustered together by each solution
# takes two dictionaries associating objects with clusters (two solutions)
# dictionaries have identical keys (objects)
# returns dictionary w/ info on pair clustering for the two solutions
def table(dict1, dict2):

    objects = dict1.keys()
    pairs = itertools.combinations(objects, 2) # every pair of objects

    tabledict = {}

    for p in pairs:

        sol1w1 = dict1[p[0]]
        sol1w2 = dict1[p[1]]
        # number of clusters in which pair is together (solution 1)
        tog1 = len(set(sol1w1) & set(sol1w2))

        sol2w1 = dict2[p[0]]
        sol2w2 = dict2[p[1]]
        # number of clusters in which pair is together (solution 2)
        tog2 = len(set(sol2w1) & set(sol2w2))

        #if sol1w1 == ['0'] or sol1w2 == ['0'] or sol2w1 == ['0'] or sol2w2 == ['0']:
        #    continue
        #else:
        tabledict[p] = (tog1, tog2)

    return tabledict
    
# calculate marginals from the table
# solNumber is the number of the solution (0 or 1)
# returns dictionary of marginals for that solution
def margins(table, solNumber):
    tv = table.values()
    marginals = {}
    d1vals = [e[solNumber] for e in tv]
    for k in list(set(d1vals)):
        marginals[k] = d1vals.count(k)
    return marginals

# uses cross-tabulation to calculate omega index
# returns omega index
def omega(tab):
    sol1 = margins(tab, 0)
    sol2 = margins(tab, 1)

    maxj = min([max(sol1.keys()), max(sol2.keys())])

    agree = 0
    for pair in tab:
        entry = tab[pair]
        if entry[0] == entry[1]:
            agree += 1
    observed = agree * len(tab)
    
    count = -1
    expected = 0
    while count < maxj:
        count += 1
        c1 = sol1[count]
        c2 = sol2[count]
        expected += (c1 * c2)
    num = observed - expected

    den = (len(tab)**2) - expected
    print 'Omega Index: ', float(num) / float(den)


def main():
    if len(sys.argv) < 3:
        print '''
              please supply two solution files as parameters, e.g.
              $ ./omega.py solution1.txt solution2.txt
              '''
    else:
        outfile = sys.argv[1]
        gsfile = sys.argv[2]

        d1 = readfile(outfile)
        d2 = readfile(gsfile)
        tab = table(d1, d2)

        score = omega(tab)


if __name__ == "__main__":
    main()
