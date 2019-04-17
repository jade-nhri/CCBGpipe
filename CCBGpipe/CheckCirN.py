#!/usr/bin/env python3
import sys, os
import subprocess
infile=sys.argv[1]
defrc=10 #default read count=10
minrc=5 #minimum read count=5
d=dict()
f=open(infile)
outfile='temp.seq'
fw=open(outfile,'w')
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
        readcount=defrc
        header=name.split(' ')[0]
        header=header.replace('>','')
        if 'reads' in name:
            tmp=name.split(' ')[2]
            readcount=int(tmp.replace('reads=',''))
        if readcount >= minrc:
            d[header]=seq
            fw.write('>'+header+'\n')
            fw.write(seq+'\n')
f.close()
fw.close()
print ("Running nucmer for checking circularity......")
comm='nucmer '+outfile+' '+outfile+' --coords --nosimplify --maxmatch'
stdout=subprocess.getoutput(comm)
cirset=set()
allset=set()
fw=open('cirseqN.fa','w')
for key in d.keys():
    #print (key)
    allset.add(key)
    seq=d[key]
    slen=int(len(seq))
    comm="grep '"+key+"' out.coords > out.tmp.coords"
    #print (comm)
    stdout=subprocess.getoutput(comm)
    f=open('out.tmp.coords')
    while True:
        for s in f:
            s=s.replace('\n','')
            tmp=s.split('|')[0]
            c2=s.split('|')[1]
            c3=s.split('|')[2]
            c4=s.split('|')[3]
            c5=s.split('|')[4]
            qstart=int(tmp.split()[0])
            qend=int(tmp.split()[1])
            sstart=int(c2.split()[0])
            send=int(c2.split()[1])
            alen=int(c3.split()[0])
            idy=float(c4)
            qid=c5.split('\t')[0]
            qid=qid.replace(' ','')
            sid=c5.split('\t')[1]
            sid=sid.replace(' ','')
            if ((qstart<100) & (qstart!=sstart) & (send>(slen-100)) & (qid==sid)):
                print('{0} with {1} bp is circular'.format(key,slen))
                cirset.add(key)
                fw.write('>'+key+'\n')
                fw.write(seq+'\n')
                break
        break
    f.close()
fw.close()
fw=open('nonCir.fa','w')
noncir=allset-cirset
for key in d.keys():
    if key in noncir:
        print (key+' is non-circular')
        fw.write('>'+key+'\n')
        fw.write(d[key]+'\n')
fw.close()
#subprocess.run('rm out.*', shell=True)
#subprocess.run('rm temp.seq',shell=True)

