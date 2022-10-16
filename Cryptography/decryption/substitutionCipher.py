import string
import random
import numpy as np
import math

class genome:
    freq=[12.7,9.1,8.2,7.5,7.0,6.7,6.3,6.1,6.0,4.3,4.0,2.8,2.8,2.4,2.4,2.2,2.0,2.0,1.9,1.5,1.0,0.8,0.15,0.15,0.10,0.07]

    def __init__(self, key=""):
        
        self.key=key
        if key=="":
            self.key=random.sample(string.ascii_lowercase,k=26)
        if np.random.random()<0.8:
            pos1=np.random.randint(26)
            pos2=np.random.randint(26)
            fL = self.key[pos1]
            sL = self.key[pos2]
            key=self.key
            self.key=""
            for i in range(26):
                if(i==pos1):
                    self.key+=sL
                elif(i==pos2):
                    self.key+=fL
                else:
                    self.key+=key[i]
        self.keys=np.zeros(26)
        for i in range(26):
            self.keys[ord(self.key[i])-97]=i
        


    def getFitness(self,data):
        count=np.zeros(26)
        length=len(data)
        for i in data:
            if ord(i)>=97 and ord(i)<=123:
                #print(self.keys[ord(i)-97])
                count[int(self.keys[ord(i)-97])]+=1
                
            else:
                length-=1
        fitness =0
        for i in range(26):
            fitness+= abs(count[i]/length-genome.freq[i]/100)*((genome.freq[i])**0.5)
        return fitness
    def decrypt(self, data):
        decrypted=""
        for i in data:
            if ord(i)>=97 and ord(i)<=123:
                decrypted+= (chr(int(self.keys[ord(i)-97]+97)))
            else:
                decrypted+= i
        return decrypted


encrypted= input("Enter encrypted string: ").lower()

popCount=800
genCount=800
elite=40

A=np.empty(popCount,genome)
scores=np.zeros(popCount)
for i in range (popCount):
    A[i]=genome()
    scores[i]=A[i].getFitness(encrypted)
ind = np.argsort(scores)
scores=scores[ind]
A=A[ind]
for i in range(genCount):
    print(i/genCount)
    parents=np.empty(elite+int(0.3*popCount),genome)
    for j in range(elite):
        parents[j]=A[j]
    for j in range(elite, elite+int(0.3*popCount)):
        parents[j]=A[np.random.randint(popCount)]
    replaced=0
    while replaced<popCount:
        p1=parents[np.random.randint(len(parents))]
        p2=parents[np.random.randint(len(parents))]
        split=np.random.randint(26)
        A[replaced]=genome("".join(p1.key[0:split])+"".join(p2.key[split:26]))
        replaced+=1
        if(replaced<popCount):
            A[replaced]=genome("".join(p2.key[0:split])+"".join(p1.key[split:26]))
            replaced+=1
    for j in range(popCount):
        scores[j]=A[j].getFitness(encrypted)
    ind =np.argsort(scores)
    scores=scores[ind]
    A=A[ind]
    print(scores)
print(A[0].decrypt(encrypted))
print(genome("qwertyuiopasdfghjklzxcvbnm").decrypt(encrypted))
print(genome("qwertyuiopasdfghjklzxcvbnm").getFitness(encrypted))
