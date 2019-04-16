#!/usr/bin/python3
import subprocess

infile1='polished2.fa'
infile2='polished_con2.fa'
outfile='conseqs.fa'

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

comm='CheckCirN.py '+infile1
log1=subprocess.getoutput(comm)
#print (log1)
fw=open('log_fpseq','w')
fw.write(log1)
fw.close()

comm='CheckCirN.py '+infile2
log2=subprocess.getoutput(comm)
#print (log2)

d2=dict()
h2=[]
f2=open(infile2)
with f2 as fp:
    for name,seq in read_fasta(fp):
        header=name.replace('>','')
        d2[header]=seq
        h2.append(header)
    #print (h2)
d1=dict()
h1=[]
f1=open(infile1)
with f1 as fp:
    for name,seq in read_fasta(fp):
        header=name.replace('>','')
        d1[header]=seq
        h1.append(header)
    #print (h1)


line=log2.split('\n')
for i in line:
    if 'non-circular' in i:
        temp=i.split(' ')[0]
        header=temp.split('_C')[0]
        comm="grep '"+header+"' log_fpseq"
        #print (comm)
        line1=subprocess.getoutput(comm)
        #print (line1)
        if 'is circular' in line1:
            #print ('\n')
            #print (header)
            for j in h2:
               if header in j:
                   del d2[j]
            #print (d2.keys())
            for j in h1:
               if header in j:
                   d2[j]=d1[j]
            #print (d2.keys())    

fw=open(outfile,'w')
for i in d2.keys():
    fw.write('>'+i+'\n')
    fw.write(d2[i]+'\n')
fw.close()    
