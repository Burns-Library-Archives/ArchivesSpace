import json
import requests
import time
import csv
from datetime import datetime

secretsVersion = input('Enter the name of the secrets file: ')
if secretsVersion != '':
    try:
        secrets = __import__(secretsVersion)
        print('Editing Production')
    except ImportError:
        secrets = __import__('secrets')
        print('Editing Development')
else:
    print('Editing Development')

startTime = time.time()

baseURL = secrets.baseURL
user = secrets.user
password = secrets.password
repository = secrets.repository

auth = requests.post(baseURL + '/users/' + user + '/login?password='
                     + password).json()
session = auth['session']
headers = {'X-ArchivesSpace-Session': session,
           'Content_Type': 'application/json'}
print('authenticated')

targetFile = input('Enter file name: ')
#csv file with headers:\
    #'sortName' : sort name of agent
    #'role' : creator, source, or subject
    #'agent_id' : endpoint of agent
    #'ao_id' : primary key of AO

date = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
f = csv.writer(open('linkAgents' + date + '.csv', 'w'))
f.writerow(['sortName'] + ['AO_uri'])

csvfile = csv.DictReader(open(targetFile))

for row in csvfile:
    AO = row['ao_id']
    try:
        output = requests.get(baseURL + '/repositories/2/archival_objects/' + AO, headers=headers).json()
        linkedagent = {}
        linkedagent['role'] = row['role']
        linkedagent['ref'] = row['agent_id']
        output['linked_agents'].append(linkedagent)
    except KeyError:
        print('This AO produced an error: ' + AO + output)
        continue
    
    try:
        post = requests.post(baseURL + '/repositories/2/archival_objects/' + AO, headers=headers, json=output).json()
        uri = post['uri']
        f.writerow([row['sortName']] + [uri])
    except KeyError:
        print(post)
        continue
        
    # Sleep for .5 seconds and then continue loop. 
    # This makes sure we don't overload the ASpace server
    time.sleep(.5)
    
elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))