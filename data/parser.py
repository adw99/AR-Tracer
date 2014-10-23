# Code to parse splits.txt and ouptut race data in JSON
import datetime

def parseteam(line1,line2):
	nameend = line1.index('(CPA)')
	teamname = line1[:nameend-1].rstrip()
	checkpoints = line1[nameend:]
	bibend = line2.index(' ')
	bib = line2[:bibend].rstrip()
	times = line2[bibend:].rstrip().lstrip()

	curr_bib = {}
	curr_bib['bib'] = bib
	curr_bib['div_id'] = curr_div_id
	bib_list.append(curr_bib)

	cplist = checkpoints.split( ' ')
	timelist = times.split(' ')
	print "team name:",teamname,bib,len(cplist),len(timelist)

	prev_cp = ''
	prev_ts = datetime.datetime.now()

	for cp,t in zip(cplist,timelist):
		if "(" in cp:
			cp = cp.translate(None, '()')
			cp_set.add(cp)
		if t!='NA':
			checkin = {}
			checkin['race_id'] = race_id
			checkin['bib'] = bib
			checkin['div_id'] = curr_div_id
			checkin['checkpoint'] = cp
			the_time = datetime.datetime.strptime( t, "%H:%M:%S")
			checkin['time'] = the_time
			cp_collection.insert( checkin )

			if prev_cp != '':
				segment = {}
				segment['from'] = prev_cp
				segment['to'] = cp
				segment['bib'] = bib
				segment['race_id'] = race_id
				segment['div_id'] = curr_div_id
				segment['seconds'] = (the_time - prev_ts).total_seconds()
				segment_collection.insert(segment)

			prev_cp = cp
			prev_ts = the_time






from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['ar_tracer']
race_collection = db['races']
cp_collection = db['checkpoints']
segment_collection = db['segments']
race_id = 0
curr_div_id = 0

bib_list = list()
cp_set = set()

# Emptying collections - development only!
race_collection.remove( {} )
cp_collection.remove( {} )
segment_collection.remove( {} )


inputfile = open('splits.txt')

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
			race['divisions'] = []
			print race
			race_id = race_collection.insert(race);
			stage = 1
	elif stage == 1:
		if line.startswith('Division:'):
			curr_div_id+=1
			curr_division = line[9:].rstrip()
			divisions.append(curr_division)
			div_record = {}
			div_record['name'] = curr_division
			div_record['div_id'] = curr_div_id
			divisions.append(div_record)
		elif len(line) >0:
			if "(CPA)" in line:
				teamline1 = line
			else:
				teamline2 = line
				parseteam(teamline1,teamline2)

race['divisions'] = divisions
race['bibs'] = bib_list
race['checkpoints'] = list(cp_set)
race_collection.update( {'_id':race_id}, {"$set": race}, upsert = False)



