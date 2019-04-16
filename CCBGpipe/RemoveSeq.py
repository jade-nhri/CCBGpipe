#!/usr/bin/python3
import sys,subprocess,os
import networkx as nx

infile=sys.argv[1]
outfile=sys.argv[2]

if (os.path.getsize(infile)>0):
    d=dict()
    f=open(infile)
    count=0
    for i in f:
         i=i.replace('\n','')
         if '>' in i:
              count+=1
              header=count
              continue
         if d.get(header):d[header]+=i
         else:d[header]=i
    f.close()
    file1=infile.replace('.fa','renamed.fa')
    fw=open(file1,'w')
    for i in d.keys():
        fw.write('>Seq'+str(i)+'_len='+str(len(d[i]))+'\n')
        fw.write(d[i]+'\n')
    fw.close()
    print ("Running nucmer......")
    comm='nucmer '+file1+' '+file1+' --coords --nosimplify --maxmatch'
    stdout=subprocess.getoutput(comm)
    f=open('out.coords')
    data=[]
    while True:
        for s in f:
            if '==' in s:
                break
        for s in f:
            s=s.replace('\n','')
            tmp=s.split('|')[4]
            tmp1=s.split('|')[2]
            alen=int(tmp1.split()[0])
            idy=float(s.split('|')[3])
            p1=tmp.split('\t')[0]
            p1=p1.replace(' ','')
            rlen1=int(p1.split('_len=')[1])
            p2=tmp.split('\t')[1]
            p2=p2.replace(' ','')
            rlen2=int(p2.split('_len=')[1])
            if (p1!=p2 and alen/rlen1>=0.2 and alen/rlen2>=0.2 and alen>=2500 and idy>98):
                data.append((p1,p2))
                #print ('alignment length: {0}; read length 1: {1} read length 2: {2}'.format(alen,rlen1,rlen2))

        break
    f.close()
    f=open(file1)
    d=dict()
    for i in f:
        i=i.replace('\n','')
        if '>' in i:
            header=i.replace('>','')
            continue
        if d.get(header):d[header]+=i
        else:d[header]=i
    f.close()
    seqset=set(d.keys())
    #for i in range(1,len(d)+1):
    #    seqset.add('Seq'+str(i))
    #print (seqset)
    fw=open(outfile,'w')
    #print (data)
    nodeset=set()
    G=nx.Graph()
    G.add_edges_from(data)
    iclust=0
    for connected_component in nx.connected_components(G):
        iclust+=1
    Nclus=iclust
    #print (Nclus)
    iclus=0
    for connected_component in nx.connected_components(G):
        iclus+=1
        fwc=open(infile.replace('.fa','_')+str(iclus)+'.fasta','w')
        temp=connected_component
        nodeset=(nodeset|temp)
        #print (nodeset)
        print(temp)
        nlen=[]
        for node in temp:
            for key in d.keys():
                if str(node) in key:
                   slen=int(key.split('len=')[1])
                   fwc.write('>'+key+'\n')
                   fwc.write(d[key]+'\n')
                   continue
            nlen.append(slen)
        maxlen=max(nlen)
        #print (maxlen)
        fwc.close()
        for i in d.keys():
            if str(maxlen) in i:
               fw.write('>'+i+'\n')
               fw.write(d[i]+'\n')
               break
    fw.close()

    single=seqset-nodeset
    outfiles=outfile.replace('.fa','_s.fa')
    fws=open(outfiles,'w')
    #print (single)
    for i in d.keys():
        if i in single:
            fws.write('>'+i+'\n')
            fws.write(d[i]+'\n')
    fws.close()
    subprocess.run('rm out.*',shell=True)

    if (os.path.getsize(outfiles)>0 and os.path.getsize(outfile)>0):
       comm='AddSeq.py {0} {1} {1}'.format(outfiles,outfile)
       print (comm)
       stdout=subprocess.getoutput(comm)
       print (stdout)

else:
    fw=open(outfile,'w')
    fw.close()

