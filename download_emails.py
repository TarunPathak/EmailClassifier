#Code: Tarun Pathak
#------------------

#importing libraries
from gmail import Gmail
import helper_functions, os, re

#function to download spam emails
def download_emails(label):
    #current directory
    cdir=helper_functions.get_current_directory()
    #setting target folder
    if label.find('/')>0:
        folder=label[label.find('/')+1:].lower()
    else:
        folder=label.lower()

    #creating folder if it does not exists
    if not os.path.exists(cdir + '\\data\\' + folder):
        os.mkdir(cdir + '\\data\\' + folder)

    #getting all emails
    mail.select_folder(label,True)
    result, data = mail.get_all_emails()

    #exiting (if no emails returned)
    if not result=='OK':
        exit(1)

    #saving the content
    print('Starting Download.')
    for uid in data:
        dict = mail.parse_email(uid)
        subject = dict['Subject']
        subject=re.sub('[^a-zA-Z ]','',subject)
        if len(subject) > 50:
            subject = subject[:50]
        file = cdir + '\\data\\' + folder + '\\' + subject + '.txt'
        with open(file, 'w', encoding='utf-8') as f:
            body = subject + '\n' + str(dict['Body'])
            f.write(body)

    #displaying status
    print('Downloaded ' + str(len(data)) + ' ' + folder + ' emails.')
    print('------------------------------')

#main
if __name__=='__main__':
    #connecting to Gmail
    mail=Gmail('<your email>','<password>')#replace with your credentials

    #saving spam and ham emails
    download_emails('[Gmail]/Spam')
    download_emails('Ham')