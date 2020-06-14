#Code: Tarun Pathak
#------------------

#Notes
#The code wont work till you enable 'Less Secure App' access
#https://myaccount.google.com/lesssecureapps

#importing packages
import imaplib, email, re
from nltk import word_tokenize
from bs4 import BeautifulSoup

#class to work with Gmail
class Gmail():

    #constructor
    def __init__(self,username,password):
        #connecting to gmail
        self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
        self.mail.login(username, password)
        #selecting 'Inbox' by Default
        #with read_only mode
        self.select_folder('Inbox',True)

    #returns list of folders
    def list_folders(self):
        list=[]
        folders=self.mail.list()[1]
        for folder in folders:
            folder=folder.decode('utf-8')
            folder=folder.replace('"','')
            list.append(folder[folder.rfind(')')+4:])

        return list

    #selects email folder (label)
    #If read_only=True, downloaded messages are not automatically marked as seen.
    def select_folder(self,folder, read_only):
        self.mail.select(folder,readonly=read_only)

    #returns UIDs of emails in selected folder
    #where send date>= date supplied by user
    def get_emails_sent_since(self,date):
        result, data = self.mail.uid('search', None, '(SENTSINCE {date})'.format(date=date))
        return result, data

    #returns UIDs of all emails in selected folder
    def get_all_emails(self):
        result,data=self.mail.uid('search',None,'All')
        return result,data[0].decode('utf-8').split()

    #returns raw email
    def raw_email(self,uid):
        result, data = self.mail.uid('fetch', uid, '(RFC822)')
        return result,data[0][1]

    #returns all unread emails
    def get_unread_emails(self):
        result, data = self.mail.uid('search', None, '(UNSEEN)')
        return result, data[0].decode('utf-8').split()

    #moves email
    def move_email(self, uid, target, destination):
        self.select_folder(target, False)
        result = self.mail.uid('COPY', uid, destination)
        if result[0] == 'OK':
            mov, data = self.mail.uid('STORE', uid, '+FLAGS', '(\Deleted)')
            self.mail.expunge()

        return mov

    #cleans email body
    #private function
    def __clean__(self,text):
        # replacing strings
        text = text.replace('  ', ' ')
        text = text.replace('</n', '<')
        text = text.replace('{*}', '')
        #replacing patterns
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'\n+', '\n', text)
        #removing long words (>15 characters)
        #this removes any css or gibberish
        output=''
        words=[word for word in word_tokenize(text) if len(word)<=15 and re.match('[A-Za-z0-9,._]+',word)]
        for word in words:
            if output=='':
                output=word
            else:
                output = output + ' ' + word

        #returning output
        return output

    #parses the meail
    def parse_email(self,uid):
        dict={}
        #raw email
        result, raw_email = self.raw_email(uid)
        raw_email = raw_email.decode('utf-8','ignore')
        #parsing email
        parsed = email.message_from_string(raw_email)
        dict['To']=email.utils.parseaddr(parsed['To'])[-1]
        dict['From']=email.utils.parseaddr(parsed['From'])[-1]
        dict['Subject']=parsed['Subject']

        body=''
        for part in parsed.walk():
            if part.get_content_type()=='text/html':
                html=str(part.get_payload())
                soup = BeautifulSoup(html,'html5lib')
                try:
                    text=soup.find('body').text.strip()
                except Exception:
                    continue

                text=self.__clean__(text)
                body=body + text

        body=self.__clean__(body)
        dict['Body']=body

        #returning parsed data
        return dict

    #terminates the connection
    def disconnect(self):
        self.mail.logout()