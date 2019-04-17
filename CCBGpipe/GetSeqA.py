#!/usr/bin/env python3
import random, sys

infile=sys.argv[1]
thr=int(sys.argv[2])

d=dict()
f=open(infile)
def read_fasta(fp):
    name, seq = None, []
    for line in fp:
        line = line.rstrip()
        if line.startswith(">"):
            if name: yield (name, ''.join(seq))
            name, seq = line, []
        else:
            seq.append(line)
    if name: yield (name, ''.join(seq))

with f as fp:
    for name, seq in read_fasta(fp):
        d[name]=seq
f.close()


fw=open('subreads.fasta','w')

seqsum=0
for key in d.keys():
    seq=d[key]
    seqsum=seqsum+int(len(seq))

    fw.write(key+'\n')
    fw.write(seq+'\n')

    if seqsum >= thr:
        print (seqsum)
        break

fw.close()

