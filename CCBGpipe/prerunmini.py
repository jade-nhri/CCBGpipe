#!/usr/bin/python3
import subprocess
import sys, os

print ('running minimap2 and miniasm......')
comm='minimap2 -x ava-ont -t32 joinedreads.fastq joinedreads.fastq > mapreads.paf'
#print (comm)
stdout=subprocess.getoutput(comm)
comm='miniasm -f joinedreads.fastq mapreads.paf > assembly.gfa'
#print (comm)
stdout=subprocess.getoutput(comm)
comm='getfa.py assembly.gfa'
#print (comm)
stdout=subprocess.getoutput(comm)
print (stdout)
comm='rm mapreads.paf assembly.gfa'
subprocess.getoutput(comm)
print ('\n')

