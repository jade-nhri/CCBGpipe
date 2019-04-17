#!/usr/bin/env python3
import random, sys
import numpy as np
infile=sys.argv[1]
outfile=sys.argv[2]

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
myseq=[]
mylen=[]
i=0
for key in d.keys():
   i+=1
   myseq.append(d[key])
   mylen.append(-len(d[key]))
k=np.argsort(mylen)

j=0
fw=open(outfile,'w')
for i in k:
   fw.write('>Seq'+str(j+1)+'_len='+str(len(myseq[i]))+'\n')
   fw.write(myseq[i]+'\n')
   j+=1
fw.close()
