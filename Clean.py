import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()

#Removing stopwords, Punctuations and doing lemmatization
def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

# converting the NLTK Modules into pickle
import pickle

file = open('stop_nltk.pkl', 'wb')
pickle.dump(stop, file)

file = open('exclude_nltk.pkl', 'wb')
pickle.dump(exclude, file)

file = open('lemma_nltk.pkl', 'wb')
pickle.dump(lemma, file)

# Testing
Newz_Headline = "Apple launches it's new Iphone 18 in August 2022 in New York City"

Clean_OP = clean(Newz_Headline)

print(Clean_OP)
