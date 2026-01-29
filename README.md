# ArchivesSpace
This is a shared space for archivists at Burns Library, Boston College, to make public their work with coding for ArchivesSpace.

## linkAgentToAOFromCSV.py
Links existing agents to existing Archival Objects based on information in a CSV file with the following header row:
- 'sortName' : sort name of agent
- 'role' : creator, source, or subject
- 'agent_id' : endpoint of agent (primary key plus endpoint based on type of agent)
- 'ao_id' : primary key of AO

## postCorporateAgentsFromCSV.py
Creates new Corporate agents based on information in a CSV file with the following header row:
- 'sortName' : sort name of agent
- 'primaryName'
- 'authorityID' : url of LoC authority (the script expects a single authority source, which is specified in the code)
- 'restOfName'
- 'fullerForm'
- 'title'
- 'prefix'
- 'suffix'
- 'date' : date as part of authorized name form
- 'qualifier' : parenthetical qualifier as part of authorized name form
- 'expression' : dates of existence
- 'begin' : normalized begin date in form YYYY-MM-DD.
- 'end' : normalized end date in form YYYY-MM-DD.
- 'noteBioghist' : Biographical note (will appear as a Biographical/Historical note with the heading "Biographical note")
- 'noteNames' : Alternate names note (will appear as a General note with the heading "Alternate names")

## postPeopleAgentsFromCSV.py
Creates new People agents based on information in a CSV file with the following header row:
- 'sortName' : sort name of agent
- 'primaryName'
- 'authorityID' : url of LoC authority (the script expects a single authority source, which is specified in the code)
- 'restOfName'
- 'fullerForm'
- 'title'
- 'prefix'
- 'suffix'
- 'date' : date as part of authorized name form
- 'qualifier' : parenthetical qualifier as part of authorized name form
- 'expression' : dates of existence
- 'begin' : normalized begin date in form YYYY-MM-DD.
- 'end' : normalized end date in form YYYY-MM-DD.
- 'noteBioghist' : Biographical note (will appear as a Biographical/Historical note with the heading "Biographical note")
- 'noteNames' : Alternate names note (will appear as a General note with the heading "Alternate names")
