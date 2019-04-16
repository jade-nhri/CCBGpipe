#!/usr/bin/python3
import random, sys
size=500000
window=490000
infile=sys.argv[1]
outfile=infile.replace('.','_split.')
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
for key in d.keys():
    print (key)
    print (len(d[key]))
    seqlen=len(d[key])
    print (seqlen)
    if (seqlen>size):
        for i in range(0,seqlen,window):
             print (i)
             header=key+'_'+str(i)+':'+str(i+size)
             print (header)
             fw.write(header+'\n')
             fw.write(d[key][i:i+size]+'\n')
    else:
        fw.write(key+'\n')
        fw.write(d[key]+'\n')
fw.close()

