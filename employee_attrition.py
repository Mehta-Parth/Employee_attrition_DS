# -*- coding: utf-8 -*-
"""Employee_attrition.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-hOfPNgS94MteKvax50Xte3IkmXCjtD6
"""

import numpy as np
import pandas as pd

hr_df=pd.read_csv('hr_data.csv')

hr_df.head()

type(hr_df)

hr_df.shape

"""#Numerical Analysis"""

hr_df.info()

hr_df['department'].unique()

hr_df['salary'].unique()

#Loading our Employee satisfaction file
s_df=pd.read_excel('employee_satisfaction_evaluation.xlsx')

s_df.head()

s_df.shape

#Merging and joining
main_df = hr_df.set_index('employee_id').join(s_df.set_index('EMPLOYEE #'))
main_df = main_df.reset_index()

main_df

main_df.info()

main_df[main_df.isnull().any(axis=1)]

main_df.describe()

main_df.fillna(main_df.mean(),inplace=True)  # fill with mode for low variance

main_df[main_df.isnull().any(axis=1)]

main_df.loc[main_df['employee_id']==3794]

main_df.drop(columns='employee_id',inplace=True)

main_df

main_df['department'].value_counts()

main_df['left'].value_counts()

main_df.groupby('department').sum()

main_df.groupby('department').mean()

"""#Data Visualisation"""

import matplotlib.pyplot as plt
import seaborn as sns

def plot_corr(df,size=10):

    corr=df.corr()
    fig,ax=plt.subplots(figsize=(size,size))
    cax=ax.matshow(corr)
    fig.colorbar(cax)
    plt.xticks(range(len(corr.columns)),corr.columns,rotation='vertical')
    plt.yticks(range(len(corr.columns)),corr.columns)

plot_corr(main_df)

sns.barplot(x='left',y='satisfaction_level',data=main_df)

sns.barplot(x='promotion_last_5years',y='satisfaction_level',data=main_df,hue='left')

sns.pairplot(main_df,hue='left')



"""#Data Preprocessing"""

y=main_df[['department','salary']]

y

from sklearn.preprocessing import LabelEncoder

le=LabelEncoder()

k = le.fit_transform(main_df['salary'])

k

main_df

main_df['salary_num']=k

main_df.loc[main_df['salary']=='high']

main_df.drop(['salary'],axis=1,inplace=True)
main_df

z = le.fit_transform(main_df['department'])
main_df['department_name']=z
main_df.drop(['department'],axis=1,inplace=True)
main_df

X = main_df.drop(['left'],axis=1)
X

y = main_df['left']
y

from sklearn.model_selection import train_test_split

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3)

X_train

X_test

"""#Model classification

##Decision Tree
"""

from sklearn.tree import DecisionTreeClassifier
scores_dict = {}
dt=DecisionTreeClassifier()

dt.fit(X_train,y_train)

prediction_dt=dt.predict(X_test)

from sklearn.metrics import accuracy_score

prediction_dt.size

y_test

accuracy_dt=accuracy_score(y_test,prediction_dt)*100
scores_dict['DecisionTreeClassifier'] = accuracy_dt
accuracy_dt

custom_dt=[[10,500,10,6,0,0.20,0.89,0,8]]

print(int(dt.predict(custom_dt)))

category=['Employee will stay','Employee will leave']

category[int(dt.predict(custom_dt))]

dt.feature_importances_

feature_importance = pd.DataFrame(dt.feature_importances_,index=X_train.columns,columns=['Importance']).sort_values('Importance',ascending=False)
feature_importance

"""##KNN algorithm
Data processing of the data
"""

from sklearn.preprocessing import StandardScaler

sc = StandardScaler().fit(X_train)
X_train_std = sc.transform(X_train)
X_test_std = sc.transform(X_test)

X_train_std

X_test_std

from sklearn.neighbors import KNeighborsClassifier

knn=KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train_std,y_train)

prediction_knn=knn.predict(X_test_std)

accuracy_knn = accuracy_score(y_test,prediction_knn)*100
scores_dict['KNeighborsClassifier'] = accuracy_score(y_test,prediction_knn)*100
accuracy_knn

prediction_knn

y_test

k_range=range(1,26)
scores={}
scores_list=[]

for k in k_range:
    knn=KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train_std,y_train)
    prediction_knn=knn.predict(X_test_std)
    scores[k]=accuracy_score(y_test,prediction_knn)*100
    scores_list.append(accuracy_score(y_test,prediction_knn))

scores

max(scores_list)

plt.plot(k_range,scores_list)

X_knn = np.array([[10,500,10,6,0,0.20,0.89,0,8]])
X_knn_std=sc.transform(X_knn)

X_knn_std

X_knn_prediction=knn.predict(X_knn_std)

category=['Employee will stay','Employee will leave']
category[int(X_knn_prediction)]

"""##SVM"""

from sklearn.svm import SVC
from sklearn.metrics import classification_report
model = SVC().fit(X_train_std,y_train)
pred = model.predict(X_test_std)
svc_accuracy = accuracy_score(y_test,pred)*100
print('Accuracy score : ',svc_accuracy)
scores_dict['SVC'] = svc_accuracy
print(classification_report(y_test,pred))

from lightgbm import LGBMClassifier
model = LGBMClassifier(learning_rate=0.03,n_estimators=1000).fit(X_train_std,y_train)
pred = model.predict(X_test_std)
LGBM_accuracy = accuracy_score(y_test,pred)*100
print('Accuracy score : ',LGBM_accuracy)
scores_dict['LGBMClassifier'] = LGBM_accuracy

"""#Comparision of decision tree and knn"""

algo_name = list(scores_dict.keys())
accuracy_list = list(scores_dict.values())

sns.set(rc={'figure.figsize':(12.4,6.5)})
with sns.color_palette('muted'):
    sns.barplot(x=algo_name,y=accuracy_list)

scores_dict

