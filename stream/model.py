import pandas as pd

model=142# 우리 모델 

df = pd.read_csv("data.csv")

X = df[["Height", "Weight", "Eye"]]
X = X.replace(["Brown", "Blue"], [1, 0])

y = df["Species"]

clf = model() 
clf.fit(X, y)


import joblib

joblib.dump(clf, "clf.pkl")