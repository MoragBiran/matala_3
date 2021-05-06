import datetime
import re

# =============+Preprocessing+=============
def read_file(file):
    x = open(file,'r', encoding = 'utf-8')
    y = x.read()
    content = y.splitlines()
    return content

chat = read_file('�צאט WhatsApp עם יום הולדת בנות לנויה.txt')
chat_full = read_file('�צאט WhatsApp עם יום הולדת בנות לנויה.txt')

#chat = read_file('bonus.txt')
#chat_full = read_file('bonus.txt')

for i in range(len(chat)):
  try:
    datetime.datetime.strptime(chat[i].split(',')[0], '%d.%m.%Y')
  except ValueError:
    chat[i-1] = chat[i-1] + ' ' + chat[i]
    chat[i] = "NA"

while True:
    try:
        chat.remove("NA")
    except ValueError:
        break

for i in range(len(chat)):
    l = len(chat[i].split(' '))
    for j in range(l):
        if chat[i].split(' ')[j] == 'הוסיף/ה':
            chat[i] = "NA"
            break

while True:
    try:
        chat.remove("NA")
    except ValueError:
        break

from datetime import datetime
outputData = { 'datetime': [], 'id': [], 'text': [] }
Id_Data = {'Id': []}
erandic = {}
count = 0
for idx,line in enumerate(chat):
    if idx == 0:
        r = re.match(r'^(\d{1,2})\.(\d{1,2})\.(\d\d\d\d), ([0-1][0-9]|2[0-3]):[0-5][0-9]', line)
        cf = r.group().split(',')
        create_file = cf[0] + ' ' + cf[1]
    elif idx == 1:
        r2 = re.match(r'((\S[^:]*?): )?(.*)$', line)
        chat_name = r2.group().split('"')[1]
        rr = re.match(r'((\S[^:]*?): )?(.*)', line)
        creator = '+' + rr.group().split('+')[1][0:15]
    matches = re.match(r'^(\d{1,2})\.(\d{1,2})\.(\d\d\d\d), ([0-1][0-9]|2[0-3]):[0-5][0-9] - ((\S[^:]*?): )?(.*): ((\S[^:]*?): )?(.*)$', line)
    # print(re.match(r'^(\d{1,2})\.(\d{1,2})\.(\d\d\d\d), ([0-1][0-9]|2[0-3]):[0-5][0-9] - ((\S[^:]*?): )?(.*): ((\S[^:]*?): )?(.*)$', line))

    if matches:
        count += 1
        s = matches.group()[0:15]
        date = datetime(day=int(s[0]), month=int(s[2]), year=int(s[4:8]), hour=int(s[10:12]), minute=int(s[13:15]))
        outputData['datetime'].append(date.strftime("%d-%m-%Y %H:%M"))
        cond1 = matches.group().split(':')[1]
        if cond1.find('+') != -1:
            cond2 = '+' + cond1.split('+')[1][0:15]
        else:
            cond2 = cond1.split(' + ')[0].split('-')[1]
        outputData['id'].append(cond2)
        outputData['text'].append(matches.group().split(':')[2])
        Id_Data['Id'].append([cond2, date.strftime("%d-%m-%Y %H:%M"), matches.group().split(':')[2]])

# =========================================================
# A
iid = {}
a = []
for i in range(len(outputData['datetime'])):
    a.append(Id_Data['Id'][i][0])
    mylist = list(dict.fromkeys(a))
for ij, ii in enumerate(mylist):
    iid[ii] = ij

# B
Text = {}
ddATA = outputData['text']

for i,j in zip(outputData['text'], outputData['id']):
    if iid[j] not in Text:
        Text[iid[j]] = i
    else:
        a = [Text[iid[j]]]
        a.append(i)
        Text[iid[j]] = a

# C
num_of_participants = '<' + str(len(iid)) + '>'
metadata = { 'creation_date': [], 'chat_name': [], 'creator': [], 'num_of_participants': []}
metadata['creation_date'] = create_file
metadata['chat_name'] = chat_name
metadata['creator'] = creator
metadata['num_of_participants'] = num_of_participants


# D
Full_Dictionary = {'metadata': metadata, 'messages': Text}
import json

#E
import json
with open("json_file.txt",'w',encoding='utf8') as fp:
    json.dump(Full_Dictionary, fp, ensure_ascii=False)
