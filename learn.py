

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion
from sklearn.svm import LinearSVC
from sklearn import cross_validation
from sklearn.naive_bayes import MultinomialNB
import numpy as np

import os

training = []
authors = []
validate = []
test = []

# define TfidfVectorizers
word_vector = TfidfVectorizer(analyzer=u'word', ngram_range=(2,2), max_features = 2000,binary=False, min_df=0)
char_vector = TfidfVectorizer(analyzer=u'char', ngram_range=(4,4), max_features = 2000, binary=False, min_df=0)

#iterate over entire corpus TODO - increase accuracy of sorting
for root, dirs, files in os.walk('/media/sf_Project/data/'): 
	if root.find("symes") != -1:
		break
	if root.find("train") != -1: # add to training data set
		for name in files:
			training.append(os.path.join(root, name))
			authors.append(root.split('/')[4])
			continue
	if root.find("validate") != -1: #add to validate data set
		for name in files:
			validate.append(os.path.join(root,name))
	if root.find("test") != -1: #add to test data set
		for name in files:
			test.append(os.path.join(root,name))

# combine the TfidfVectorizers
vectorizer = FeatureUnion([("chars", char_vector), ("words", word_vector) ]) 

# generate word and character ngrams
X_training = vectorizer.fit_transform(training) 
X_validate = vectorizer.transform(validate)

# initialize models
model_SVC = LinearSVC(dual=False) 
model_NB = MultinomialNB()

# fit models to training data
model_SVC.fit(X_training, authors)
model_NB.fit(X_training, authors)

# generate predictions for validation set
Y_SVC = model_SVC.predict(X_validate)
Y_NB = model_NB.predict(X_validate)

# declare accuracy vars
total = 0
correct_SVC = 0
correct_NB = 0

# TODO - CrossValidation steps.

# check validation accuracy
for idx, item in enumerate(Y_SVC):
	total += 1
	if item == validate[idx].split('/')[4]:
		correct_SVC += 1
for idx, item in enumerate(Y_NB):
	if item == validate[idx].split('/')[4]:
		correct_NB += 1

print 'LinearSVC', correct_SVC, 'out of', total
print 'MultinomialNB', correct_NB, 'out of', total

while len(test) > 0 and raw_input("Type 'y' to quit ") != 'y':
	file_path = test.pop(np.random.randint(0, len(test)))
	print file_path

	# generate ngrams for current file
	X_test = vectorizer.transform([file_path])
	
	# generate predictions for test example
	prediction_SVC = model_SVC.predict(X_test)
	prediction_NB = model_NB.predict(X_test)
	
	# parse out true label
	true_label = file_path.split('/')[4]

	print "File predicted as: ", prediction_SVC, "with LinearSVC\t\t", "Accurate? ", \
			"yes" if prediction_SVC == true_label else "no"
	print "File predicted as: ", model_NB.predict(X_test), "with MultinomialNB\t\t", "Accurate? ", \
			"yes" if prediction_NB == true_label else "no"


