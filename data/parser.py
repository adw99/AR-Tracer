# Code to parse splits.txt and ouptut race data in JSON
import datetime

def parseteam(line1,line2):
	nameend = line1.index('(CPA)')
	teamname = line1[:nameend-1].rstrip()
	checkpoints = line1[nameend:]
	bibend = line2.index(' ')
	bib = line2[:bibend].rstrip()
	times = line2[bibend:].rstrip().lstrip()

	cplist = checkpoints.split( ' ')
	timelist = times.split(' ')
	print "team name:",teamname,bib,len(cplist),len(timelist)

	for cp,t in zip(cplist,timelist):
		if "(" in cp:
			cp = cp.translate(None, '()')
		if t!='NA':
			checkin = {}
			checkin['race_id'] = race_id
			checkin['bib'] = bib
			checkin['division_id'] = curr_div_id
			checkin['checkpoint'] = cp
			the_time = datetime.datetime.strptime( t, "%H:%M:%S")
			checkin['time'] = the_time
			cp_collection.insert( checkin )



from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['ar_tracer']
race_collection = db['races']
div_collection = db['divisions']
cp_collection = db['checkpoints']
race_id = 0
curr_div_id = 0

# Emptying collections - development only!
race_collection.remove( {} )
div_collection.remove( {} )
cp_collection.remove( {} )

inputfile = open('splits.txt')
# outputfile = open('splits.json',w)

stage = 0;

race = {}
divisions = []
teamline1 = ''
teamline2 = ''

for line in inputfile:
	line = line.rstrip()
	if stage == 0:
		if line.startswith('Race:'):
			race['name'] = line[5:]
		if line.startswith('Date:'):
			race['date'] = line[5:]
			print race
			race_id = race_collection.insert(race);
			stage = 1
	elif stage == 1:
		if line.startswith('Division:'):
			curr_division = line[9:].rstrip()
			divisions.append(curr_division)
			div_record = {}
			div_record['name'] = curr_division
			div_record['race_id'] = race_id
			curr_div_id = div_collection.insert( div_record )
		elif len(line) >0:
			if "(CPA)" in line:
				teamline1 = line
			else:
				teamline2 = line
				parseteam(teamline1,teamline2)



