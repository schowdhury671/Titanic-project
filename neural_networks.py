#!usr/bin/python

import pandas as pd 
import numpy as np 
import csv
# import keras as kp
from keras.models import Sequential
from keras.layers import Dense

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
	family_size=float(val[6])+float(val[7])+1
	newlist.append([float(val[2]),float(sex),float(age),float(val[6]),float(val[7]),float(val[9]),family_size])


# print Y
model = Sequential()
model.add(Dense(18, input_dim=7, activation='sigmoid'))
model.add(Dense(9, activation='sigmoid'))
model.add(Dense(14, activation='sigmoid'))
model.add(Dense(17, activation='sigmoid'))
model.add(Dense(1, activation='sigmoid'))
# Compile model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# Fit the model

# evaluate the model

with open('test.csv', 'rb') as f:
    reader = csv.reader(f)
    your_list = list(reader)
new_X=[]
for val in your_list:
	# Y.append([float(val[1])])
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
	family_size=float(val[5])+float(val[6])+1
	new_X.append([float(val[1]),float(sex),float(age),float(val[5]),float(val[6]),float(fare),family_size])

#predict
model.fit(newlist, Y, epochs=150, batch_size=10)
result=(model.predict_classes(new_X,batch_size=32,verbose=0))

# print result

# scores = model.evaluate(newlist, Y)
# print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))


f=open('result.csv','w')
f.write('PassengerID,Survived\n')
p=892
for val in result:
	class_result=0
	for i in val:
		class_result=i
	towrite=str(p)+","+str(class_result)+"\n"
	f.write(towrite)
	p+=1

f.close()

