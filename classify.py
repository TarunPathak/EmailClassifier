#Code: Tarun Pathak
#------------------

#importing libraries
from gmail import Gmail
from random import randint
import joblib, sys, logging, datetime
from helper_functions import get_current_directory

#main
if __name__=='__main__':
    #connecting to gmail
    #fetching unread emails
    mail = Gmail('tarunpathak86@gmail.com', 'Nik@nD51@@')
    result,data=mail.get_unread_emails()

    #exiting (if no data found)
    if not result=='OK':
        print('No unread emails found.')
        sys.exit(0)

    #loading model and vectorizer
    path = get_current_directory()
    clf=joblib.load(path + '\\model\\naive_bayes.sav')
    vectorizer=joblib.load(path + '\\model\\tf_idf.sav')

    #setting up log files
    dt=datetime.datetime.now()
    log_file=path + '\\logs\\' + str(dt.year) + str(dt.month) + str(dt.day) + '-' + str(randint(0,10000)) + '.txt'
    logger=logging.getLogger(log_file)
    logger.setLevel(logging.INFO)
    logging.info('Starting...')


    #fetching email contents
    #storing email subject along with body
    #this is to classify those emails which dont have text but
    #just an image embedded in the body
    for uid in data:
        dict = mail.parse_email(uid)
        content=[dict['Subject'] + '\n' + dict['Body']]

        #extracting features
        #getting predicition from classifier
        features = vectorizer.transform(content)
        pred = clf.predict(features)

        #moving to spam folder (if predicted as spam)
        if pred[0]==1:
            mov=mail.move_email(data[1],'Inbox','[Gmail]/Spam')
            if mov=='OK':
                message='Following email moved to spam:\nuid: ' + str(uid) +'\nSubject: ' + str(dict['Subject']) + '\nContent: ' + str(dict['Body']) +'\n----------------------------------'
                print(message)
                logging.info(message)

    #message
    print('Program Ended')
    logging.info('Ended.')