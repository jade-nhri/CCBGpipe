#!/usr/bin/python3
import os, sys
import subprocess
import numpy as np
origin_gene_file='/opt/origin.nuc.fa'
infile=sys.argv[1]
gc_skew_window=500
gc_skew_slide=20
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
    return seq,name
def GC_skew(seq, window, slide):
    pos=[]
    gc_skew=[]
    c_skew=0
    for i in range (0,len(seq),slide):
        posi=i+round(window/2)
        if posi<=len(seq):
            s=seq[i: i+window]
            pos.append(posi)
            g=s.count('G')+s.count('g')
            c=s.count('C')+s.count('c')
            try:
                skew=(g-c)/(g+c)
            except ZeroDivisionError:
                skew=0
            c_skew+=skew
            gc_skew.append(c_skew)
            continue
    gc_skew_max=max(gc_skew)
    gc_skew_min=min(gc_skew)
    ter=pos[gc_skew.index(gc_skew_max)]
    ori=pos[gc_skew.index(gc_skew_min)]
    return ter,ori
def reverse_complement(seq):
    seq=seq.upper()
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'K':'M','M':'K','R':'Y','Y':'R','S':'W','W':'W','B':'V','V':'B','H':'G','D':'C','X':'N','N':'N'}
    bases = list(seq)
    bases = bases[::-1]
    rc=[complement.get(base,base) for base in bases]
    bases = ''.join(rc)
    return bases
f=open(infile)
seqname=[]
seqseq=[]
seqlen=[]
fw=open('temp.seq','w')
orit=[]
tert=[]
with f as fp:
    print ('gc_skew based on '+str(gc_skew_window)+'-bp windows with a '+str(gc_skew_slide)+'-bp sliding step along the sequences......')
    for name ,seq in read_fasta(fp):
        name=name.split()[0]
        name=name.replace('>','')
        seqname.append(name)
        seqseq.append(seq)
        seqlen.append(len(seq))
        ter,ori=GC_skew(seq,gc_skew_window,gc_skew_slide)
        orit.append(ori)
        tert.append(ter)
        fw.write('>'+name+'\n')
        fw.write(seq+'\n')
f.close()
fw.close()
print ('seqname: {0}'.format(seqname))
print ('seqlen: {0}'.format(seqlen))
print ('Origin: {0}'.format(orit))
print ('Terminus: {0}'.format(tert))
print ('Running promer for searching the location of dnaA/repA, then for reverse complement seqs......')
comm='promer '+origin_gene_file+' temp.seq --coords'
stdout=subprocess.getoutput(comm)
fw=open('temp.seq1','w')
for header in seqname:
    comm="grep '"+header+"$' out.coords > out.tmp.coords"
    stdout=subprocess.getoutput(comm)
    f=open('out.tmp.coords')
    while True:
        for s in f:
            s=s.replace('\n','')
            tmp=s.split('|')[0]
            c2=s.split('|')[1]
            c3=s.split('|')[2]
            c4=s.split('|')[3]
            sid=s.split()[-1]
            qstart=int(tmp.split()[0])
            qend=int(tmp.split()[1])
            sstart=int(c2.split()[0])
            send=int(c2.split()[1])
            alen=int(c3.split()[0])
            if ((qstart==1) & (sstart<=send)):
                break
            if  ((qstart<100) & (sstart>=send)):
                namerc=header+'_rc'
                seqrc=reverse_complement(seqseq[seqname.index(header)])
                fw.write('>'+namerc+'\n')
                fw.write(seqrc+'\n')
                continue
        break
fw.close()
d=dict()
f1=open('temp.seq')
f2=open('temp.seq1')
for l in f1:
    l=l.replace('\n','')
    if '>' in l:
        name=l.replace('>','')
        continue
    d[name]=l
for l2 in f2:
    l2=l2.replace('\n','')
    if '>' in l2:
        name=l2.replace('>','')
        n1=name.replace('_rc','')
        if n1 in d:
           print ('Sequence of {0} was reverse complement and replaced'.format(n1))
           del d[n1]
           continue
    d[name]=l2
f1.close()
f2.close()
ori=[]
ter=[]
seqseq=[]
seqname=[]
seqlen=[]
fw=open('temp.seq2','w')
for key in d.keys():
    fw.write('>'+key+'\n')
    fw.write(d[key]+'\n')
    seqname.append(key)
    seqseq.append(d[key])
    seqlen.append(len(d[key]))
    terv,oriv=GC_skew(d[key],gc_skew_window,gc_skew_slide)
    ori.append(oriv)
    ter.append(terv)
fw.close()
print ('seqname: {0}'.format(seqname))
print ('seqlen: {0}'.format(seqlen))
print ('Origin: {0}'.format(ori))
print ('Terminus: {0}'.format(ter))
print ('Running promer for searching the location of dnaA/repA and fixing start......')
comm='promer '+origin_gene_file+' temp.seq2 --coords'
stdout=subprocess.getoutput(comm)
fw=open('startfixed.fa','w')
for header in seqname:
    fixstart=False
    seq=seqseq[seqname.index(header)]
    midp=round(len(seq)/2)
    orip=ori[seqname.index(header)]
    terp=ter[seqname.index(header)]
    comm="grep '"+header+"$' out.coords > out.tmp.coords"
    stdout=subprocess.getoutput(comm)
    f=open('out.tmp.coords')
    while True:
        for s in f:
            print (s)
            s=s.replace('\n','')
            tmp=s.split('|')[0]
            c2=s.split('|')[1]
            c3=s.split('|')[2]
            c4=s.split('|')[3]
            sid=s.split()[-1]
            qstart=int(tmp.split()[0])
            qend=int(tmp.split()[1])
            sstart=int(c2.split()[0])
            send=int(c2.split()[1])
            alen=int(c3.split()[0])
            if ((qstart<100) & (sstart<=send)):
                print ('for {0}'.format(sid))
                print ('dnaA/repA locates in {0}:{1}'.format(sstart-(qstart-1),send))
                orip=sstart-(qstart-1)
                print ('origin was corrected to {0} based on the start poistion of dnaA/repA'.format(sstart-(qstart-1)))
                fixstart=True
                newseq=seq[(orip-1):]+seq[:(orip-1)]
                if 'ATG' not in newseq[0:3]:
                    print ("    fixing strat with 'ATG'")
                    for i in range(5):
                        shift=i-2
                        startseq=seq[(orip-1-shift):(orip-1-shift+3)]
                        if startseq=='ATG':
                            newseq=seq[(orip-1-shift):]+seq[:(orip-1-shift)] #index=position-1
                            print ('    bases were shifted by {0}'.format(shift))
                            break
                break
        break
    if fixstart==False:
        mdis=terp-midp
        newseq=seq[mdis:]+seq[:mdis]
    fw.write('>'+header+'\n')
    fw.write(newseq+'\n')
fw.close()

