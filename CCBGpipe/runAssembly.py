#!/usr/bin/python3
import subprocess
import sys, os
comm="date '+%Y-%m-%d %H:%M:%S'"
print ('Start at '+subprocess.getoutput(comm))

gsize=4000000 #default genome size
#mydir=['barcode05']
mydir=[x for x in os.listdir() if os.path.isdir(x) and 'barcode' in x]
print (mydir)
for i in mydir:
    print (i)
    os.chdir(i)
    if (os.path.exists('assembly.fa')):
        gsize=os.path.getsize('assembly.fa')

        comm="grep 'c_' assembly.fa | wc -l"
        Ncir=int(subprocess.getoutput(comm))
        print ('Number of circular sequences in assembly.fa: {0}'.format(Ncir))

        comm="grep 'c_' assemblyA.fa | wc -l"
        NcirA=int(subprocess.getoutput(comm))
        print ('Number of circular sequences in assemblyA.fa: {0}'.format(NcirA))

        comm="grep 'c_' assemblyB.fa | wc -l"
        NcirB=int(subprocess.getoutput(comm))
        print ('Number of circular sequences in assemblyB.fa: {0}'.format(NcirB))
 

    if os.path.getsize('readsB.fastq')<os.path.getsize('readsA.fastq'):
        comm='runcanu.py {0}'.format(gsize)
    else:
        if NcirA>Ncir or NcirB>Ncir or Ncir==NcirA==NcirB:
            comm='runcanuAB.py {0}'.format(gsize)
        else:
            comm='runcanu.py {0}'.format(gsize)
    print (comm)
    subprocess.run(comm,shell=True, universal_newlines=True)

    os.chdir('../')

comm="date '+%Y-%m-%d %H:%M:%S'"
print ('Finish at '+subprocess.getoutput(comm))
