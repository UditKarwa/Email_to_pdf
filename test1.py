import imaplib, email, getpass
import os,sys


HOST = ""
USERNAME = ""
PASSWORD = ""

connection = imaplib.IMAP4_SSL(HOST)
connection.login(USERNAME, PASSWORD)

#connection.list() # to get the list of all the folders in your email box

connection.select('"INBOX"')
result, data = connection.uid('search',None,'ALL')
mails = data[0].split()


count = len(mails)
print(count)

file_num = 0
for j,i in enumerate(mails):
  to_ = []
  from_ = []
  subj = []
  body = []
  ctype = []
  sys.stdout.write('fetching {}/{} mail'.format(j,count))
  e_result, e_data = connection.uid('fetch',i,'(RFC822)')
  sys.stdout.write('\r')
  sys.stdout.write('decoding')
  raw_email = e_data[0][1].decode("utf-8")
  sys.stdout.write('\r')
  email_msg = email.message_from_string(raw_email)

  to_.append(email_msg['To'])
  from_.append(email_msg['From'])
  subj.append(email_msg['Subject'])
  for i in email_msg.walk():
    content = []
    if i.get_content_maintype() == 'multipart':
      continue
    file_name = i.get_filename()

    if not file_name:
      ext = '.html'
    count -= 1
    content_type = i.get_content_type()
    if "plain" in content_type:
      content.append(i.get_payload())
    elif "html" in content_type:
      continue
    else:
      content.append('nan')
    body.append( content)
    ctype.append(content_type)
    with open('test_emails/email__'+str(file_num)+'.txt', 'w') as f:
      f.writelines('To: '+str(' '.join(to_))[:]+'\n')
      f.writelines('From: '+str(' '.join(from_))[:]+'\n')
      f.writelines('Subject: '+str(''.join( subj))[:]+'\n')
      f.writelines(str(' '.join(content)[:]+'\n'))
      f.writelines('CType: '+str(' '.join(ctype))[:]+'\n')
    file_num += 1
    if file_num == 10: 
        exit
  
connection.logout() #at the end of the program

