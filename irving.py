#!/usr/bin/env python

import sys
import re

# IRVing
#
# A simple script for Instant Runoff Voting
#
# Input format is a CSV file:
#  * Each row is one ballot
#  * Column one is the voter name/id
#  * Remaining columns are candidates, in descending 
#    order of preference
#  * Candidates are compared with string equality, 
#    with leading/trailing whitespace stripped
#
# For example, ballots in a bike-shed painting vote could be:
#  Joe,  sky blue, powder blue, antique white, fuchsia
#  Mary, fuchsia, powder blue, sky blue, antique white
#  Bob,  fuchsia, sky blue, powder blue, antique white
# (In which case, the winner would be fuchsia, in the first round)
#
# For simplicity, we require that all ballots have the same 
# number of candidates (i.e., each ballot must rank all candidates.)
# Incomplete ballots are ignored.
#
# The output is a set of human readable election results

# 0. Data structures and utility functions

ballots = []        # Array of candidate ranking arrays (CSV rows without voter ID)
invalid = []        # Invalid ballots
candidates = set()  # Set of candidates in the election
votes = []          # Which candidate each voter is voting for (changes by round)
tallies = []        # The per-candidate tallies for each round
eliminated = []     # Candidates eliminated in each round
winner = ""         # The winning candidate

DEBUG = True
def log(x):
    if DEBUG:
        print x 

# 1. Collect the ballots from the input file

for line in sys.stdin:
    line = line.rstrip()                # Trim endline
    ballot = re.split(r'\s*,\s*', line) # Split on commas+whitespace
    voter_id = ballot[0]
    ballot = ballot[1:]                 # Ignore voter ID

    if len(candidates) == 0:
        candidates = set(ballot)        # Learn candidates from the first ballot
    elif set(ballot) != candidates:     # Thereafter, check that the others are valid
        log("Warning: ballot for voter {} is invalid".format(voter_id))
        invalid.append(ballot)
    else:
        ballots.append(ballot)


# 1. Conduct the election
votes = [0] * len(ballots)
majority = len(ballots) / 2 # NB: integer division
for i in range(len(candidates)-1):
    # Tally the votes
    tally = {}
    for c in candidates - set(eliminated):
        tally[c] = 0
    for i in range(len(votes)):
        tally[ballots[i][votes[i]]] += 1
    tallies.append(tally)
    
    # See if there's a winner
    for c in tally:
        if tally[c] > majority:
            winner = c
            break

    # If not, eliminate the candidate with the least votes...
    eliminee = [c for c in tally if tally[c] == min(tally.values())][0]
    eliminated.append(eliminee)

    # ... and reassign his ballots to the next candidate
    for i in range(len(votes)):
        while ballots[i][votes[i]] in eliminated \
          and votes[i] < len(candidates):
            votes[i] += 1


# 2. Print out election results

print "Total ballots cast  {:6d}".format(len(ballots)+len(invalid))
print "  Valid             {:6d}".format(len(ballots))
print "  Invalid           {:6d}".format(len(invalid))
print
print "The winner is: {}".format(winner)
print

for i in range(len(tallies)):
    print "===== ROUND {} =====".format(i+1)
    print
    
    print "Vote counts:"
    for c in tallies[i]:
        print "  {} {:6d} {:6.2f}%".format(c, tallies[i][c], tallies[i][c] * 100.0 / len(ballots))
    print
    
    if i == len(tallies)-1:
        print "Winner declared: {}".format(winner)
    else:
        print "Eliminated candidate: {}".format(eliminated[i])

    print 
    print




