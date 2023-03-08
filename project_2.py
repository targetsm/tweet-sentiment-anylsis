# -*- coding: utf-8 -*-
"""Project_2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/dalab/lecture_cil_public/blob/master/exercises/2021/Project_2.ipynb

# Sentiment Classification Project
"""

import numpy as np

"""# Load data"""

tweets = []
labels = []

def load_tweets(filename, label):
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            tweets.append(line.rstrip())
            labels.append(label)
    
load_tweets('twitter-datasets/train_neg_full.txt', -1)
load_tweets('twitter-datasets/train_pos_full.txt', 1)

# Convert to NumPy array to facilitate indexing
tweets = np.array(tweets)
labels = np.array(labels)

print(f'{len(tweets)} tweets loaded')

"""# Build validation set
We use 90% of tweets for training, and 10% for validation
"""

def get_test_set(filename):
    twt = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            twt.append(line.split(",", 1)[1].rstrip())

    return twt

np.random.seed(1) # Reproducibility!

shuffled_indices = np.random.permutation(len(tweets))
split_idx = int(1.0 * len(tweets))
train_indices = shuffled_indices[:split_idx]
val_indices = shuffled_indices[split_idx:]

"""# Bag-of-words baseline"""

from sklearn.feature_extraction.text import CountVectorizer

# We only keep the 5000 most frequent words, both to reduce the computational cost and reduce overfitting
vectorizer = CountVectorizer(max_features=5000)

# Important: we call fit_transform on the training set, and only transform on the validation set
X_train = vectorizer.fit_transform(tweets[train_indices])
X_val = vectorizer.transform(tweets[val_indices])

Y_train = labels[train_indices]
Y_val = labels[val_indices]

"""Now we train a logistic classifier..."""

from sklearn.linear_model import LogisticRegression

print('Training Logistic Regression model')
model = LogisticRegression(C=1e5, max_iter=100)
model.fit(X_train, Y_train)

Y_train_pred = model.predict(X_train)
#Y_val_pred = model.predict(X_val)

train_accuracy = (Y_train_pred == Y_train).mean()
#val_accuracy = (Y_val_pred == Y_val).mean()

print(f'Accuracy (training set): {train_accuracy:.05f}')
#print(f'Accuracy (validation set): {val_accuracy:.05f}')

X_test = get_test_set('twitter-datasets/test_data.txt')
X_test = vectorizer.transform(X_test)
Y_test_pred = model.predict(X_test)
print(Y_test_pred)

with open("./logit_reg.csv", "w") as f:
    f.write("Id,Prediction\n")
    for idx, pred in enumerate(Y_test_pred):
        f.write("{},{}\n".format(idx + 1, pred))

exit()


"""# Model interpretation"""

model_features = model.coef_[0]
sorted_features = np.argsort(model_features)
top_neg = sorted_features[:10]
top_pos = sorted_features[-10:]

mapping = vectorizer.get_feature_names()

print('---- Top 10 negative words')
for i in top_neg:
    print(mapping[i], model_features[i])
print()

print('---- Top 10 positive words')
for i in top_pos:
    print(mapping[i], model_features[i])
print()

