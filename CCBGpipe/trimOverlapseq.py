#!/usr/bin/python3
import sys, os
import subprocess
infile=sys.argv[1]
names = []
seq = []
f=open(infile)
fw=open('temp.seq','w')
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
        fw.write(name+'\n')
        fw.write(seq+'\n')
f.close()
fw.close()
readcount=0
d1=dict()
f=open('temp.seq')
for i in f:
    if '>' in i:
        header=i.split(' ')[0]
        header=header.replace('>','')
        header=header.replace('\n','')
        if 'reads' in i:
            tmp=i.split(' ')[2]
            readcount=int(tmp.replace('reads=',''))
        d1[header]=''
        continue
    d1[header]+=i
    if readcount==1:
        del d1[header]
f.close()
outfile='temp.seq2'
seqset=set()
fw=open(outfile,'w')
for key in d1.keys():
    fw.write('>'+key+'\n')
    fw.write(d1[key]+'\n')
    seqset.add(key)
fw.close()
print (seqset)
subprocess.run('nucmer {0} {0} --coords --nosimplify --maxmatch'.format(outfile),shell=True)
fw=open('trimmedH.fa','w')
for key in d1.keys():
    seq=d1[key]
    seq=seq.replace('\n','')
    slen=int(len(seq))
    comm="grep '"+key+"' out.coords > temp.coords"
    stdout=subprocess.getoutput(comm)
    f=open('temp.coords')
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
                #print(sstart)
                fw.write('>'+key+'\n')
                fw.write(seq[int(qend/2):]+'\n')
                break
        break
    f.close()
fw.close()
comm='nucmer trimmedH.fa trimmedH.fa --coords --nosimplify --maxmatch'
#print (comm)
stdout=subprocess.getoutput(comm)
d=dict()
f=open('trimmedH.fa')
for i in f:
    if '>' in i:
        header=i.replace('>','')
        header=header.replace('\n','')
        d[header]=''
        continue
    d[header]+=i
f.close()
trimset=set()
fw=open('trimmedseqs.fa','w')
for key in d.keys():
    seq=d[key]
    seq=seq.replace('\n','')
    slen=int(len(seq))
    comm="grep '"+key+"' out.coords > temp.coords"
    stdout=subprocess.getoutput(comm)
    f=open('temp.coords')
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
                seq=seq[:(sstart-1)]
                fw.write('>'+key+' len='+str(len(seq))+'\n')
                fw.write(seq+'\n')
                trimset.add(key)
                break
        break
    f.close()
print (trimset)
for key in seqset-trimset:
    seq=d1[key]
    seq=seq.replace('\n','')
    print (key)
    fw.write('>'+key+' len='+str(len(seq))+'\n')
    fw.write(seq+'\n')
fw.close()
subprocess.run('rm *.coords',shell=True)
subprocess.run('rm out.*', shell=True)

