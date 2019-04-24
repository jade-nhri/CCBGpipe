#!/usr/bin/env python3
import os, sys
import subprocess

cwd=os.getcwd()
outfile='download_kp.sh'
outpath='/Run/5171491_kp'
fw=open(os.path.join(cwd,outfile),'w')
fw.write('wget https://ndownloader.figshare.com/files/8812159 -O barcode01.fastq.gz\n')
fw.write('wget https://ndownloader.figshare.com/files/8812162 -O barcode02.fastq.gz\n')
fw.write('wget https://ndownloader.figshare.com/files/8812216 -O barcode06.fastq.gz\n')
fw.write('wget https://ndownloader.figshare.com/files/8812267 -O barcode07.fastq.gz\n')
fw.write('wget https://ndownloader.figshare.com/files/8812273 -O barcode08.fastq.gz\n')
fw.write('wget https://ndownloader.figshare.com/files/8812279 -O barcode10.fastq.gz\n')
fw.write('wget https://ndownloader.figshare.com/files/8812285 -O barcode12.fastq.gz\n')

fw.close()

print ('Downloading ....')
subprocess.call('parallel --jobs 7 --no-notice < {0}/{1}'.format(cwd,outfile), shell=True)
myfile=[x for x in os.listdir() if 'fastq' in x]
print (myfile)
for i in myfile:
    barcode=i.split('.')[0]
    os.makedirs(os.path.join(outpath,barcode))
    comm='gzip -d {0}'.format(i)
    print (comm)
    subprocess.getoutput(comm)
    comm='fqstat.py {0}.fastq'.format(barcode)
    print (comm)
    stdout=subprocess.getoutput(comm)
    print (stdout)
    comm='mv {0}.fastq {1}/{0}/reads.fastq'.format(barcode,outpath)
    print (comm)
    subprocess.getoutput(comm)

comm='rm {0}'.format(outfile)
subprocess.getoutput(comm)
