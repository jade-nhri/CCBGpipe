#!/usr/bin/python3
import subprocess
import sys, os

comm="date '+%Y-%m-%d %H:%M:%S'"
print ('Start at '+subprocess.getoutput(comm))

inpath=sys.argv[1]    #the fast5 foler
gsize=4000000 #default genome size
minbases=1000000    #for removing undesired barcodes
cwd=os.getcwd()
os.chdir(inpath)
#print (os.listdir())
#mydir=['barcode03']
mydir=[x for x in os.listdir() if os.path.isdir(x) and 'barcode' in x]
print (mydir)
for i in mydir:
    comm="cat {0}.txt | awk ".format(i)+"'"+"{"+"sum+=$4"+"}"+" END "+"{"+"print sum"+"}"+"'"
    totalbases=int(subprocess.getoutput(comm))
    if (os.path.exists(i+'/assembly.fa')):
        gsize=os.path.getsize(i+'/assembly.fa')
    amount=int(gsize)*80
    if (totalbases>=minbases):
        comm='GetFastq.py -i {0}.txt -q {0}/ -t {1} -o {2}/{0}/'.format(i,amount,cwd)
        print (comm)
        stdout=subprocess.getoutput(comm)
        print (stdout)
os.chdir(cwd)

comm="date '+%Y-%m-%d %H:%M:%S'"
print ('Finish at '+subprocess.getoutput(comm))

