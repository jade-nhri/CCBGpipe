#!/usr/bin/env python3
import subprocess
import sys, os
import argparse

parser = argparse.ArgumentParser(
    prog='runmini.py',
    description='''Please run this in the Run folder!''')
args = parser.parse_args()

comm="date '+%Y-%m-%d %H:%M:%S'"
print ('Start at '+subprocess.getoutput(comm))

#mydir=['barcode05','barcode07']
mydir=[x for x in os.listdir() if os.path.isdir(x) and 'barcode' in x]
print (mydir)

for i in mydir:
    if (os.path.isdir(i)):
        os.chdir(i)
        print (i+', running minimap and miniasm......')
        comm='minimap2 -x ava-ont -t32 reads.fastq reads.fastq > mapreads.paf'
        #print (comm)
        stdout=subprocess.getoutput(comm)
        comm='miniasm -f reads.fastq mapreads.paf > assembly.gfa'
        #print (comm)
        stdout=subprocess.getoutput(comm)
        comm='getfa.py assembly.gfa'
        #print (comm)
        stdout=subprocess.getoutput(comm)
        print (stdout)

        print (i+', running minimap and miniasm on A reads......')
        comm='minimap2 -x ava-ont -t32 readsA.fastq readsA.fastq > mapreads.paf'
        #print (comm)
        stdout=subprocess.getoutput(comm)
        comm='miniasm -f readsA.fastq mapreads.paf > assemblyA.gfa'
        #print (comm)
        stdout=subprocess.getoutput(comm)
        comm='getfa.py assemblyA.gfa'
        #print (comm)
        stdout=subprocess.getoutput(comm)
        print (stdout)

        print (i+', running minimap and miniasm on B reads......')
        comm='minimap2 -x ava-ont -t32 readsB.fastq readsB.fastq > mapreads.paf'
        #print (comm)
        stdout=subprocess.getoutput(comm)
        comm='miniasm -f readsB.fastq mapreads.paf > assemblyB.gfa'
        #print (comm)
        stdout=subprocess.getoutput(comm)
        comm='getfa.py assemblyB.gfa'
        #print (comm)
        stdout=subprocess.getoutput(comm)
        print (stdout)
        
        comm='rm mapreads.paf assembly*.gfa'
        subprocess.getoutput(comm)

        os.chdir('../')
        print ('\n')


comm="date '+%Y-%m-%d %H:%M:%S'"
print ('Finish at '+subprocess.getoutput(comm))
