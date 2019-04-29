#!/usr/bin/env python3
import sys, os, subprocess
import pandas as pd
import numpy as np
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-b', help='the path to barcoding_summary.txt',dest="barcoding_summary.txt")
parser.add_argument('-s', help='the path to sequencing_summary.txt',dest='sequencing_summary.txt')
parser.add_argument('-o', help='the path to output',dest='outdir')
args = parser.parse_args()

bcfile='barcoding_summary.txt'
sfile='sequencing_summary.txt'
outdir='outdir'

argv=sys.argv
if '-b' in argv:
    bcfile=argv[argv.index('-b')+1]
    bcfile=os.path.abspath(bcfile)
if '-s' in argv:
    sfile=argv[argv.index('-s')+1]
    sfile=os.path.abspath(sfile)
if '-o' in argv:
    outdir=argv[argv.index('-o')+1]
    outdir=os.path.abspath(outdir)


wd=bcfile.replace('barcoding_summary.txt','')
os.chdir(wd)

df = pd.read_table(bcfile)
unibarcode = np.unique(df[['barcode_arrangement']].values)
bdf=df.set_index('read_id')
sdf=pd.read_table(sfile)
jdf=bdf.join(sdf.set_index('read_id'))
jdf=jdf.reset_index()


for bc in unibarcode:
    if 'barcode' in bc:
        outdf = jdf[jdf['barcode_arrangement'] == bc]
        outdf=outdf[['read_id','run_id','sequence_length_template', 'mean_qscore_template']]
        if not os.path.exists(os.path.join(bc,bc+'.txt')):
           outdf.to_csv(os.path.join(bc,bc+'.txt'),sep='\t')


        readID=np.unique(outdf[['read_id']].values)

        print ('Writing '+bc+'......'+'\n')
        fwi=open(os.path.join(bc,bc+'_readid.tsv'),'w')
        fwi.write('read_id'+'\n')
        for ID in readID:
            fwi.write(ID+'\n')
        fwi.close()
        print (bc+' done!'+'\n')

if not os.path.exists(outdir):
    os.makedirs(outdir)
mydir=[x for x in os.listdir() if os.path.isdir(x) and 'barcode' in x]
print (mydir)


for i in sorted(mydir):
    if not os.path.exists(os.path.join(outdir,i)):
        os.mkdir(os.path.join(outdir,i))
    comm='cat {0}/fastq_runid_*.fastq > {0}/{0}.fastq'.format(i)
    print (comm)
    stdout=subprocess.getoutput(comm)
    comm='cp {0}/{0}.fastq {1}/{0}/joinedreads.fastq'.format(i,outdir)
    print (comm)
    stdout=subprocess.getoutput(comm)
    print (stdout)
    os.chdir(os.path.join(outdir,i))
    print ('Running miniasm...')
    comm='prerunmini.py'
    subprocess.getoutput(comm)
    os.chdir(wd)
    comm='cp {0}/{0}.txt {1}/'.format(i,outdir)
    print (comm)
    stdout=subprocess.getoutput(comm)
    print (stdout)
