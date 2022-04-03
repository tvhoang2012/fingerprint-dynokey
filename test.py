from Crypto.PublicKey import ECC
import scipy.io as sio
import numpy as np
import clr
import math
import Dynokey
minNp=4
def ffr(k):
    count=0
    for i in range(4,8):
        for j in range(4,8):
        #if i!=j:
            path=str(k)+'_'+str(i)+'.mat'
            data = sio.loadmat(path)
            a = data['Ftemplate']
            a=np.array(a).flatten()
            a=quantization(a)
            path1=str(k)+'_'+str(j)+'.mat'
            data = sio.loadmat(path1)
            b = data['Ftemplate']
            b=np.array(b).flatten()
            b=quantization(b)
            c=hammingDist(a,b)/len(b)
            print(c)
            if(c>=0.6):
                count=count+1
    return count
def hammingDist(f1,f2):
    count=0
    for i in range (0,len(f1)):
        if(f1[i]==f2[i]):
            count +=1
    return count
def quantization(f1):
    a=[]
    for i in f1:
        if i>=0:
            a.append(1)
        else:
            a.append(0)
    return a
def sum(f1,f2):
    count=0
    for i in range (0,len(f1)):
        count=count + f1[i]*f2[i]
    sum1=np.sum(np.power(f1,2))
    sum2=np.sum(np.power(f2,2))
    return count/(sum1+sum2)
def calcnp(a,b):
    if(a>b):
        v=b
    else:
        v=a
    u=32
    r=0.25
    k=-r*(v-u)
    Z=1/(1+math.pow(math.e,k))
    np=minNp+round(Z*6)
    return np
point_x=2656260949702819593775994095768777215309496706443786914386737476760406616152543114788706991411191827643967738727249493343490309747809686548271546654755551243
point_y=6545579463343772820521740217596549368341605880849630829454644377143033930250137681210130858918498283449425892004557403195953902315373745225831258068353697695
k=ECC.EccPoint(point_x,point_y,curve='P-521')
k=12*k
m=ECC.EccKey(curve='P-521',point=k)
#print(m.public_key())
#clr.AddReference('MccSdk')
#import BioLab.Biometrics.Mcc.Sdk
#BioLab.Biometrics.Mcc.Sdk.MccSdk.SetMccEnrollParameters("testmcc.xml")
#count= BioLab.Biometrics.Mcc.Sdk.MccSdk.CreateMccTemplateFromIsoTemplate("1_2.ist")
#BioLab.Biometrics.Mcc.Sdk.MccSdk.SaveMccTemplateToTextFile(count,"2.txt")
##for k in range(1,100):
 ##   count=count+(ffr(k)/2)   
""""      
f = open("2.txt", "r")
content = f.readlines()
int1=int(content[3])+5
a=content[int1]
a=a.replace("True","")
a=a.replace(" ","")

b=np.zeros(4500,dtype=np.int8)
for i in range(4500):
    b[i]=a[i]
c=np.random.choice(4275,500,replace=False)
cx=np.zeros(500,dtype=np.int8)
i=0
for x in c:
    cx[i]=b[x]
    i=i+1
d1=b[0:225]
#c=np.sort(c)
d2=b[225:]
count=225
d2=np.delete(d2,c)
d=np.concatenate((d1,d2))
l=(len(d)/500)
array=[]
for i in range(int(l)):
    array.append(d[500*i:500*(i+1)])
for i in range(int(l)):
    for j in range(500):
        array[i][j]=array[i][j]^cx[i]
"""
sum=0
for ii in range(20):
    c=np.random.choice(1280,128,replace=False)
#c1=np.random.choice(1280,128,replace=False)
    a, na=Dynokey.getmcc(1,1,1,c)
    b, nb=Dynokey.getmcc(1,3,3,c)
    c=Dynokey.matching(a,b)
    count=0
    k13=calcnp(na,nb)
    for i in range(k13):
        k12=np.max(c)
        index=np.argmax(c)
        count=count+k12
        c = np.delete(c,index) 
    print(count/k13)
    sum=sum+count/k13
print(sum/20)

