#!/usr/bin/env python3
import os, sys
import subprocess
import shutil
import pandas as pd
import numpy as np
flowcell='FLO-MIN107'
kit='SQK-LSK108'
threads=60

argv=sys.argv
if '-flowcell' in argv:
    flowcell=argv[argv.index('-flowcell')+1]
if '-kit' in argv:
    kit=argv[argv.index('-kit')+1]
if '-t' in argv:
    threads=argv[argv.index('-t')+1]

inpath=os.path.abspath(sys.argv[1])+'/'
outpath=os.path.abspath(sys.argv[2])+'/'

if not os.path.exists(outpath):
    os.mkdir(outpath)

cwd=os.getcwd()
albout=outpath+'albacore/'
data=albout+'sequencing_summary.txt'
outpathq=albout+'workspace/pass/'
rs=4000
readcount=0
fast5dir=outpath+'fast5/'


if os.path.exists(outpath+'copiedfiles.txt'):
    copiedfiles=set(line.strip() for line in open(outpath+'copiedfiles.txt'))
else:
    copiedfiles=set()

bcindex=[]
for i in range (12):
    bcindex.append('barcode'+str(i+1).zfill(2))
bc_rc=dict.fromkeys(bcindex,0)
bc_done=dict.fromkeys(bcindex,False)
satisfied=False
while True:
    fw=open(outpath+'filelist.txt','w')
    for dirpath, dirname, files in os.walk(inpath):
        #print (dirpath)
        #print (dirname)
        fileset=set(files)
        copyingset=fileset.difference(copiedfiles)
        #print ('copyingset:'+str(len(copyingset)))
        count=0
        for f5file in copyingset:
            if (f5file.endswith(".fast5")) & (f5file.startswith("Nanopore") or f5file.startswith("DESKTOP")) & (count<100):
                count+=1
                copiedfiles.add(f5file)
                fw.write(os.path.join(dirpath,f5file)+'\n')
    fw.close()
    print ('processing '+str(len(copiedfiles)))
    if (os.stat(outpath+'filelist.txt').st_size==0):
        break
    #print (len(copiedfiles))
    comm='rm '+albout+' -rf'
    subprocess.getoutput(comm)
    comm='read_fast5_basecaller.py -t '+str(threads)+' -s '+albout+' --flowcell '+flowcell+' --kit '+kit+' --barcoding -o fastq -q 0 < '+outpath+'filelist.txt'
    print (comm)
    stdout=subprocess.getoutput(comm)
    df = pd.read_table(data, index_col='filename')
    if not os.path.exists(fast5dir):
        os.mkdir(fast5dir)
    unibarcode = np.unique(df[['barcode_arrangement']].values)
    fw=open(outpath+'temp.sh','w')
    #print ('writing to temp.sh...')
    for bc in unibarcode:
        if not os.path.exists(fast5dir+'/'+bc) and 'barcode' in bc:
            os.mkdir(fast5dir+'/'+bc)
        if 'barcode' in bc:
            outdf = df[df['barcode_arrangement'] == bc]
            # filter by barcode
            dfset = outdf[['read_id','run_id','sequence_length_template', 'mean_qscore_template']]
            out=dfset[dfset['mean_qscore_template']>7]
            #print (out)
            if not os.path.exists(fast5dir+bc+'.txt'):
                out.to_csv(fast5dir+bc+'.txt',sep='\t')
            else:
                with open(fast5dir+bc+'.txt','a') as f:
                    out.to_csv(f,header=False,sep='\t')
            for i in out.index:
                #print (i)
                comm="grep '{0}' {1}filelist.txt".format(i,outpath)
                #print (comm)
                a=subprocess.getoutput(comm)
                #print (a)
                bc_rc[bc]+=1
                #print (bc_rc)
                dirn=str(int(bc_rc[bc]/rs))
                tmp=bc_rc[bc]%rs
                if tmp < rs:
                    #a=inpath+'*/*/*/'+i
                    b='cp {0} {1}{2}/{3}/'.format(a,fast5dir,bc,dirn)
                    fw.write('{0}\n'.format(b))
            #print (bc_rc)
            os.chdir(fast5dir+bc)
            #print (os.getcwd())
            for i in range(0,int(bc_rc[bc]/rs)+1):
                if not os.path.exists(str(i)):
                    os.mkdir(str(i))
            if os.path.exists(outpathq+bc):
                for fqfile in os.listdir(outpathq+bc):
                    if fqfile.endswith('fastq'):
                        shutil.copy(os.path.join(outpathq+bc,fqfile),'reads.fastq')
                        #print (os.path.join(outpathq+bc,fqfile))
                        comm='cat reads.fastq joinedreads.fastq > temp.fastq'
                        subprocess.getoutput(comm)
                        comm='mv temp.fastq joinedreads.fastq'
                        subprocess.getoutput(comm)
                        comm='rm temp.fastq reads.fastq'
                        subprocess.getoutput(comm)
                comm="grep 'read=' joinedreads.fastq | wc -l"
                print ('How many reads in {0}?'.format(bc))
                print (subprocess.getoutput(comm))
                print ('The total bases are:')
                comm="cat {0}{1}.txt | awk ".format(fast5dir,bc)+"'"+"{"+"sum+=$4"+"}"+" END "+"{"+"print sum"+"}"+"'"
                #print (comm)
                stdout=subprocess.getoutput(comm)
                print (stdout)
                bases=int(stdout)
            if  os.path.getsize('joinedreads.fastq')>400000000 and not os.path.exists('assembly.fa') :
                comm='prerunmini.py'
                subprocess.getoutput(comm)
            if os.path.exists('assembly.fa'):
                if bases > 200*os.path.getsize('assembly.fa'):
                    bc_done[bc]=True                 
            
            satisfied=satisfied*bc_done[bc]
            if satisfied==1 and not os.path.exists('satisfied'):
                fw1=open('../satisfied','w')
                fw1.write('Enough reads for assembly\n')
                fw1.close

        os.chdir("../")
        #print (os.getcwd())

    fw.close()
    #break
    
    #print ('running temp.sh...')
    subprocess.call('parallel --jobs {0} --no-notice < {1}temp.sh'.format(threads,outpath), shell=True)
    subprocess.call('rm {0}temp.sh -rf'.format(outpath),shell=True)

    fw=open('copiedfiles.txt','w')
    fw.write('\n'.join(map(lambda x: str(x),list(copiedfiles))))
    fw.write('\n')
    fw.close()

comm='rm '+albout+' -rf'
subprocess.getoutput(comm)

os.chdir(fast5dir)
fw=open('reads_stats.txt','w')
mydir=[x for x in os.listdir() if os.path.isdir(x) and 'barcode' in x]
for i in mydir:
    os.chdir(i)
    fw.write(os.getcwd()+'\n')
    comm='fqstat.py joinedreads.fastq'
    stdout=subprocess.getoutput(comm)
    fw.write(stdout+'\n')
    os.chdir('..')
os.chdir(cwd)



