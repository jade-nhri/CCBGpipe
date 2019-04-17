#!/usr/bin/env python3
import sys, os
import subprocess
infile=sys.argv[1]
readfile=sys.argv[2]

infilesize=os.path.getsize(infile)
print (infilesize)
if infilesize>0:
    d=dict()
    f=open(infile)
    count=0
    for i in f:
         i=i.replace('\n','')
         if '>' in i:
              header=i.replace('>','')
              continue
         if d.get(header):d[header]+=i
         else:d[header]=i
    f.close()
    comm='/opt/graphmap/bin/Linux-x64/graphmap align -r {0} -d {1} --max-error 0.15 -t 32 -o alignments.sam'.format(infile,readfile)
    print (comm)
    subprocess.getoutput(comm)
    comm='samtools view -T {0} -Sb alignments.sam | samtools sort -o alignments.bam'.format(infile)
    print (comm)
    subprocess.getoutput(comm)
    comm='samtools index alignments.bam'
    print (comm)
    subprocess.getoutput(comm)
    comm="samtools depth -a -a alignments.bam | awk '$3'==0 > canu.0depth.txt"
    print(comm)
    subprocess.getoutput(comm)
    for i in d.keys():
        seqlen=len(d[i])
        upperb=seqlen-100
        #print (i)
        contigid=i.split(' ')[0]
        #print (upperb)
        comm="cat canu.0depth.txt | awk '{if ($1~"+contigid+"&&$2<"+str(upperb)+"&&$2>100) print $1,$2,$3}'>tmp."+contigid
        #print (comm)
        subprocess.getoutput(comm)
        comm='cat tmp.* >canu.0depth'
        #print (comm)
        subprocess.getoutput(comm)
        comm='rm tmp.*'
        subprocess.getoutput(comm)

    removkey=[]
    if os.path.getsize('canu.0depth')>0:
        comm="cat canu.0depth | awk 'NR>1{if($2-p==1)print $1,$2,$3}{p=$2}' > canu.0depth1.txt"
        subprocess.getoutput(comm)
        comm="cat canu.0depth1.txt | awk 'NR>1{if($2-p==1)print $1,$2,$3}{p=$2}' > canu.0depth2.txt"
        subprocess.getoutput(comm)
        comm="cat canu.0depth2.txt | awk 'NR>1{if($2-p==1)print $1,$2-3,$S2}{p=$2}' > canu.0depth3.txt"
        subprocess.getoutput(comm)
        if os.path.getsize('canu.0depth3.txt')>0:
            for i in d.keys():
                print (i)
                comm="grep '"+i+"' canu.0depth3.txt -c"
                print (comm)
                stdout=subprocess.getoutput(comm)
                if int(stdout)>2:
                    removkey.append(i)
                    print ('removing {0}'.format(i)) 
                else:
                    comm='rm alignments.*'
                    subprocess.getoutput(comm)
    else:
        comm='rm alignments.*'
        subprocess.getoutput(comm)

    for key in removkey:
        del d[key]
    fw=open(infile,'w')
    for key in d.keys():
        fw.write('>'+key+'\n')
        fw.write(d[key]+'\n')
    fw.close()

