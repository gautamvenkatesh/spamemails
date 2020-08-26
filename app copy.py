from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
import email
import mysql.connector
from bs4 import BeautifulSoup
import quopri
from datetime import date

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def startup():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
         with open('token.pickle', 'rb') as token:
             creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

global service
service = startup()

def updatedb():
    global service
    result = service.users().messages().list(userId='me', labelIds = ['INBOX']).execute()
    count = 0
    messages = result.get('messages', [])
    id_list_prev = []
    #new_email = []
    for i in messages:
        id_list_prev.append(i['id'])


    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Sql314209!",
        )
    cursor = mydb.cursor()
    cursor.execute('use emails')
    cursor.execute('delete from olids')

    for i in id_list_prev:
        cursor.execute(f"insert into olids (ids) values ('{i}');")
    mydb.commit()
    cursor.close()


def check_for_new():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Sql314209!",
        )
    cursor = mydb.cursor()
    cursor.execute('use emails')
    cursor.execute('select * from olids')
    rawids = cursor.fetchmany(100)
    old_ids = []
    for i in rawids:
        old_ids.append(i[0])

    global service
    result = service.users().messages().list(userId='me', labelIds = ['INBOX']).execute()
    messages = result.get('messages', [])
    new_ids = []
    for i in messages:
        new_ids.append(i['id'])

    unread = []

    try:
        num = 99 - old_ids.index(new_ids[-1])
    except ValueError as ve:
        print('ValueError occurred')
        updatedb()
        num = 100 - old_ids.index(new_ids[-1])

    if num > 0:
        for i in range(0,num):
            unread.append(new_ids[i])
    return unread

def spamcheck(ids):
    global service
    fin_message = []
    data = []
    for message in ids:
        count = 0
        fin_message.append(gethtml(message))

    for i in fin_message:
        soup = BeautifulSoup(i, 'html.parser')
        soup.prettify()
        data_small = ''
        for z in soup.find_all(['p','a','td']):
            data_small += (z.text.replace('=','').replace('\n','').replace('\r',''))
            data_small += '\n'
        data.append(data_small)
    spam_list = []
    findict = {}
    for i in data:
        if 'Unsubscribe' in i or 'unsubscribe' in i:
            spam_list.append(True)
        else:
            spam_list.append(False)
    for i in range(0, len(ids)):
            findict[ids[i]] = spam_list[i]

    return findict

def gethtml(ids):
    global service
    msg = service.users().messages().get(userId='me',id=ids, format='raw').execute()
    msg_raw = base64.urlsafe_b64decode(msg['raw'].encode("utf-8")).decode("utf-8")
    mime_msg = email.message_from_string(msg_raw)
    html = ''
    count = 0
    for i in mime_msg.walk():
        if i.get_content_type() == 'text/html':
            try:
                raw = quopri.decodestring(i.get_payload())
            except ValueError:
                raw = "Message could not be decoded"
                print("ValueError occured")
            count = 1
    if count == 0:
        raw = mime_msg.get_payload()

    soup = BeautifulSoup(raw, 'html.parser')
    soup.prettify()
    for s in soup(['style']):
        s.decompose()
    return soup.prettify()


def getinformation(ids):
    info = {}
    global service
    msg = service.users().messages().get(userId='me',id=ids, format='raw').execute()
    msg_raw = base64.urlsafe_b64decode(msg['raw'].encode("utf-8")).decode("utf-8")
    mime_msg = email.message_from_string(msg_raw)
    info['subject'] = mime_msg['subject']
    date = mime_msg['date']
    date_splt = date.split()
    datenew = ''
    for i in date_splt:
        if ':' in i:
            break
        datenew += i + ' '
    info['date'] = datenew
    sender = mime_msg['from'].replace('<','').replace('>','')
    sender_splt = sender.split()
    name = ''
    sendemail = ''
    for i in sender_splt:
        if '@' in i:
            sendemail = i
        else:
            name += i + ' '
    info['name'] = name
    info['emailadd'] = sendemail 
    return info









    