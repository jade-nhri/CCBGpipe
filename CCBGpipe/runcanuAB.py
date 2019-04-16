#!/usr/bin/python3
import sys, subprocess
import os
Nrun=5    #How many times for assembling 40X-sampling reads
Nsucc=0
Nmaxcanu=0
#canu='/opt/canu-1.7/Linux-amd64/bin/canu'
canu='canu'

comm="grep 'c_' assembly.fa | wc -l"
Ncir=int(subprocess.getoutput(comm))

genomesize=sys.argv[1]
comm=canu+' -p canu -d canu.A genomeSize='+str(genomesize)+' -nanopore-raw readsA.fastq gnuplotTested=true'
print (comm)
subprocess.run(comm, shell=True, universal_newlines=True)
os.chdir('canu.A')
print(os.getcwd())
comm='CheckCirN.py canu.contigs.fasta'
stdout=subprocess.getoutput(comm)
print (stdout)

comm='Checkbam.py cirseqN.fa ../readsA.fastq'
print (comm)
stdout=subprocess.getoutput(comm)
print (stdout)

if (os.path.getsize('cirseqN.fa')>0.95*os.path.getsize('../assembly.fa')):
    Nsucc+=1

if (os.path.exists('canu.trimmedReads.fasta.gz')):
    comm='gzip -d canu.trimmedReads.fasta.gz'
    print (comm)
    stdout=subprocess.getoutput(comm)
os.chdir('..')

comm=canu+' -p canu -d canu.B genomeSize='+str(genomesize)+' -nanopore-raw readsB.fastq gnuplotTested=true'
print (comm)
subprocess.run(comm, shell=True, universal_newlines=True)
os.chdir('canu.B')
print(os.getcwd())
comm='CheckCirN.py canu.contigs.fasta'
stdout=subprocess.getoutput(comm)
print (stdout)

comm='Checkbam.py cirseqN.fa ../readsB.fastq'
print (comm)
stdout=subprocess.getoutput(comm)
print (stdout)

comm="grep '>' cirseqN.fa | wc -l"
Ncanucir=int(subprocess.getoutput(comm))
Nmaxcanu=max(Nmaxcanu,Ncanucir)

if (os.path.getsize('cirseqN.fa')>0.95*os.path.getsize('../assembly.fa')):
    Nsucc+=1

if (os.path.exists('canu.trimmedReads.fasta.gz')):
    comm='gzip -d canu.trimmedReads.fasta.gz'
    print (comm)
    stdout=subprocess.getoutput(comm)
os.chdir('..')
comm='cat canu.B/canu.trimmedReads.fasta canu.A/canu.trimmedReads.fasta > canu.trimmedReads.fasta'
subprocess.getoutput(comm)

bases=int(genomesize)*40
for x in range (1,Nrun+1):
    comm='GetSeqA.py canu.trimmedReads.fasta '+str(bases)
    print (comm)
    subprocess.getoutput(comm)
    comm=canu+' -p canu -d canu.'+str(x)+' -assemble genomeSize='+str(genomesize)+' -nanopore-corrected subreads.fasta gnuplotTested=true'
    print (comm)
    subprocess.run(comm, shell=True, universal_newlines=True)
    wdir='canu.'+str(x)
    os.chdir(wdir)
    print(os.getcwd())
    comm='CheckCirN.py canu.contigs.fasta'
    stdout=subprocess.getoutput(comm)
    print (stdout)
    comm='Checkbam.py cirseqN.fa ../reads.fastq'
    print (comm)
    stdout=subprocess.getoutput(comm)
    print (stdout)

    comm="grep '>' cirseqN.fa | wc -l"
    Ncanucir=int(subprocess.getoutput(comm))
    Nmaxcanu=max(Nmaxcanu,Ncanucir)

    if (os.path.getsize('cirseqN.fa')>0.95*os.path.getsize('../assembly.fa')):
        Nsucc+=1
    os.chdir('..')
    if Nsucc>=3 and Nmaxcanu>=Ncir:
        break

comm='cat canu.*/cirseqN.fa > allcir.fa'
print (comm)
subprocess.getoutput(comm)
comm='RemoveSeq.py allcir.fa canu.cir.fa'
print (comm)
stdout=subprocess.getoutput(comm)
print (stdout)

if (os.path.getsize('canu.cir.fa')<0.95*os.path.getsize('assembly.fa') or Ncir>Nmaxcanu):
#    os.chdir('canu.A')
#    if (os.path.exists('canu.correctedReads.fasta.gz')):
#        comm='gzip -d canu.correctedReads.fasta.gz'
#        print (comm)
#        stdout=subprocess.getoutput(comm)
#    os.chdir('../canu.B')
#    if (os.path.exists('canu.correctedReads.fasta.gz')):
#        comm='gzip -d canu.correctedReads.fasta.gz'
#        print (comm)
#        stdout=subprocess.getoutput(comm)
#    os.chdir('..')
#    
#    comm='cat canu.B/canu.correctedReads.fasta canu.A/canu.correctedReads.fasta > canu.correctedReads.fasta'
#    subprocess.getoutput(comm)

    comm='minimap2 -x map-ont -t32 assembly.fa reads.fastq > mapreads.paf'
    subprocess.getoutput(comm)
    comm='racon -t 32 reads.fastq mapreads.paf assembly.fa > assembly_con.fa'
    subprocess.getoutput(comm)
    comm='split.py assembly_con.fa'
    subprocess.getoutput(comm)

    bases=int(genomesize)*40
    for x in range (Nrun+1,Nrun+Nrun+1):
        comm='GetSeqA.py canu.trimmedReads.fasta '+str(bases)
        print (comm)
        stdout=subprocess.getoutput(comm)
        print (stdout)
        
        comm='cat assembly_con_split.fa >> subreads.fasta'
        subprocess.getoutput(comm)
 
        comm=canu+' -p canu -d canu.'+str(x)+' -assemble genomeSize='+str(genomesize)+' -nanopore-corrected subreads.fasta gnuplotTested=true'
        print (comm)
        subprocess.run(comm, shell=True, universal_newlines=True)
        wdir='canu.'+str(x)
        os.chdir(wdir)
        print (os.getcwd())
        comm='CheckCirN.py canu.contigs.fasta'
        stdout=subprocess.getoutput(comm)
        print (stdout)

        comm='Checkbam.py cirseqN.fa ../reads.fastq'
        print (comm)
        stdout=subprocess.getoutput(comm)
        print (stdout)

        comm="grep '>' cirseqN.fa | wc -l"
        Ncanucir=int(subprocess.getoutput(comm))
        Nmaxcanu=max(Nmaxcanu,Ncanucir)

        if (os.path.getsize('cirseqN.fa')>0.95*os.path.getsize('../assembly.fa')):
            Nsucc+=1

        os.chdir('..')

        if Nsucc>=3 and Nmaxcanu>=Ncir:
            break

    comm='cat canu.*/cirseqN.fa > allcir.fa'
    print (comm)
    subprocess.getoutput(comm)
    comm='RemoveSeq.py allcir.fa canu.cir.fa'
    print (comm)
    stdout=subprocess.getoutput(comm)
    print (stdout)

if not os.path.exists('assembly_con.fa'):
    comm='minimap2 -x map-ont -t32 assembly.fa reads.fastq > mapreads.paf'
    subprocess.getoutput(comm)
    comm='racon -t 32 reads.fastq mapreads.paf assembly.fa > assembly_con.fa'
    subprocess.getoutput(comm)

comm='getcontigs.py assembly_con.fa'
subprocess.getoutput(comm)

comm='AddSeq.py assembly_concir.fa canu.cir.fa fpseq.fa'
print (comm)
stdout=subprocess.getoutput(comm)
print (stdout)


