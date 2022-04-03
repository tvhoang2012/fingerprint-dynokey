import numpy as np
import clr
from numpy.linalg import norm
clr.AddReference('MccSdk')
import BioLab.Biometrics.Mcc.Sdk
def getmcc(iso,iso1,output,c):
    count= BioLab.Biometrics.Mcc.Sdk.MccSdk.CreateMccTemplateFromIsoTemplate(str(iso)+"_"+str(iso1)+".ist")
    BioLab.Biometrics.Mcc.Sdk.MccSdk.SaveMccTemplateToTextFile(count,str(output)+".txt")
    f = open(str(output)+".txt", "r")
    readmcc = f.readlines()
    countmcc=int(readmcc[3])+5
    binaryvector=[]
    for k in range(int(readmcc[3])):
        if(readmcc[countmcc+k].startswith("True")):
            binaryvector.append(Dynokeymodel(countmcc,readmcc,k,c))
    return binaryvector ,countmcc
def Dynokeymodel(countmcc,readmcc,k,c):
    a=readmcc[countmcc+k]
    a=a.replace("True","")
    a=a.replace(" ","")
    b=np.zeros(1536,dtype=np.int8)
    for i in range(1536):
        b[i]=a[i]
    cx=np.zeros(128,dtype=np.int8)
    i=0
    for x in c:
        cx[i]=b[x]
        i=i+1
    d1=b[0:256]
#c=np.sort(c)
    d2=b[256:]
    count=256
    d2=np.delete(d2,c)
    d=np.concatenate((d1,d2))
    l=(int)(len(d)/128)
    array=[]
    arrayout=[]
    for i in range(128): 
        array.append(d[l*i:l*(i+1)])
    for i in range(128):
        for j in range(l):
            array[i][j]=array[i][j]^cx[i]
    for i in range(len(array)):
        arrayout=np.concatenate((arrayout,array[i]))
    arrayout=np.array(arrayout,dtype=np.int8)
    return arrayout

def matching(a,b):
    s=[]
    for i in range(len(a)):
        for j in range(len(b)):
            a1=a[i][0:256]
            b1=b[j][0:256]
            k=np.bitwise_and(a1,b1)
            """
            a2=a[i][256:512]
            b2=b[j][256:512]
            k1=np.bitwise_and(a2,k)
            k1=np.concatenate((a[i][512:],k1))
            k2=np.bitwise_and(b2,k)
            k2=np.concatenate((b[j][512:],k2))
            k3=np.bitwise_xor(k1,k2)
            k11=pow(norm(k1),2)
            k22=pow(norm(k2),2)
            k33=pow(norm(k3),2)
            if(k11+k22!=0):
                k44=(k33)/(k11+k22)
                k44=1-k44
                s.append(k44)
            """
            n=1152//256
            k1=sim(a[i],k,n)
            a12=a[i][1280:]
            ka12=np.bitwise_and(a12,k[0:128])
            k1=np.concatenate((k1,ka12))
            k2=sim(b[j],k,n)
            b12=b[j][1280:]
            kb12=np.bitwise_and(b12,k[0:128])
            k2=np.concatenate((k2,kb12))
            k3=np.bitwise_xor(k1,k2)
            k11=pow(norm(k1),2)
            k22=pow(norm(k2),2)
            k33=pow(norm(k3),2)
            if(k11+k22!=0):
                k44=(k33)/(k11+k22)
                k44=1-k44
                s.append(k44)
            #"""
    return s
def sim(a,k,n):
    b=[]
    for i in range(1,n+1):
        b1=a[256*i:256*(i+1)]
        b1=np.bitwise_and(b1,k)
        b=np.concatenate((b,b1))
    b=np.array(b,dtype=np.int8)
    return b
