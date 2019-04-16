#!/usr/bin/python3
import sys
import numpy as np
infile=sys.argv[1]
slen=[]
d=dict()
f=open(infile)
while True:
    h=f.readline()
    if not h: break
    h=h.replace('\n','')
    rID=h.split()[0]
    rID=rID.replace('@','')
    seq=f.readline().replace('\n','')
    qh=f.readline().replace('\n','')
    qual=f.readline().replace('\n','')
    d[rID]=[]
    d[rID].append(h)
    d[rID].append(seq)
    d[rID].append(qual)
    slen.append(len(seq))
f.close()
print ('Number of reads: {0}'.format(len(slen)))
print ('Total bases: {0} bp'.format(np.sum(slen)))
print ('Mean length: {:0.2f} bp'.format(np.mean(slen)))

