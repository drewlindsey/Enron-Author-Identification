# Enron E-mail Author Attribution
Assigns the author of a given e-mail from the Enron E-mail corpus.

### Data
The data in the corpus are man e-mails sent to and from the ~150 employee's of Enron. This data was cleaned and stripped of the headers and left with only the message body. This was then used to build a 'stylistic' profile for each author.

### Tech
Utilizes python's scikit learn as a machine learning library. Utilizes python's multiprocessing lib to handle data cleaning.

One-vs-all binary classification was utilized with Multinomial Naive bayes and LinearSVM.
