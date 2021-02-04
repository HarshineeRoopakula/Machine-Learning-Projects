import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline

# This function is used to visualize confusion matrix
def cm(y_test, y_pred):
    cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
    df_cm = pd.DataFrame(cnf_matrix, columns=np.unique(y_pred),index=np.unique(y_pred))
    fig, ax = plt.subplots()
    sns.heatmap(df_cm, annot=True, cmap='YlGnBu', fmt='.0f') 
    ax.xaxis.set_label_position('top')
    plt.tight_layout()
    plt.title('Confusion matrix', y=1.1)
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    
# This function is used to calculate performance metric
def metric_calculation(y_test, y_pred):
    metric_list = list()
    accuracy = metrics.accuracy_score(y_test, y_pred)
    precision = metrics.precision_score(y_test, y_pred)
    recall = metrics.recall_score(y_test, y_pred)
    F1 = 2 * (precision * recall) / (precision + recall)
    metric_list = [accuracy, precision, recall, F1]
    return metric_list
  
df = pd.read_csv('online_shoppers_intention.csv')

# create dummy variables for categorical variables
df_with_dummies= pd.get_dummies(df,columns=['Month', 'OperatingSystems', 'Browser', 'Region',
       'TrafficType', 'VisitorType', 'Weekend'],drop_first=True)

# change the column order to separate attributes and target variable more easily later
df_new = pd.concat([df_with_dummies.iloc[:,1],df_with_dummies.iloc[:,0],df_with_dummies.iloc[:,2:]], axis=1)

X = df_new.iloc[:,1:]  # Attributes
y = df_with_dummies.Revenue # Target 
# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

############## Decision Tree ##############  

from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier

DT = DecisionTreeClassifier(max_depth=5)
DT.fit(X_train,y_train)
y_pred_clf = DT.predict(X_test)
cm(y_test, y_pred_clf)
DT_metric = metric_calculation(y_test, y_pred_clf)

############## kNN ##############  

from sklearn.preprocessing import StandardScaler # Standardize features by removing the mean and scaling to unit variance

sc = StandardScaler()
sc.fit(X_train)

X_train_std = sc.transform(X_train)
X_test_std = sc.transform(X_test)

# Fitting classifier to the Training set
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=6, p=2, metric='minkowski')
knn.fit(X_train_std, y_train)
y_pred_knn = knn.predict(X_test_std)
cm(y_test,y_pred_knn)
knn_metric = metric_calculation(y_test, y_pred_knn)

############## Logistic Regression ##############  

from sklearn.linear_model import LogisticRegression # Import Logistic Regression Classifier

logreg = LogisticRegression()
logreg.fit(X_train,y_train)
y_pred_logreg=logreg.predict(X_test)
cm(y_test,y_pred_logreg)
logreg_metric = metric_calculation(y_test, y_pred_logreg)

############## Naive Bayes ##############  

from sklearn.naive_bayes import GaussianNB #Import Gaussian Naive Bayes model

gnb = GaussianNB(). #Create a Gaussian Classifier
gnb.fit(X_train, y_train)
y_pred_gnb = gnb.predict(X_test)
cm(y_test, y_pred_gnb)
gnb_metric = metric_calculation(y_test, y_pred_gnb)

# summurize and visualize the performance for each classifier
metric = pd.DataFrame([DT_metric, knn_metric, logreg_metric, gnb_metric], columns=['accuracy', 'precision', 'recall','f1'],
                     index=['decision_tree', 'knn', 'logistic_regression', 'naive_bayes'])

metric.T.plot.bar(rot=0)