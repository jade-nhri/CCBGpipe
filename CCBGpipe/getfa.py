#!/usr/bin/env python3
import sys
infile=sys.argv[1]
outfile=infile.replace('gfa','fa')
f=open(infile)
header=[]
seq=[]
for i in f:
    if i.startswith('S'):
        header.append(i.split()[1])
        seq.append(i.split()[2])
f.close()
fw=open(outfile,'w')
for i in range (0, len(header)):
    print ('  '+header[i]+'_len='+str(len(seq[i])))
    fw.write('>'+header[i]+'_len='+str(len(seq[i]))+'\n')
    fw.write(seq[i]+'\n')
fw.close()

