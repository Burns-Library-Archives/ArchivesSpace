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
        secrets = __import__('secretsTEST')
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
    #'primaryName'
    #'authorityID' : url of LoC authority
    #'restOfName'
    #'fullerForm'
    #'title'
    #'prefix'
    #'suffix'
    #'date' : date as part of authorized form
    #'qualifier' : parenthetical qualifier as part of authorized form
    #'expression' : dates of existence
    #'begin' : normalized begin date in form YYYY-MM-DD.
    #'end' : normalized end date in form YYYY-MM-DD.
    #'noteBioghist' : Biographical note
    #'noteNames' : Alternate names note
    #Make sure to remove curly quotes/apostrophes
    #Make sure normalized dates are of type TEXT in excel - it likes to try and change them to DATE!

date = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
f = csv.writer(open('postNewPersonalAgents' + date + '.csv', 'w'))
f.writerow(['sortName'] + ['uri'])

csvfile = csv.DictReader(open(targetFile))

for row in csvfile:
    agentRecord = {}
    names = []
    name = {}
    name['sort_name'] = row['sortName']
    name['primary_name'] = row['primaryName']
    name['name_order'] = 'inverted'
    name['jsonmodel_type'] = 'name_person'
    name['rules'] = 'rda'
    if row['authorityID'] != '':
        name['authority_id'] = row['authorityID']
        name['source'] = 'lcnaf'
    else:
        name['source'] = 'local'
    try:
        name['rest_of_name'] = row['restOfName']
    except ValueError:
        name['name_order'] = 'direct'
    try:
        name['fuller_form'] = row['fullerForm']
    except ValueError:
        pass
    try:
        name['title'] = row['title']
    except ValueError:
        pass
    try:
        name['prefix'] = row['prefix']
    except ValueError:
        pass
    try:
        name['suffix'] = row['suffix']
    except ValueError:
        pass
    try:
        name['dates'] = row['date']
    except ValueError:
        pass
    try:
        name['qualifier'] = row['qualifier']
    except ValueError:
        pass
    names.append(name)
    
    notes = []
    bioNote = {}
    bioNote['jsonmodel_type'] = 'note_bioghist'
    bioNote['label'] = 'Biographical note'
    bioNote['publish'] = True
    subnotes = []
    subnote = {}
    subnote['jsonmodel_type'] = 'note_text'
    subnote['content'] = row['noteBioghist']
    subnote['publish'] = True
    subnotes.append(subnote)
    bioNote['subnotes'] = subnotes
    notes.append(bioNote)
    
    if row['noteNames'] != '':
        nameNote = {}
        nameNote['jsonmodel_type'] = 'note_general_context'
        nameNote['label'] = 'Alternate names'
        nameNote['publish'] = True
        subnotes = []
        subnote = {}
        subnote['jsonmodel_type'] = 'note_text'
        subnote['content'] = row['noteNames']
        subnote['publish'] = True
        subnotes.append(subnote)
        nameNote['subnotes'] = subnotes
        notes.append(nameNote)
    else:
        pass

    dates = []
    date = {}
    date['date_label'] = 'existence'
    date['jsonmodel_type'] = 'structured_date_label'
    if row['begin'] != '' and row['end'] != '':
        date['begin'] = row['begin']
        date['end'] = row['end']
        date['date_type_structured'] = 'range'
    elif row['begin'] != '':
        date['begin'] = row['begin']
        date['date_type_structured'] = 'single'
    elif row['end'] != '':
        date['end'] = row['end']
        date['date_type_structured'] = 'single'
    structuredDate = {}
    if row['begin'] != '' and row['end'] != '':
        structuredDate['jsonmodel_type'] = 'structured_date_range'
        structuredDate['begin_date_standardized'] = row['begin']
        structuredDate['begin_date_standardized_type'] = 'standard'
        structuredDate['end_date_standardized'] = row['end']
        structuredDate['end_date_standardized_type'] = 'standard'
        date['structured_date_range'] = structuredDate
    elif row['begin'] != '':
        structuredDate['jsonmodel_type'] = 'structured_date_single'
        structuredDate['date_standardized'] = row['begin']
        structuredDate['date_standardized_type'] = 'standard'
        structuredDate['date_role'] = 'begin'
        date['structured_date_single'] = structuredDate
    elif row['end'] != '':
        structuredDate['jsonmodel_type'] = 'structured_date_single'
        structuredDate['date_standardized'] = row['end']
        structuredDate['date_standardized_type'] = 'standard'
        structuredDate['date_role'] = 'end'
        date['structured_date_single'] = structuredDate
    else:
        structuredDate = {}
    dates.append(date)
        
    if row['expression'] != '':
        agentRecord['dates_of_existence'] = dates
    agentRecord['names'] = names
    agentRecord['notes'] = notes
    agentRecord['publish'] = True
    agentRecord['jsonmodel_type'] = 'agent_person'
    #print(agentRecord)
  
    try:
        post = requests.post(baseURL + '/agents/people', headers=headers, json=agentRecord).json()
        uri = post['uri']
        f.writerow([row['sortName']] + [uri])
    except KeyError:
        print(post)
        oops = post['error']
        uri = oops['conflicting_record']
        f.writerow([row['sortName']] + [uri])
        continue
    
    # Sleep for .5 seconds and then continue loop. 
    # This makes sure we don't overload the ASpace server
    time.sleep(.5)

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))