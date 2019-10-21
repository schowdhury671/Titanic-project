#I am adding this line

#!usr/bin/python

import pandas as pd 
import numpy as np 
import math
import csv
import keras as kp
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
import cv2


train_url = "http://s3.amazonaws.com/assets.datacamp.com/course/Kaggle/train.csv"
train = pd.read_csv(train_url)

test_url = "http://s3.amazonaws.com/assets.datacamp.com/course/Kaggle/test.csv"
test=pd.read_csv(test_url)

with open('train.csv', 'rb') as f:
    reader = csv.reader(f)
    your_list = list(reader)
newlist,Y=[],[]
for val in your_list:
	family_size=0.0
	title=0
	mtitle=val[3].split(' ')
	if(mtitle[0]=='Mr.'):
		title=0
	elif(mtitle[0]=='Mrs.'):
		title=1
	elif(mtitle[0]=='Miss.'): 
		title=2
	else:     # for the remaining category
		title=3
	Y.append([float(val[1])])
	sex=0
	age=val[5]
	if(val[4]=='male'):
		sex=1
	if(val[5]==''):
		age=22
	embarked=0
	if(val[11]=='S'):
		embarked=0
	elif(val[11]=='Q'):
		embarked=2
	else:
		embarked=1
	fare=val[9]
	if(fare==''):
		fare=5.0
	elif(fare=='0'):
		fare=0.1
	family_size=float(val[6])+float(val[7])+1
	newlist.append([float(val[2]),float(title),float(sex),float(age),float(val[6]),float(val[7]),math.log10(float(fare)),family_size])


X=np.array(newlist)

print X


with open('test.csv', 'rb') as f:
    reader = csv.reader(f)
    your_list = list(reader)
new_X=[]
for val in your_list:
	
	title=0
	mtitle=val[2].split(' ')
	if(mtitle[0]=='Mr.' or mtitle[0]=='Capt' or mtitle[0]=='Don'or mtitle[0]=='Major'or mtitle[0]=='Col'):
		title=0
	elif(mtitle[0]=='Mrs.'or mtitle[0]=='Dona' or mtitle[0]=='Lady'or mtitle[0]=='Jonkheer'or mtitle[0]=='Mlle'):
		title=1
	elif(mtitle[0]=='Miss.'):
		title=2
	else:
		title=3
	family_size=0.0
	sex=0
	age=val[4]
	if(val[3]=='male'):
		sex=1
	if(val[4]==''):
		age=22
	embarked=0
	if(val[10]=='S'):
		embarked=0
	elif(val[10]=='Q'):
		embarked=2
	else:
		embarked=1
	fare=val[8]
	if(fare==''):
		fare=5.0
	elif(fare=='0'):
		fare=0.1
	family_size=float(val[5])+float(val[6])+1
	new_X.append([float(val[1]),float(title),float(sex),float(age),float(val[5]),float(val[6]),math.log10(float(fare)),family_size])

nX=np.array(new_X)

clf=svm.SVC(kernel='linear',C=1.0,degree=2)
clf.fit(X,Y)   # fits the model

result=clf.predict(nX).tolist()
print result
f=open('result2.csv','w')
f.write('PassengerID,Survived\n')
p=892
for val in result:
	#print val
	class_result=int(val)
	towrite=str(p)+","+str(class_result)+"\n"
	f.write(towrite)
	p+=1

f.close()

