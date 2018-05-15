# This file is just for my conveniece; it's not connected to the main program, only to the database.
import sqlite3 # for reading/writing learned data to database ***NEW
import uuid #for UUID
from datetime import datetime #for UUID
import os # for creating database backups ***NEW
import shutil # for creating database backups ***NEW
# absolute_filepath = os.path.dirname(__file__) #the absolute filepath of this script.
dbConn = sqlite3.connect('learned_data.db')
dbCursor = dbConn.cursor()
# dbCursor.execute("PRAGMA foreign_keys=ON") # to allow SQLite foreign key deletion/update on cascade
def generateUuid(order="None"):
	"""Generate a reasonably unique ID string based on date and time.
	----------Dependencies:
	import uuid
	import os or from datetime import datetime

	----------Parameters:
	None

	----------Returns:
	a string (e.g. '2018_11_26-9_13-85894b2f')
	"""
	dateAndTime = datetime.now()
	randomId = str(uuid.uuid4()) #generate a UUID
	randomId = randomId[:8] #truncate it because 36 digits is too long
	if order=="random-first":
		myUuid = "%s_%s-%s-%s_%s-%s" % (
			randomId,
			str(dateAndTime.year),
			str('%02d' % dateAndTime.month),
			str('%02d' % dateAndTime.day),
			str('%02d' % dateAndTime.hour),
			str('%02d' % dateAndTime.minute)
			)
	else:
		myUuid = "%s-%s-%s_%s-%s_%s" % (
			str(dateAndTime.year),
			str('%02d' % dateAndTime.month),
			str('%02d' % dateAndTime.day),
			str('%02d' % dateAndTime.hour),
			str('%02d' % dateAndTime.minute),
			randomId
			)
	print("\t\tGenerated UUID: ",myUuid)
	return myUuid
def pullQueryResults():
	"""Copies the most recent SQLite selection. Should ONLY be called after executing a SQLite query."""
	#pull in whatever the most recent query selected
	dbData = dbCursor.fetchall() 
	
	#put the results into a list
	listToReturn = []
	for row in dbData:
		listToReturn.append(row[0])
	return listToReturn

	if listToReturn == []: # if no results, return None.
		return None
# Creating/Writing
def createTables():
	# Note: pastPerfect is AKA pluperfect.
	dbCursor.execute("""CREATE TABLE IF NOT EXISTS terms (
		key TEXT,
		term TEXT,
		partOfSpeech TEXT,
		def_comprehensive TEXT,
		def_deduced TEXT,
		plural TEXT,
		past TEXT,
		present TEXT,
		future TEXT,
		pastPerfect TEXT,
		pastPlural TEXT,
		presentSingularThirdPerson TEXT,
		presentPluralThirdPerson TEXT,
		pastParticiple TEXT,
		presentParticiple TEXT,
		subjunctive TEXT,
		actor TEXT,
		tradResponse TEXT,
		PRIMARY KEY(`key`)
		)""")
	dbCursor.execute("""CREATE TABLE IF NOT EXISTS terms_definingCateg (
		key TEXT,
		terms_key TEXT NOT NULL,
		term TEXT,
		definingCateg TEXT,
		PRIMARY KEY(`key`),
		FOREIGN KEY(`terms_key`) REFERENCES `terms`(`key`) ON DELETE CASCADE ON UPDATE CASCADE,
		FOREIGN KEY(`term`) REFERENCES `terms`(`term`) ON DELETE CASCADE ON UPDATE CASCADE
		)""")
	dbCursor.execute("""CREATE TABLE IF NOT EXISTS terms_otherCateg (
		key TEXT,
		terms_key TEXT,
		term TEXT,
		otherCateg TEXT,
		PRIMARY KEY(`key`),
		FOREIGN KEY(`terms_key`) REFERENCES `terms`(`key`) ON DELETE CASCADE ON UPDATE CASCADE,
		FOREIGN KEY(`term`) REFERENCES `terms`(`term`) ON DELETE CASCADE ON UPDATE CASCADE
		)""")
	dbCursor.execute("""CREATE TABLE IF NOT EXISTS terms_misc (
		key TEXT,
		terms_key TEXT,
		term TEXT,
		property TEXT,
		PRIMARY KEY(`key`),
		FOREIGN KEY(`terms_key`) REFERENCES `terms`(`key`) ON DELETE CASCADE ON UPDATE CASCADE,
		FOREIGN KEY(`term`) REFERENCES `terms`(`term`) ON DELETE CASCADE ON UPDATE CASCADE
		)""")
	dbCursor.execute("""CREATE TABLE IF NOT EXISTS terms_conceptType (
		key TEXT,
		terms_key TEXT,
		term TEXT,
		conceptType TEXT,
		PRIMARY KEY(`key`),
		FOREIGN KEY(`terms_key`) REFERENCES `terms`(`key`) ON DELETE CASCADE ON UPDATE CASCADE,
		FOREIGN KEY(`term`) REFERENCES `terms`(`term`) ON DELETE CASCADE ON UPDATE CASCADE
		)""")
def backupDB():
	""" 
	Dependencies: generateUuid
		import os, shutil
	Returns: True if there's not a fatal error first lol
	"""
	print("\tcreating backup of learned_data.db")

	newFileName = "learned_data_"+str(generateUuid())+".db"

	src_dir= os.curdir
	dst_dir= os.path.join(os.curdir , "backup_databases")
	src_file = os.path.join(src_dir, "learned_data.db")
	shutil.copy(src_file,dst_dir)

	dst_file = os.path.join(dst_dir, "learned_data.db")
	new_dst_file_name = os.path.join(dst_dir, newFileName)
	os.rename(dst_file, new_dst_file_name)

	return True
def updateDefComp():
	print ("\t\tupdating each def_comprehensive in the table 'terms'.")
	wordsWithDefComp = [
		["517223ec_2018-04-08_17-27", "def_comp_include.py"],
		["f71e490c_2018-04-08_17-27", "def_comp_define.py"],
	]

	for i in range (0,len(wordsWithDefComp)): #for each word with a comprehensive definition
		currentKey = wordsWithDefComp[i][0]
		currentFileName = wordsWithDefComp[i][1]
		currentDefAsString = ""

		#pull contents of .py file into a string
		with open (currentFileName, 'r', encoding="utf8") as f:
		    for line in f: #For each line of text, store in a string variable in the list urlContent_raw.
		        currentDefAsString += line+"\n"

		#push the string to the database
		dbCursor.execute("""UPDATE terms SET def_comprehensive = ? WHERE key = ? """, (currentDefAsString,currentKey,))
	dbConn.commit()
def populateTable(table):
	"""Dependencies: updateDefComp()"""
	if table == "terms":
		# insert multiple values from a Python list
		rowsToInsert = [
			('8c713d7c_2018-04-08_17-27', "instrument", "NOUN",None,None,None,None,None,None,None,None,None,None,None,None,None,None,None),
			('178793e0_2018-04-08_17-27', "inanimate", "ADJ",None,None,None,None,None,None,None,None,None,None,None,None,None,None,None),
			('395221b5_2018-04-08_17-27', "musical instrument", "NOUN",None,None,None,None,None,None,None,None,None,None,None,None,None,None,None),
			('991335b6_2018-04-08_17-27', "object shaped like a guitar", "NOUN",None,None,"objects shaped like guitars",None,None,None,None,None,None,None,None,None,None,None,None),
			('47f86f92_2018-04-08_17-27', "guitar", "NOUN",None,None,None,None,None,None,None,None,None,None,None,None,None,None,None),
			('3e62a082_2018-04-08_17-27', "physical object owned by me", "NOUN",None,None,"physical objects which I own",None,None,None,None,None,None,None,None,None,None,None,None),
			('f052bbab_2018-04-08_17-27', "dominionstats", "NOUN",None,None,None,None,None,None,None,None,None,None,None,None,None,None,None),
			('c553b8a1_2018-04-08_17-27', "huntokar", "NOUN",None,None,None,None,None,None,None,None,None,None,None,None,None,None,None),
			('04da5d0b_2018-04-08_17-27', "black", "ADJ",None,None,None,None,None,None,None,None,None,None,None,None,None,None,None),
			('4bd02b9d_2018-04-08_17-27', "run", "VERB",None,None,None,"ran","run","will run","had run",None,"ran","run",None,"running","were running","runner",None),
			('ec7f8a50_2018-04-08_17-27', "fly", "VERB",None,None,None,"flew","fly","will fly","had flown","flew","flew","flew","flown","flying","were flying","flyer",None),
			('47651306_2018-04-08_17-27', "bird", "NOUN",None,None,None,None,None,None,None,None,None,None,None,None,None,None,None),
			('7e2e76d4_2018-04-08_17-27', "goose", "NOUN",None,None,"geese",None,None,None,None,None,None,None,None,None,None,None,None),
			('410593b5_2018-04-08_17-27', "penguin", "NOUN",None,None,None,None,None,None,None,None,None,None,None,None,None,None,None),
			('36dc0a25_2018-04-08_17-27', "duck", "NOUN",None,None,None,None,None,None,None,None,None,None,None,None,None,None,None),
			('06339b16_2018-04-08_17-27', "aquatic", "ADJ",None,None,None,None,None,None,None,None,None,None,None,None,None,None,None),
			('517223ec_2018-04-08_17-27', "include", "VERB",None,None,None,"included","include","will include","had included",None,None,None,"included","including","were including","includer",None),
			('f71e490c_2018-04-08_17-27', "define", "VERB",None,None,None,"defined","define","will define","had defined",None,None,None,None,"defining","were defining","definer",None),
			('26055ed2_2018-04-08_17-27', "number", "NOUN",None,None,None,None,None,None,None,None,None,None,None,None,None,None,None),
			('2e8be200_2018-04-08_17-27', "longer", "ADJ",None,None,None,None,None,None,None,None,None,None,None,None,None,None,None),
			('2883e6a9_2018-04-08_17-27', "speak of the devil and he shall appear", "SENTENCE",None,None,None,None,None,None,None,None,None,None,None,None,None,None,None),
			('aad14126_2018-04-08_17-27', "hello", "INTJ",None,None,None,None,None,None,None,None,None,None,None,None,None,None,"hello"),
			('tempryky_2018-05-13_23-01', "abstraction", "NOUN",None,None,None,None,None,None,None,None,None,None,None,None,None,None,None),
			('31415926_2018-05-13_07-56', "pi", "NOUN",None,None,None,None,None,None,None,None,None,None,None,None,None,None,None),
			('symbol00_2018-05-13_23-01', "symbol", "NOUN",None,None,None,None,None,None,None,None,None,None,None,None,None,None,None),
			('isableto_2018-04-08_17-27', "can", "VERB",None,None,None,"was able to","can","will be able to","had been able to",None,None,None,"been able to","being able to","could",None,None)
		]
		dbCursor.executemany('insert into terms values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', rowsToInsert)
		dbConn.commit()
		updateDefComp()
		## Generate new keys (code used for first run).
		# for i in range (0,len(knownTerms)):
		# 	key = generateUuid("random-first")
		# 	term = knownTerms[i][0]
		# 	partOfSpeech = knownTerms[i][1]

		# 	dbCursor.execute("INSERT INTO terms (key, term, partOfSpeech) VALUES (?, ?, ?)",
		# 		  (key, term, partOfSpeech))
	
	elif table == "terms_definingCateg":
		# insert multiple values from a Python list
		rowsToInsert = [
			("96d48984_2018-04-08_18-24", "395221b5_2018-04-08_17-27", "musical instrument","instrument"),
			("dbf5e29f_2018-04-08_18-24", "395221b5_2018-04-08_17-27", "musical instrument","tool"),
			("c1d436f8_2018-04-08_18-24", "395221b5_2018-04-08_17-27", "musical instrument","inanimate"),
			("8aa29813_2018-04-08_18-24", "991335b6_2018-04-08_17-27", "object shaped like a guitar","object"),
			("b958a608_2018-04-08_18-24", "47f86f92_2018-04-08_17-27", "guitar","musical instrument"),
			("26d29994_2018-04-08_18-24", "47f86f92_2018-04-08_17-27", "guitar","object shaped like a guitar"),
			("f6b723b5_2018-04-08_18-24", "3e62a082_2018-04-08_17-27", "physical object owned by me","object"),
			("26d3c19e_2018-04-08_18-24", "3e62a082_2018-04-08_17-27", "physical object owned by me","owned by me"),
			("df7d60da_2018-04-08_18-24", "f052bbab_2018-04-08_17-27", "dominionstats","software"),
			("29c5854f_2018-04-08_18-24", "f052bbab_2018-04-08_17-27", "dominionstats","owned by me"),
			("e977753f_2018-04-08_18-24", "c553b8a1_2018-04-08_17-27", "huntokar","guitar"),
			("bfa1ea3d_2018-04-08_18-24", "c553b8a1_2018-04-08_17-27", "huntokar","black"),
			("6c5de551_2018-04-08_18-24", "c553b8a1_2018-04-08_17-27", "huntokar","physical object owned by me"),
			("404a17f8_2018-04-08_18-24", "04da5d0b_2018-04-08_17-27", "black","color"),
			("3bec8cd1_2018-04-08_18-24", "04da5d0b_2018-04-08_17-27", "black","dark"),
			("bf2f917d_2018-04-08_18-24", "4bd02b9d_2018-04-08_17-27", "run","action"),
			("cffe3829_2018-04-08_18-24", "4bd02b9d_2018-04-08_17-27", "run","locomote"),
			("aafa2704_2018-04-08_18-24", "4bd02b9d_2018-04-08_17-27", "run","use"),
			("1346f372_2018-04-08_18-24", "ec7f8a50_2018-04-08_17-27", "fly","in air"),
			("47179c63_2018-04-08_18-24", "47651306_2018-04-08_17-27", "bird","fly"),
			("d4ed033a_2018-04-08_18-24", "47651306_2018-04-08_17-27", "bird","animal"),
			("6cd27521_2018-04-08_18-24", "7e2e76d4_2018-04-08_17-27", "goose","bird"),
			("36c0196d_2018-04-08_18-24", "7e2e76d4_2018-04-08_17-27", "goose","aquatic"),
			("ef98c346_2018-04-08_18-24", "7e2e76d4_2018-04-08_17-27", "goose","waterfowl"),
			("3d4394f0_2018-04-08_18-24", "410593b5_2018-04-08_17-27", "penguin","bird"),
			("fdbd83b3_2018-04-08_18-24", "410593b5_2018-04-08_17-27", "penguin","tuxedo-wearing"),
			("9bc7ec15_2018-04-08_18-24", "410593b5_2018-04-08_17-27", "penguin","aquatic"),
			("0de56481_2018-04-08_18-24", "410593b5_2018-04-08_17-27", "penguin","not fly"),
			("2af48527_2018-04-08_18-24", "36dc0a25_2018-04-08_17-27", "duck","bird"),
			("552b10b0_2018-04-08_18-24", "36dc0a25_2018-04-08_17-27", "duck","aquatic"),
			("351d6caa_2018-04-08_18-24", "36dc0a25_2018-04-08_17-27", "duck","waterfowl"),
			("495cc279_2018-04-08_18-24", "06339b16_2018-04-08_17-27", "aquatic","live in water"),
			("fb38bcaa_2018-04-08_18-24", "f71e490c_2018-04-08_17-27", "define","describe"),
			("b510c436_2018-04-08_18-24", "26055ed2_2018-04-08_17-27", "number","concept"),
			("9025dbac_2018-04-08_18-24", "2e8be200_2018-04-08_17-27", "longer","comparative"),
			("f6b3e0e6_2018-04-08_18-24", "symbol00_2018-05-13_23-01", "symbol","abstraction"),
			("pinumber_2018-05-13_19-26", "31415926_2018-05-13_07-56", "pi","number"),
			("irationl_2018-05-13_19-26", "31415926_2018-05-13_07-56", "pi","number")
		]
		dbCursor.executemany('insert into terms_definingCateg values (?,?,?,?)', rowsToInsert)

	elif table == "terms_otherCateg":
		rowsToInsert = [
			("5cda575a_2018-04-08_18-24", "47f86f92_2018-04-08_17-27", "guitar","bridged"),
			("ded8efac_2018-04-08_18-24", "47651306_2018-04-08_17-27", "bird","winged"),
			("2d4fc793_2018-04-08_18-24", "7e2e76d4_2018-04-08_17-27", "goose","migrational"),
			("88fbca4a_2018-04-08_18-24", "f71e490c_2018-04-08_17-27", "define","state"),
			("b3a4cd72_2018-04-08_18-24", "26055ed2_2018-04-08_17-27", "number","symbol"),
			("b2da49a4_2018-04-08_18-24", "26055ed2_2018-04-08_17-27", "number","word"),
			("343cbd9e_2018-04-08_18-24", "2e8be200_2018-04-08_17-27", "longer","long")
		]
		dbCursor.executemany('insert into terms_otherCateg values (?,?,?,?)', rowsToInsert)
	elif table == "terms_misc":
		pass
	elif table == "terms_conceptType":
		rowsToInsert = [
			("2018-04-12_14-12_8ef933d9", "517223ec_2018-04-08_17-27", "include", "detail"),
			("2018-04-12_14-12_f112bf59", "f71e490c_2018-04-08_17-27", "define", "general"),
			("2018-04-12_14-12_87192fe8", "26055ed2_2018-04-08_17-27", "number", "math"),
			("2018-04-12_14-12_0859fa11", "26055ed2_2018-04-08_17-27", "number", "detail"),
			("2018-04-12_14-12_5ba4fcbd", "2e8be200_2018-04-08_17-27", "longer", "compare"),
			("2018-04-12_14-12_2d094bdf", "2e8be200_2018-04-08_17-27", "longer", "physical"),
			("2018-04-12_14-12_4c4159f2", "2e8be200_2018-04-08_17-27", "longer", "size"),
			("2018-04-12_14-12_b839f56a", "2e8be200_2018-04-08_17-27", "longer", "space")
		]
		dbCursor.executemany('insert into terms_conceptType values (?,?,?,?)', rowsToInsert)
	else:
		print("populateTable() was called on an unknown table.")
	dbConn.commit()
	return True
def recreateTerms():
	dbCursor.execute("""
	DROP TABLE terms
	""")
	dbConn.commit()
	print("Dropped terms.")
	dbCursor.execute("""CREATE TABLE IF NOT EXISTS terms (
		key TEXT PRIMARY KEY,
		term TEXT,
		partOfSpeech TEXT,
		def_comprehensive TEXT,
		def_deduced TEXT,
		plural TEXT,
		past TEXT,
		present TEXT,
		future TEXT,
		pastPerfect TEXT,
		pastPlural TEXT,
		presentSingularThirdPerson TEXT,
		presentPluralThirdPerson TEXT,
		pastParticiple TEXT,
		presentParticiple TEXT,
		subjunctive TEXT,
		actor TEXT,
		tradResponse TEXT
	)""")
	dbConn.commit()
	populateTable("terms")
	printTable("terms")

# Reading/Executing
def printTable(requestedTable=None):
	allTables = ["terms","terms_definingCateg","terms_otherCateg","terms_misc","terms_conceptType"]

	if requestedTable == None: #if no argument, print all tables
		for i in range (0,len(allTables)):
			currentTable = allTables[i]

			# SQLite Query
			sql_cmd = """SELECT * FROM {}""".format(currentTable)
			dbCursor.execute(sql_cmd)
			dbData = dbCursor.fetchall()
			
			# Print results
			print ("\n\n=========="+currentTable)
			for row in dbData:
				print(row)
	else:
		# SQLite Query
		sql_cmd = """SELECT * FROM {}""".format(requestedTable)
		dbCursor.execute(sql_cmd)
		dbData = dbCursor.fetchall()
		
		# Print results
		print ("\n\n=========="+requestedTable)
		for row in dbData:
			print(row)
def execDefComp(requestedKey,wordContext,subject=None,verb=None,do=None,io=None,adjAdv=None):
    '''
    Executes a  currentDef() from the column 'def_comprehensive' in the table 'terms'.
    Can only return ONE row at a time, from the table 'terms'. Don't pass in any key which could return >1 row!!!
    '''
    #import the currentDef as string
    dbCursor.execute("""SELECT def_comprehensive FROM terms WHERE key = ?;""", (requestedKey,))
    dbData = dbCursor.fetchall()
    for row in dbData:
    	functionAsString = (row)
    functionAsString = functionAsString[0]

    #if Query returned "Null" or None, print a warning and then return None. If Query returned more than one row, same. #incomplete

    #call currentDef()
    # print(functionAsString+"\t.\n\t.\n\t.")
    exec(functionAsString,globals()) # bring the currentDef into global scope
    defResult = currentDef(wordContext,subject,verb,do,io,adjAdv) # call the currentDef
    # print ("\tresults=",str(defResult))
    return defResult


###################@@# Do The Things #########
backupDB()
# createTables()
# populateTable('terms')
# populateTable('terms_definingCateg')
# populateTable('terms_otherCateg')
# populateTable('terms_conceptType')

# updateDefComp()
# execDefComp("517223ec_2018-04-08_17-27","declarative","authors",None,"mark twain")



print("=========Done\n")






###################@@# Notes #########
# sqlite notes: 
   #leave known corpus (and its text file) as .py files for now
   #booleans can be represented by integers
   #knownmeanings and their utilites each are in their own .py file in learned_data
   #knownmeanings defs: will be executed as a string of each meaning def. the defs are stored each in their own python file (shared dependencies are in separate files), in learned_data. the strings are automatically refreshed when the main runtime starts, and when triggered as needed.

# database notes: 
	# definitions are looked-up according to the following order: def_comprehensive > def_deduced > definingcateg > othercategory
	# nouns do not have comprehensive definitions unless hey have an ontological meaning which is separate from the categories which characterize them (such as numbers)
	# when adding idioms/sentence fragments as terms, they must be either in unconjugated present tense, or in the tense in which the idiom is always spoken. notes about the evaluation conditions appear in their .py definitions.

	# Order of cascading TAMC (tense, aspect, mood, conjugation):
	# for nouns: 
		# plural --> term
	# for verbs: 
		# subjunctive --> presentParticiple --> present --> term
		# presentSingularThirdPerson --> present --> term
		# presentPluralThirdPerson --> present --> term
		
		# pastParticiple --> past --> present --> term
		# pastPerfect --> past --> present --> term
		# pastPlural --> past --> present --> term
		
		# future --> present --> term
	# Info on contructing verbs can be found here: https://www.brighthubeducation.com/english-homework-help/39260-the-english-verb-system-for-esl-students

	# during reflection, deduceRegularConj: for each empty slot,  calculate plurals, presentParticiples (-ing), pastParticiples (-en), past tenses for verbs ending in e (-ed), and the subjunctives (were PastParticipling).

#'terms' notes: 
	# category lists are sparse (i.e. not comprehensive), and are subjective.
	# the rest of these rules are just suggestions; none of this needs to be perfect in order to function.
	# all nouns should be singular and nominative case (e.g. "i", not "me"). all verbs should be infinitive present-tense, without the word 'to' (e.g. "fly", not "to fly").
	# 'negated' categories (e.g. 'not animal') are only allowed if they're exceptions to a rule. for example, "not fly" is allowed for "penguin" because bird has the property "fly"). they can also be allowed if they're stand-alone terms on their own (e.g. 'non-smoking' or 'inanimate').
	# nested categories are not required! also, no category is required to link to a root category; free-floating branches are fine.
	# terms can be longer sentence fragments, but ideally they will be words or phrases. this maximizes pattern-recognition during reflection.

	#each term has the following:
		# part of speech - for a complete list, see http://universaldependencies.org/u/pos/
		# various forms of the term, e.g. conjugation for verbs or plaurality for nouns or whatever:
			# 'plaural':	*defaults to the singular form plus 's'
			# 'pasttense':
			# 'presenttense':
			# 'gerund':
			# 'actor':	  *defaults to the gerund form minus "ing" plus "er".
			# 'singular3rdpersonperfecttense':
			# 'perfecttense':
			# 'pluperfect':
			# (and for the verb "be": 'pluralpasttense', 'pluralpresenttense', 'pluralinfinitive').
		# 'infinitive' is omitted because it's already included in index 0.
		# 'futuretense' is omitted because it's simply "will " + the infinitive.
			
		# these forms don't need to be comprehensive, because i intend to write a conjugation function which cascades to the next-most-appropriate conjugation, whenever the requested conjugation is unavailable.
		

		# terms_definingcateg = the categories which define the object ontologically, and into which all instances can be classified. for example: every time someone 'defines' something, they are 'describing' it.
		# terms_otherCateg = other categories into which all instances can be classified. for example: all instances of 'defining' are instances of 'claiming'.]


# Required and Suggested Database Indexes - https://www.sqlite.org/foreignkeys.html#fk_indexes