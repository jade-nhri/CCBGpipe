#!/usr/bin/python3
import sys, os
import subprocess
outpath=sys.argv[1]

comm="date '+%Y-%m-%d %H:%M:%S'"
print ('Start at '+subprocess.getoutput(comm))

#mydir=['barcode01']
mydir=[x for x in os.listdir() if os.path.isdir(x) and 'barcode' in x]

outfile='fpseq.fa'
print (mydir)
for i in mydir:
    os.chdir(i)
    print (os.getcwd())
    comm='minimap2 -x map-ont -a -t 32 '+outfile+' reads.fastq | samtools view -T '+outfile+' -bS - | samtools sort -T long.bwa -o long.bam -'
    #print (comm)
    subprocess.getoutput(comm)
    comm='samtools index long.bam'
    #print (comm)
    subprocess.getoutput(comm)
    if '_' in i:
        i=i.split('_')[0]
    os.mkdir(outpath+i)
    comm='cp {0} {1}{2}/'.format(outfile,outpath,i)
    #print (comm)
    subprocess.getoutput(comm)
    comm='cp long.bam* {0}{1}/'.format(outpath,i)
    #print (comm)
    subprocess.getoutput(comm)

    #comm='cp reads.fastq {0}/{1}'.format(outpath,i)
    #print (comm)
    #subprocess.getoutput(comm)
    #comm='cp canu/canu.trimmedReads.fasta {0}/{1}'.format(outpath,i)
    #print (comm)
    #subprocess.getoutput(comm)

    os.chdir('../')
    print ('\n')

comm="date '+%Y-%m-%d %H:%M:%S'"
print ('Finish at '+subprocess.getoutput(comm))

