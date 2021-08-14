import sys
import os

file_ = sys.argv[1]
lines = None
print file_
with open(file_) as f:
    lines = f.read()
lines = lines.split("\n")

summe = 0
nsum = 0
for line in lines:
    a = line.split(" = ")
    if len(a) == 2:
        summe += int(a[1])
        nsum += 1

print "Counted {0} files with {1} events".format(nsum, summe)
