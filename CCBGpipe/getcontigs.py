#!/usr/bin/env python3
import subprocess
import os,sys

infile=sys.argv[1]
strpat='c_'
outfile=infile.replace('.fa','cir.fa')

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


fw=open(outfile,'w')
for i in d.keys():
    if strpat in i:
        seq=d[i]
        fw.write(i+'\n')
        fw.write(seq+'\n')
fw.close()



