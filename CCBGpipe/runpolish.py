#!/usr/bin/env python3
import os,sys,time
import subprocess

fast5dir=sys.argv[1]
infile=sys.argv[2]
outfile=sys.argv[3]
label=sys.argv[4]

myTime=time.strftime('%m-%d %H:%M:%S',time.localtime(time.time()))
print (myTime)

comm='cp {0} draft.fa'.format(infile)
print (comm)
subprocess.getoutput(comm)

print(os.getcwd())

if label=='1':
    #comm="sed -n '1~4s/^@/>/p;2~4p' < reads.fastq > reads.fasta"
    comm='nanopolish index -d {0} reads.fastq'.format(fast5dir)
    print (comm)
    stdout=subprocess.getoutput(comm)

comm='minimap2 -x map-ont -a -t 32 draft.fa reads.fastq.index | samtools sort -o reads.sorted{0}.bam -T reads.tmp -'.format(label)
print (comm)
stdout=subprocess.getoutput(comm)
#print (stdout)

comm='samtools index reads.sorted{0}.bam'.format(label)
print (comm)
stdout=subprocess.getoutput(comm)



comm='python /opt/nanopolish/scripts/nanopolish_makerange.py draft.fa | parallel --results nanopolish.results'+label+' -P 8 \
nanopolish variants --methylation-aware dcm,dam --consensus plished'+label+'.{1}.fa -w {1} -r reads.fastq -b reads.sorted'+label+'.bam -g draft.fa -t 4 --min-candidate-frequency 0.1'

print (comm)
stdout=subprocess.getoutput(comm)

comm='python /opt/nanopolish/scripts/nanopolish_merge.py plished{0}.*.fa > {1}'.format(label,outfile)
print (comm)
stdout=subprocess.getoutput(comm)

#comm='rm plished.*'
#print (comm)
#stdout=subprocess.getoutput(comm)

#comm='rm draft.fa*'
#print (comm)
#stdout=subprocess.getoutput(comm)

#comm='rm nanopolish.results -rf'
#print (comm)
#stdout=subprocess.getoutput(comm)

myTime=time.strftime('%m-%d %H:%M:%S',time.localtime(time.time()))
print (myTime)

