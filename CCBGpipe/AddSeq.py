#!/usr/bin/python3
import sys,subprocess
import numpy as np

file1=sys.argv[1] #miniasm
file2=sys.argv[2]
outfile=sys.argv[3]

d1=dict()
f=open(file1)
print ("Adding A to B...")
print ("A assembly contains:")
for i in f:
    i=i.replace('\n','')
    if '>' in i:
        header=i.replace('>','')
        header=header.split()[0]
        print (header)
        continue
    d1[header]=i
f.close()

alen=[]
d2=dict()
f=open(file2)
print ("B assembly contains:")
for i in f:
    i=i.replace('\n','')
    if '>' in i:
        header=i.replace('>','')
        header=header.split()[0]
        print (header)
        continue
    d2[header]=i
    alen.append(len(d2[header]))
mlen=max(alen)
print('The maximum length of original assembly: '+str(mlen))
f.close()

print ("Running nucmer......")
comm='nucmer '+file1+' '+file2+' --coords --nosimplify --maxmatch'
stdout=subprocess.getoutput(comm)

dnew=d2.copy()
for key in d1.keys():
    molapr=0
    mlen2=0
    addlen=1
    len1=len(d1[key])
    print (key,len1)
    comm="grep '"+key+"[[:space:]]' out.coords > temp.coords"
    #print (comm)
    stdout=subprocess.getoutput(comm)
    #f=open('temp.coords')
    comm="awk '{print $13}' temp.coords | sort -u"
    s2header=subprocess.getoutput(comm)
    temph=[]
    #print (s2header)
    #print (s2header.split())
    temph=s2header.split()
    #print (temph)
    for s2 in temph:
        comm="grep '"+s2+"$' temp.coords > temp2.coords"
        #print ("   "+comm)
        stdout=subprocess.getoutput(comm)
        len2=len(d2[s2])
        print ("   "+s2,len2)
        coords=np.zeros(len2)
        f=open("temp2.coords")
        for i in f:
            #print (i)
            tmp=i.split('|')[1]
            s2start=int(tmp.split()[0])
            s2end=int(tmp.split()[1])
            s2s=min(s2start,s2end)
            s2e=max(s2start,s2end)
            #print (s2s,s2e)
            coords[s2s:(s2e+1)]=1
        #print (coords)
        olapr=sum(coords==1)/len2
        if (len1>sum(coords==1) and olapr<0.9):
            addlen1=1
        else:
            addlen1=0
        addlen=addlen*addlen1
        molapr=max(olapr,molapr)
        mlen2=max(len2,mlen2)
        print ("   "+str(olapr))
        if (len1>len2*1.2) & (olapr>0.9):
           del(dnew[s2])
           print ("   "+s2+' was deleted')
           dnew[key]=d1[key]
           print ("   "+key+' was added')
        f.close()
    if molapr<0.2 and len1>mlen2:
        dnew[key]=d1[key]
        print (key+' was added')
    else:
        if addlen==1:
            dnew[key]=d1[key]
            print(key+' was added')


for key in d1.keys():
    len1=len(d1[key])
    if (len1>mlen*1.2): dnew[key]=d1[key]



#subprocess.call('rm temp*', shell=True)
subprocess.call('rm out.*', shell=True)


fw=open(outfile,'w')
for key in dnew.keys():
    fw.write('>'+key+'\n')
    fw.write(dnew[key]+'\n')

fw.close()

