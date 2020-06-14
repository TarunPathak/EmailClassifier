#Code: Tarun Pathak
#------------------

#importing libraries
import joblib
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import RepeatedKFold
from helper_functions import get_dataset, feature_extraction,get_current_directory

#main
if __name__=='__main__':
    #getting data
    encoding_dict={'ham':0,'spam':1}
    dataset=get_dataset(encoding_dict)
    #extracting features from text
    print('Extracting text features.')
    label = dataset['label'].values.tolist()
    features=feature_extraction(dataset['text'].values.tolist())


    #training
    #--------

    #setting up classifier
    clf=MultinomialNB()

    #splitting dataset using Repeated KFold
    #training model on each split
    print('Training started.')
    score=[]
    rkf=RepeatedKFold(n_splits=5,n_repeats=2,random_state=20)
    for train,test in rkf.split(features,label):
        #getting splits
        x_train=[features[index] for index in train]
        x_test=[features[index] for index in test]
        y_train=[label[index] for index in train]
        y_test = [label[index] for index in test]
        #training classifier and getting score
        clf.fit(x_train, y_train)
        result = clf.score(x_test, y_test)
        score.append(result)

    #saving model
    path=get_current_directory() + '\\model\\naive_bayes.sav'
    joblib.dump(clf,path)
    print('Training complete. Model has been saved.')
    #printing accuracy
    print('Mean accuracy score: ' + str(sum(score)/len(score)))