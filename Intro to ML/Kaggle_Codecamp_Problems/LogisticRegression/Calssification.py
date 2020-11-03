# %% [code]
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.impute import KNNImputer
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
from sklearn.neural_network import MLPClassifier

# %% [code]
train_x = pd.read_csv("D:/MSIT/2-YEAR-GIT-REPOS/Datascience_2019501102/Intro to ML/Kaggle_Codecamp_Problems/LogisticRegression/marketing_training.csv",index_col=0)
train_x

# %% [code]
train_y = train_x['responded']
train_y.hist()
train_x.drop('responded',axis=1,inplace=True)
train_x

# %% [code]
test_x = pd.read_csv("D:/MSIT/2-YEAR-GIT-REPOS/Datascience_2019501102/Intro to ML/Kaggle_Codecamp_Problems/LogisticRegression/marketing_test.csv",index_col=0)
test_x

# %% [code]
sample_size = len(train_x)
sample_size

# %% [code]
sample_size = len(test_x)
sample_size

# %% [code]
train_col_with_nullvalues=[[col,float(train_x[col].isnull().sum())/float(sample_size)] for col in train_x.columns if train_x[col].isnull().sum()]
train_col_with_nullvalues


# %% [code]
test_col_with_nullvalues=[[col,float(test_x[col].isnull().sum())/float(sample_size)] for col in test_x.columns if test_x[col].isnull().sum()]
test_col_with_nullvalues

# %% [code]
train_col_to_drop=[x for (x,y) in train_col_with_nullvalues if y>0.3]
train_col_to_drop


# %% [code]
test_col_to_drop=[x for (x,y) in test_col_with_nullvalues if y>0.3]
test_col_to_drop

# %% [code]
train_x.drop(train_col_to_drop,axis=1,inplace=True)
print(train_x)

# %% [code]
test_x.drop(test_col_to_drop,axis=1,inplace=True)
print(test_x)

# %% [code]
train_categorical_columns=[col for col in train_x.columns if train_x[col].dtype==object]
train_categorical_columns
print(len(train_categorical_columns))
train_ordinal_columns=[col for col in train_x.columns if col not in train_categorical_columns]
train_ordinal_columns
print((train_ordinal_columns))

# %% [code]
test_categorical_columns=[col for col in test_x.columns if test_x[col].dtype==object]
test_categorical_columns
print(len(test_categorical_columns))
test_ordinal_columns=[col for col in test_x.columns if col not in test_categorical_columns]
test_ordinal_columns
print(len(test_ordinal_columns))

# %% [code]
dummy_row=list()
for col in train_x.columns:
    if col in train_categorical_columns:
        dummy_row.append("dummy")
    else:
        dummy_row.append("")
new_row = pd.DataFrame([dummy_row],columns=train_x.columns)
train_x = pd.concat([train_x,new_row],axis=0, ignore_index=True)
train_x

# %% [code]
for col in train_categorical_columns:
    train_x[col].fillna(value="dummy",inplace=True)
    test_x[col].fillna(value="dummy",inplace=True)
    
enc = OneHotEncoder(drop='first',sparse=False)
enc.fit(train_x[train_categorical_columns])
trainx_enc=pd.DataFrame(enc.transform(train_x[train_categorical_columns]))
trainx_enc.columns=enc.get_feature_names(train_categorical_columns)

testx_enc=pd.DataFrame(enc.transform(test_x[train_categorical_columns]))
testx_enc.columns=enc.get_feature_names(train_categorical_columns)

train_x = pd.concat([train_x[train_ordinal_columns],trainx_enc],axis=1,ignore_index=True)
test_x = pd.concat([test_x[train_ordinal_columns],testx_enc],axis=1,ignore_index=True)

train_x.drop(train_x.tail(1).index,inplace=True)
train_x

# %% [code]
imputer = KNNImputer(n_neighbors=2)
imputer.fit(train_x)
trainx_filled = imputer.transform(train_x)
trainx_filled=pd.DataFrame(trainx_filled,columns=train_x.columns)
trainx_filled

# %% [code]
testx_filled = imputer.transform(test_x)
testx_filled=pd.DataFrame(trainx_filled,columns=test_x.columns)
testx_filled.reset_index(drop=True,inplace=True)
testx_filled

# %% [code]
scaler = preprocessing.StandardScaler().fit(trainx_filled)
train_x=scaler.transform(trainx_filled)
test_x=scaler.transform(testx_filled)
print(test_x)
print(train_x)

# %% [code]
pca = PCA().fit(train_x)
itemindex = np.where(np.cumsum(pca.explained_variance_ratio_)>0.9999)
print('np.cumsum(pca.explained_variance_ratio_)',      np.cumsum(pca.explained_variance_ratio_))
#Plotting the Cumulative Summation of the Explained Variance
plt.figure(np.cumsum(pca.explained_variance_ratio_)[0])
plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.xlabel('Number of Components')
plt.ylabel('Variance (%)') #for each component
plt.title('Principal Components Explained Variance')
plt.show()
pca_std = PCA(n_components=itemindex[0][0]).fit(train_x)
train_x = pca_std.transform(train_x)
test_x = pca_std.transform(test_x)
print(train_x)
print(test_x)

# %% [code]
le = preprocessing.LabelEncoder()
train_y=le.fit_transform(train_y)
print(train_y)

# %% [code]
train_x.shape

# %% [code]
X_train, X_test, y_train, y_test = train_test_split(train_x, train_y, test_size=1/3, random_state=0)

# %% [code]
test_x.shape

# %% [code]
logreg=LogisticRegression(class_weight="balanced",C=0.00001,max_iter=1000000)
logreg.fit(X_train, y_train)


# %% [code]
from math import sqrt
from sklearn.metrics import r2_score, mean_squared_error

print(sqrt(mean_squared_error(y_test, logreg.predict(X_test))))
print('R2 Value/Coefficient of Determination: {}'.format(logreg.score(X_test,y_test)))

# %% [code]
testpred=pd.DataFrame(logreg.predict(test_x))
testpred.to_csv("test_pred.csv")

# %% [code]
