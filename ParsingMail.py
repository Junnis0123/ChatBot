import imaplib
import email
from time import sleep
from email.header import decode_header
import base64

#USER INFORMATION
UserId = ''
Password = ''

#MAIL SERVER SETTING
Server = ''
Port = 993

#FROM INFO
fromName = ''
fromMail = '{}{}{}'.format('(UNSEEN from ', fromName, ')')

#MAILINFO
latest = ''

def change_from_name(name):
    global fromName
    fromName = name
    global fromMail
    fromMail = '{}{}{}'.format('(UNSEEN from ', fromName, ')')


def get_name():
    return fromName

def ConnectMailSvr():
    print('Connect To ' + UserId + "...")
    mail = imaplib.IMAP4_SSL(Server, Port)
    mail.login(UserId, Password)
    mail.select("inbox")
    print('Connect!')
    _, unseen_data = mail.search(None, fromMail)
    
    email_ids  = unseen_data[0].split()

    if len(email_ids) == 0:
        mail.close() 
        return 0, 0

    latest_id = email_ids[-1:][0]
    global latest

    if latest_id == latest:
        mail.close() 
        return 0, 0
    
    if latest == '': #first
        latest = email_ids[0]
        eachIdsList = email_ids[  email_ids.index(latest) : email_ids.index(latest_id) + 1 ]
    else:
        eachIdsList = email_ids[  email_ids.index(latest) + 1 : email_ids.index(latest_id) + 1 ]
    latest = latest_id

    result =  str(len(email_ids))
    print('unseen mail is {}, new unseen mail is {}.'.format(result, len(eachIdsList)))    
    

    mails = []
    for e_id in eachIdsList:
        _, data = mail.fetch(e_id, '(RFC822)')
        mails.append(GetContents(data))

   
    mail.close() 
    print('DisConnect!')
    return result, mails

def GetContents(data):
    raw_email = data[0][1]

    raw_email_string = raw_email.decode('utf-8')        
    email_message = email.message_from_string(raw_email_string)
 
    print (email.utils.parseaddr(email_message['From'])[1]) 
    subject = email_message['Subject']

    if len(subject) != 0:
        subject, encoding = decode_header(subject)[0]
        subject = subject.decode(encoding)
    else:
        subject = '()'
    
    print(subject)

     # Contents
    while email_message.is_multipart():
        email_message = email_message.get_payload(0)

    content = email_message.get_payload()
    content = base64.b64decode(content).decode()
    print(content)
    return subject, content


'''
if __name__ == "__main__":
    GetMailLoop()
'''