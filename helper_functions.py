#Code: Tarun Pathak
#------------------

#importing libraries
import os, joblib
from pandas import DataFrame
from string import punctuation
from sklearn.utils import shuffle
from spacy.lang.en.stop_words import STOP_WORDS
from sklearn.feature_extraction.text import TfidfVectorizer

#returns current directory
#(where the python script is saved)
def get_current_directory():
    return os.path.dirname(os.path.realpath(__file__))

#returns list of stopwords
def get_stopwords():
    custom_stopwords=['tarun','tathak','tarunpathak86@gmail.com','\\r','\\n']
    stopwords=STOP_WORDS.union(set(punctuation)).union(set(custom_stopwords))
    return [x.lower() for x in list(stopwords)]

#function to return dataset
#step 1) navigates through data directories
#step 2) extracts text and label from the text files (stores in list of list)
#extracted text in converted to lowercase
#step 3) encode labels as per encoding_dict
#step 4) shuffles the data (to avoid biased data sampling)
#step 5) returns data frame with text and encoded labels
def get_dataset(encoding_dict):
    #variables
    data = [];encoded_data = []
    cdir = get_current_directory() + '\\data\\'
    #building dataset
    for root, dirs, files in os.walk(cdir):
        for file in files:
            folder=root[root.rfind('\\')+1:]
            file_path=os.path.join(root, file)
            #reading file
            with open(file_path,'r',encoding='utf8') as f:
                content=str(f.read()).lower()
            #adding to data
            data.append([folder,content])

    #encoding data
    for record in data:
        try:
            label=encoding_dict[record[0]]
            encoded_data.append([label,record[1]])
        except Exception:
            encoded_data.append(record)

    #shuffling data
    encoded_data=shuffle(encoded_data)

    #returning data
    df=DataFrame()
    df['text']=[element[1] for element in encoded_data]
    df['label']=[element[0] for element in encoded_data]
    return df


#function to extract features from text data
#will be extracting TF-IDF values
def feature_extraction(corpus):
    #initializing transfer and
    #extracting features
    vectorizer = TfidfVectorizer(stop_words=get_stopwords())
    features = vectorizer.fit_transform(corpus).toarray()
    #saving model
    path = get_current_directory() + '\\model\\tf_idf.sav'
    joblib.dump(vectorizer,path)
    #returning dataframe
    return features