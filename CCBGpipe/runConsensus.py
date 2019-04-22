#!/usr/bin/env python3
import subprocess
import sys, os
import argparse

parser = argparse.ArgumentParser(
    prog='runConsensus.py',
    description='''Please run this in the Run folder!''')
parser.add_argument('f5path', help='the path to the barcoded folder (i.e. fast5)')
args = parser.parse_args()

fast5dir=sys.argv[1]
cwd=os.getcwd()
os.chdir(fast5dir)
afast5dir=os.getcwd()
os.chdir(cwd)
#mydir=['barcode07']
mydir=[x for x in os.listdir() if os.path.isdir(x) and 'barcode' in x]
print (mydir)
for i in mydir:
    os.chdir(i)
    print (os.getcwd())

    comm='runpolish.py {0}/{1}/ {2} {3} {4}'.format(afast5dir,i,'fpseq.fa','polished.fa','1')
    print (comm)
    subprocess.run(comm,shell=True, universal_newlines=True)
    comm='fixpolish.py 1 polished.fa'
    print (comm)
    stdout=subprocess.getoutput(comm)
    print (stdout)

    comm='runpolish.py {0}/{1}/ {2} {3} {4}'.format(afast5dir,i,'polished.fa','polished2.fa','2')
    print (comm)
    subprocess.run(comm,shell=True, universal_newlines=True)
    comm='fixpolish.py 2 polished2.fa'
    print (comm)
    stdout=subprocess.getoutput(comm)
    print (stdout)

    print ('running racon1...')
    comm='minimap2 -x map-ont -t32 polished2.fa reads.fastq > mapreads.paf'
    print (comm)
    subprocess.getoutput(comm)
    comm='racon -t 32 reads.fastq mapreads.paf polished2.fa > polished_con1.fa'
    print (comm)
    subprocess.getoutput(comm)

    print ('running racon2...')
    comm='minimap2 -x map-ont -t32 polished_con1.fa reads.fastq > mapreads.paf'
    print (comm)
    subprocess.getoutput(comm)
    comm='racon -t 32 reads.fastq mapreads.paf polished_con1.fa > polished_con2.fa'
    print (comm)
    subprocess.getoutput(comm)

    comm='selseqs.py'
    stdout=subprocess.getoutput(comm)


    comm='renamefa.py conseqs.fa myconseqs.fa'
    subprocess.getoutput(comm)


    comm='runpolish.py {0}/{1}/ {2} {3} {4}'.format(afast5dir,i,'myconseqs.fa','polished3.fa','3')
    print (comm)
    subprocess.run(comm,shell=True, universal_newlines=True)
    comm='fixpolish.py 3 polished3.fa'
    print (comm)
    stdout=subprocess.getoutput(comm)
    print (stdout)


    comm='renamefa.py polished3.fa conseqs.fasta'
    print (comm)
    subprocess.getoutput(comm)


    comm='rm plished*'
    print (comm)
    stdout=subprocess.getoutput(comm)

    comm='rm nanopolish.results* -rf'
    print (comm)
    stdout=subprocess.getoutput(comm)

    os.chdir(cwd)

