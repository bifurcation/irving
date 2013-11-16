#!/usr/bin/env python

from random import random
from math import floor

# CONFIG

ncandidates = 7
nballots = 275

# CODE
for i in range(nballots):
    ballot = []

    candidates = range(ncandidates)
    while len(candidates) > 0:
        ix = int(floor(random() * len(candidates)))
        ballot.append(candidates[ix])
        del candidates[ix]

    print "{},{}".format(i, ",".join(map(str,ballot)))
