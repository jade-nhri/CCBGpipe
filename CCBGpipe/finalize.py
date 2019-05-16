#!/usr/bin/env python3
import sys, os
import subprocess
import argparse

parser = argparse.ArgumentParser(
    prog='finalize.py',
    description='''Please run this in the Run folder!''')
parser.add_argument('outpath', help='the path to output')
args = parser.parse_args()

outpath=sys.argv[1]
outpath=os.path.abspath(outpath)
comm="date '+%Y-%m-%d %H:%M:%S'"
print ('Start at '+subprocess.getoutput(comm))

comm="iUP.py 100 800 'dnaa taxonomy:bacteria AND reviewed:yes' dnaa dnaa"
print('To download dnaa nucleotides...')
print ('    '+comm)
stdout=subprocess.getoutput(comm)
comm="iUP.py 100 800 'repa taxonomy:bacteria AND reviewed:yes' repa repa"
print('To download repa nucleotides...')
print ('    '+comm)
stdout=subprocess.getoutput(comm)
comm="cat dnaa.nucleotides.fa repa.nucleotides.fa > origin.nuc.fa"
#print (comm)
subprocess.getoutput(comm)
comm="cp origin.nuc.fa /opt/"
#print (comm)
subprocess.getoutput(comm)

comm='rm dnaa.* repa.* origin.*'
subprocess.getoutput(comm)

if not os.path.exists(outpath):
    os.mkdir(outpath)

#mydir=['barcode02','barcode04','barcode12']
mydir=[x for x in os.listdir() if os.path.isdir(x) and 'barcode' in x]

outfile='startfixed.contigs.fa'
print (mydir)
for i in mydir:
    os.chdir(i)
    print (os.getcwd())
    comm='trimOverlapseq.py conseqs.fasta'
    print (comm)
    subprocess.getoutput(comm)
    comm='fixstart.py trimmedseqs.fa'
    print (comm)
    stdout=subprocess.getoutput(comm)
    print (stdout)
    comm='renamefa.py startfixed.fa '+outfile
    print (comm)
    subprocess.getoutput(comm)
    comm='minimap2 -x map-ont -a -t 32 '+outfile+' reads.fastq | samtools view -T '+outfile+' -bS - | samtools sort -T long.bwa -o long.bam -'
    print (comm)
    subprocess.getoutput(comm)
    comm='samtools index long.bam'
    print (comm)
    subprocess.getoutput(comm)
    if '_' in i:
        i=i.split('_')[0]
    
    os.mkdir(os.path.join(outpath,i))
    comm='cp {0} {1}/{2}/'.format(outfile,outpath,i)
    print (comm)
    subprocess.getoutput(comm)
    comm='cp long.bam* {0}/{1}/'.format(outpath,i)
    print (comm)
    subprocess.getoutput(comm)

    comm='cp reads.fastq {0}/{1}'.format(outpath,i)
    print (comm)
    subprocess.getoutput(comm)
    comm='cp fpseq.fa {0}/{1}'.format(outpath,i)
    print (comm)
    subprocess.getoutput(comm)

    os.chdir('../')
    print ('\n')

comm="date '+%Y-%m-%d %H:%M:%S'"
print ('Finish at '+subprocess.getoutput(comm))

