#{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
#{}
#{}	@@		Load dependencies and global variables
#{}
#{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}

#import dependencies
from datetime import datetime #to generate UUIDs
from learned_data.util_findCategories import * #to link terms
from learned_data.util_isCategoryInstance import * #to evaluate terms' category relationships
from operator import itemgetter #to sort lists of lists
import itertools # to removeDuplicates()
import json #to read doc metadata
import os #to read and write from disk, and backup database
import re #to parse html
import shutil #for creating database backups
import sqlite3 #for reading/writing to database
import sys #to delete and reload python files
import textacy #to create docs/doc metadata, and to lemmatize and tokenize unstructured text
import uuid #to generate UUIDs

#declare global variables
absolute_filepath = os.path.dirname(__file__) #the absolute filepath of this script.
knowledgePriorityLevel = 1
sentencesJustWritten = 0 #number of sentences written since last user input
maxSentencesAtOnce = 10 #limit how many sentences can be written without user input
dbConn = sqlite3.connect(absolute_filepath+'/learned_data/learned_data.db') #to connect to database
dbCursor = dbConn.cursor() #to connect to database
# dbCursor.execute("PRAGMA foreign_keys=ON") # to allow SQLite foreign key deletion/update on cascade
# from nlp_resources.compromise_conjugations_mod import * #import variable compromiseConjugations, to help parse conjugated verbs #it'll be a long time before this can learn verbs on its own.


#{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
#{}
#{}	@@		General utilities
#{}
#{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}

#Utilities with no external dependencies:
def eow(input,p=False):
	"""Takes a list of lists of lists of words. Returns it, but with Every Other Word omitted. Useful for removing parts of speech from sentences to print.
		Or, if p == True, 
	----------Dependencies:
	None
	
	----------Parameters:
	input = list of lists of lists of words.
		Example: [
			[['bird', 'NOUN'], ['fly', 'VERB']], 
			[['number', 'NOUN'], ['include', 'VERB'], ['eight', 'ADV']]
		]
	p = a boolean. If True, prints directly from this function.
	
	----------Returns:
	A list of lists of strings, e.g.:
		Example: [
			['bird', 'fly'], 
			['number', 'include', 'eight']
		]
	"""
	errors = 0
	output = []
	
	if isinstance(input,list) and len(input)>0: #fail gracefully
	
		for i in range (0,len(input)):
			sentence = input[i]
			newSc = []
			
			if isinstance(sentence,list) and len(sentence)>0: #fail gracefully
				for j in range (0,len(sentence)):
					termGroup = sentence[j]
					
					if isinstance(termGroup,list) and len(termGroup)>0: #fail gracefully
						newSc.append(termGroup[0])
					else:
						errors += 1
						print("  ERROR - Bad value in eow() parameter:",str(termGroup))
				if p == True and len(newSc)>0: #print stuff. fail gracefully.
					toPrint = ""
					for j in range (0,len(newSc)):
						toPrint = "%s %s" % (toPrint,newSc[j])
					print(" |",toPrint)
			else:
				errors += 1
				print("  ERROR - Bad value in eow() parameter:",str(sentence))
			output.append(newSc)

	else:
		errors += 1
		print("  ERROR - Bad value passed to eow().")

	if errors > 0:
		print("  The full list of values passed to eow() was:",str(output))
	if p==False:
		return(output)
	else:
		return output
def findIndexOfString(string,storedList,indexOne,indexTwo=None):
	"""Find the index of a string in a list. (Or in a list of lists, once I get around to it.)
	----------Dependencies:
	None

	----------Parameters:
	string = the string you want to find, e.g. 'musical instrument'
	storedList = the name of the list to search within, e.g. 'knownTerms'
	indexOne = a number. the index of storedList, to search within. e.g. 0
	indexTwo = a number. indexTwo exists because I will later overload this function to also hanlde lists of lists.

	----------Returns:
	A number. The index of the string found in storedList. If the string was not found, returns False.
	"""
	
	
	tempStroredList = []

	for i in range(0,len(storedList)):
		#if the two strings have same first AND last letter AND are the same length...
		if string[0]==storedList[i][indexOne][0] and string[-1]==storedList[i][indexOne][-1] and len(string)==len(storedList[i][0]): 
			#save the matching index in tempStroredList
			tempStroredList.append(i)

	#search tempStoredList for precise matches. 
	for i in range(0,len(tempStroredList)):
		storedListIndex = tempStroredList[i]
		if storedList[storedListIndex][indexOne] == string:
			return storedListIndex #return the (tempStroredList) index of the first precise match found.
	
	#if no match found, return False
	return False
def findPosTemplates():
	"""One day this will pull varied lists from a fancy table, but for now there are only two sentence templates.
	----------Dependencies:
	None, for now. learned_data.db, eventually.
	
	----------Parameters:
	None, for now.
	
	----------Dependencies:
	A list of lists containing strings which are parts of speech.
	"""
	allSctemplates = [
		["NOUN", "VERB"],
		["NOUN", "VERB", "NOUN"],
	]
	return allSctemplates
def generateUuid(order=None):
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
def removeDuplicates(myList):
	"""Takes a list. Returns it with only the unique values.
	----------Dependencies: 
	import itertools
	"""
	if isinstance(myList,list):
		myList.sort()
		myList = list(myList for myList,_ in itertools.groupby(myList))
		return myList
	else:
		print("\t\t\tremoveDuplicate() was called on a non-list:",str(input))
		return myList
def sortLists(myLists,index,order):
	"""Takes a list of lists. Returns it, sorted by a given index.
	----------Dependencies:
	from operator import itemgetter

	----------Parameters:
	myLists (a list of lists. one item in each of the lists should be an int.)
	index (the index to sort by)
	order Smallest-to-largest is Python's default. If that's not what you want, write 'largestToSmallest'

	----------Returns:
	the same list you passed in, but sorted.
	"""

	sortedLists = sorted(myLists, key=itemgetter(index))
	if order == "largestToSmallest":
		sortedLists = list(reversed(sortedLists))
	return sortedLists

#Utilities with external dependencies:
def infinitize(word,pos=None):
	pass 
	# try using textacy, then (via regular expressions) the db and compromise.
def execDefComp(requestedTerm,wordContext,subject=None,verb=None,do=None,io=None,adjAdv=None):
	"""	Executes a currentDef() located in the column 'def_comprehensive' in the table 'terms'.
	Note: This function's query can only return ONE row at a time, from the table 'terms'. Avoid passing in any terms which could return >1 row.

	----------Dependencies:
	learned_data.db in the folder learned_data
	
	----------Parameters:
	requestedTerm = a string. the term to execute the def_comprehensive of.
	wordContext = a string. options are: 'evaluate', 'learn', or 'perform'
	subject = a string. 
	verb = a string. 
	do = a string. 
	io = a string. 
	adjAdv = a string. 

	----------Returns:
	whatever the function currentDef returns, for a given term. this function can be found in the column def_comprehensive for a given term in the table terms.
	"""
	def printArgs():
		print("\t\t\t\trequestedTerm=",requestedTerm)
		print("\t\t\t\twordContext=",wordContext)
		print("\t\t\t\tsubject=",subject)
		print("\t\t\t\tverb=",verb)
		print("\t\t\t\tdo=",do)
		print("\t\t\t\tio=",io)
		print("\t\t\t\tadjAdv=",adjAdv)

	dbCursor.execute("""SELECT def_comprehensive FROM terms WHERE term = ?;""", (requestedTerm,))
	dbData = pullQueryResults()
	if isinstance(dbData,list):

		#report errors
		if len(dbData) == 0:
			print("\t\t\tA bad argument was passed to execDefComp(), so no def_comprehensive was found. Returned None. \n\t\t\t\tArguments passed in:")
			printArgs()
			return None
		if len(dbData) > 1:
			print("\t\t\tA bad argument was passed to execDefComp(), resulting in mulltiple files found. Only the first result was used.\n\t\t\tArguments passed in:")
			printArgs()

		#import the currentDef as string
		functionAsString = dbData[0]
		#call the currentDef() located in the executed string
		# print(functionAsString+"\t.\n\t.\n\t.")
		exec(functionAsString,globals()) # bring the currentDef into global scope
		defResult = currentDef(wordContext,subject,verb,do,io,adjAdv) # call the currentDef
		# print ("\tresults=",str(defResult))
		return defResult

	else:
		print("\t\t\tA bad argument was passed to execDefComp(), so no def_comprehensive was found. Returned None. \n\t\t\tArguments passed in:")
		printArgs()
		return None
def orderByPos(templates,words):
	"""Returns every possible order of the words passed in, which is both the correct length AND has the correct parts of speech.
	----------Dependencies:
	None

	----------Parameters:
	templates = a list of lists containing strings which are parts of speech. findPosTemplates() can provide these templates.
		Example: [
			["NOUN", "VERB"],
			["NOUN", "VERB", "NOUN"],
		]
	words = a list of lists. each of the lists should contain a word (infinitized) and it's POS. Can be in any order.
		Example: [
			["bird","NOUN"],
			["duck","NOUN"],
			["include","VERB"],
		]

	----------Returns:
	A list containing all possible arrangements of those words, which match the POS in the templates. The arrangements are grammatical, but have not yet been tested for truth.
	"""
	validatedOrders = []
	
	#Error handling
	if templates == None or templates == []:
		print("\t\t\torderByPos() was called with templates = None or templates = []. Returned None.")
		return None
	if words == None or words == []:
		print("\t\t\torderByPos() was called with words = None or words = []. Returned None.")
		return None
		
	for h in range(0,len(templates)):
		currentTemplate = templates[h]
		startOrder = words
		def compareLen(testList,testTemplate):
			"""Takes a list. Returns the string '<' or '=' or '>'. """
			if len(testList) < len(testTemplate):
				# print("< compareLen")
				return "<"
			elif len(testList) == len(testTemplate):
				# print("= compareLen")
				return "="
			else:
				# print("> compareLen")
				return ">"
			### end of compareLen()
		def comparePOS(testPOS,templatePOS):
			"""Compares POS in test list, to POS in template list, at the requestedindex only. If they match, returns True.
			Only test phrases vetted as the correct length ever get passed to this function."""
			threshold = len(testPOS)
			correctPOS = 0
			
			for p in range(0,len(testPOS)):
				if testPOS[p][1] == templatePOS[p]:
					correctPOS += 1
			
			if correctPOS >= threshold:
				# print ("passed the pos threshold")
				return True
			else:
				return False
			### end of comparePOS()
		def instance_lenMatch(templateIndex,jOrder,visualizeTabs=''):
			"""An infinitely recursive function. Appends any orders with the correct length and POS', to validatedOrders"""
			#break out of infinite loops
			templateIndex += 1
			for m in range (0,templateIndex):
				visualizeTabs += '  '
			if templateIndex > len(currentTemplate):
				print("%stemplateIndex=%s:   jOrder=%s" % (visualizeTabs,templateIndex,jOrder))
				print ("\na possible infinite loop was detected, so an instance_lenMatch() recursive search was terminated.\n")
				return False

			# show what is going on (for debugging)
			# print("%stemplateIndex=%s:   jOrder=%s" % (visualizeTabs,templateIndex,jOrder))

			#try adding an element to eval loop.
			for k in range (0,len(startOrder)):
				#recreate kOrder (to reset it)
				kOrder = []
				for a in range(0,len(jOrder)):
					kOrder.append(jOrder[a])
				# templateIndex = 2
				#print kOrder results
				kOrder.append(startOrder[k])
				kCurr = startOrder[k]
				# print("	kCurr=",kCurr)
				# print("          ",kOrder)
				#perform tests
				lenVsTemplate = compareLen(kOrder,currentTemplate) # test length
				if lenVsTemplate == '>':
					# print ("          Too long. Breaking.")
					break
				elif lenVsTemplate == '=':
					# print ("          CORRECT LENGTH")
					posVSTemplate = comparePOS(kOrder,currentTemplate) # test pos
					if posVSTemplate == True:
						# print ("          CORRECT POS\n\n")
						validatedOrders.append(kOrder)
				else: # if lenVsTemplate == '<'
					# print ("          Too short. Search deeper.")
					instance_lenMatch(templateIndex,kOrder,visualizeTabs='')	
			### end of instance_lenMatch()

	
		#Start first eval loop
		for i in range(0,len(startOrder)):
			iOrder = [startOrder[i]] #declare iOrder (to reset it)
			#test for length and pos
			lenVsTemplate = compareLen(iOrder,currentTemplate) # test length
			if lenVsTemplate == '>':
				# print ("          Too long. Breaking.")
				break
			elif lenVsTemplate == '=':
				# print ("          CORRECT LENGTH")
				posVSTemplate = comparePOS(iOrder,currentTemplate) # test pos
				if posVSTemplate == True:
					# print ("          CORRECT POS\n\n")
					validatedOrders.append(iOrder)
			else:
				instance_lenMatch(0,iOrder,'') #start the recursive search


	#back to broadest scope of orderByPos()
	if validatedOrders == []:
		validatedOrders = None #if empty, return None
	# else: #Commented out because I'm pretty sure removing duplicates is unnecessary.
	# 	#Remove duplicates 
	# 	import itertools 
	# 	validatedOrders.sort()
	# 	validatedOrders = list(validatedOrders for validatedOrders,_ in itertools.groupby(validatedOrders))
	return validatedOrders
	### end of orderByPos()
def pullQueryResults():
	"""Copies the most recent SQLite selection. Should ONLY be called after executing a SQLite query.
	----------Dependencies:
	import sqlite3
	learned_data.db in the folder learned_data
	the global variables 'dbConn' and 'dbCursor'

	----------Parameters:
	None
	----------Returns:
	a list, or None.
	"""
	#pull in whatever the most recent query selected
	dbData = dbCursor.fetchall() 
	#put the results into a list
	listToReturn = []
	for row in dbData:
		listToReturn.append(row[0])
	return listToReturn

	if listToReturn == []: # if no results, return None.
		return None
def refreshKnownCorpus():
	"""Update the global variable 'knownCorpus', from the file known_corpus_tokenized.py.
	----------Dependencies:
	import os, import sys
	known_corpus_tokenized.py (in this script's directory)

	----------Parameters:
	None

	----------Returns:
	None (content is pushed straight to the global variable named knownCorpus)
	"""
	#exec 'For each line of text, concat to string.' then exec 'exec of that string'.
	exec("stringOfKnownCorpus = '' \nwith open ('known_corpus_tokenized.py', 'rt', encoding='utf8') as f:\n\tfor line in f:\n\t\tstringOfKnownCorpus+=line\nexec(stringOfKnownCorpus)")


#Utilities with both internal and external dependencies:
def backupDB(): #internal dependency: generateUuid()
	"""Save a backup of learned_data.db, in the folder backup_databases, under a unique name.
	----------Dependencies:
	generateUuid()
	import os, import shutil
	learned_data.db in the folder learned_data
	
	----------Returns:
	True (unless a fatal error occurs)
	"""
	print("\tcreating backup of learned_data.db")
	newFileName = "learned_data_"+str(generateUuid())+".db"

	src_dir= absolute_filepath+"/learned_data"
	dst_dir= absolute_filepath+"/learned_data/backup_databases"
	src_file = os.path.join(src_dir, "learned_data.db")
	shutil.copy(src_file,dst_dir)

	dst_file = os.path.join(dst_dir, "learned_data.db")
	new_dst_file_name = os.path.join(dst_dir, newFileName)
	os.rename(dst_file, new_dst_file_name)

	return True
def determinePOS(termOrList,db=None): #internal dependency: pullQueryResults() 
	"""Looks up the part of speech of a term (or of list of terms). Returns it as a string (or as a list of strings). Recursive, but not infinitely recursive.
	----------Dependencies:
	pullQueryResults() 
	learned_data.db
	some compromise list #incomplete
	some yet-to-be-written textacy contextual analysis. #incomplete
	
	----------Parameters:
	termOrList = The word(s) to look up. A string (or a list of strings). 
	db = a string. the database to reference. The options are: "learned_data", "compromise", "textacy", and maybe one day "context".
	
	----------Returns:
	the POS (as a string). If none found, returns 'Unknown POS'.
	"""
	
	#If termOrList is a list of strings...
	if isinstance(termOrList,list):

		if len(termOrList) == 0:
			print("\t\tdeterminePOS() was passed an empty list. Returned 'Unknown POS'.")

		listWithPos = []
		for i in range (0,len(termOrList)):
			iPOS = determinePOS(termOrList[i])
			listWithPos.append([termOrList[i], iPOS])
		return listWithPos

	#If termOrList is a string...
	elif isinstance (termOrList,str):
		if db == "learned_data":
			#try to infinitize() the term #incomplete
			
			# determine POS 
			dbCursor.execute("""SELECT partOfSpeech FROM terms WHERE term = ?;""", (termOrList,))
			pos = pullQueryResults()
			#proactive error handling. return results.
			if isinstance(pos,list):
				if len(pos) == 1:
					return pos[0] #return the result. this is the most common scenario.
				elif len(pos) > 1:
					print("\t\t\tdeterminePOS() returned more than one POS for '%s'. It returned only the first result." % termOrList) 
					return pos[0] #return only the first search result
			elif pos == None or pos == []:
				print("\t\t\tdeterminePOS() could not find the POS of '%s'. Returned 'Unknown POS'." % termOrList)
				return 'Unknown POS' # return a string because thats what other functions are expecting to recieve. No (fatal) harm done if that string never matches anything useful.
			else:
				print("\t\t\tdeterminePOS() retreived a very bad value for '%s'. Returned 'Unknown POS'." % termOrList)
				return 'Unknown POS' # return a string because thats what other functions are expecting to recieve. No (fatal) harm done if that string never matches anything useful.

		elif db == "compromise":
			# print ("\t\t\tdeterminePOS() tried to reference compromise.")
			pos = None #incomplete
	
		elif db == "textacy":
			# print ("\t\t\tdeterminePOS() tried to reference textacy.")
			pos = None #incomplete
	
		elif db == None:
			#try calling self again with each of the three possible DBs. 
			result = determinePOS (termOrList,"learned_data") #try learned_data
			if result == None:
				result = determinePOS (termOrList,"compromise") #try compromise
				if result == None:
					result = determinePOS (termOrList,"textacy") #try textacy
					if result == None:
						#give up and return "Unknown POS".
						print("\t\t\tdeterminePOS() couldn't find a POS for '%s' anywhere." % termOrList)
						return("Unknown POS")
					else:
						return result
				else:
					return result
			else:
				return result
	
		else:
			print("A bad 'db' argument value was passed to determinePOS(). It was",str(db))

	#Else (if termOrList is not a string or a list) ...
	else:
		print("\t\tdeterminePOS() was passed a bad value - '%s'. Returned 'Unknown POS'." % termOrList)
		return("Unknown POS")



#{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
#{}
#{}	@@		Reading
#{}
#{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
def loadHtml(myURL,sourceToLoad="Unknown"):
	"""Download HTML from a webpage and push the useful parts of the text to temp_processing_text.txt.
	This function is called by read(). It should not be called directly.
	----------Dependencies:
	import os, import sys, import re, absolute_filepath

	----------Parameters:
	myURL (a string. must begin with http:// or https://)
	sourceToLoad (optional string)

	----------Returns:
	None (data is pushed directly to temp_processing_text.txt and temp_preprocessing_text.txt)
	"""
	#download webpage content and push to temp_preprocessing_text.txt
	import urllib.request
	with urllib.request.urlopen(myURL) as response:
		urlContent = response.read()
		# this can't be converted to a real string, until it's written to disk.
		with open(absolute_filepath+'/temp_preprocessing_text.txt', 'wb') as f: #wb stands for write as 'bytes'
			f.write(urlContent)
	del urlContent #save some memory

	#Pull from temp_preprocessing_text.txt
	urlContent_raw = []
	with open ('temp_preprocessing_text.txt', 'rt', encoding="utf8") as f:
		for line in f: #For each line of text, store in a string variable in the list urlContent_raw.
			urlContent_raw.append(line)
	assert len(urlContent_raw) > 0, "Hey, there is no content to pull from temp_preprocessing_text.txt"

	#Parse the HTML 
	urlContent_ready = []
	for i in range (0,len(urlContent_raw)):
		line = urlContent_raw[i]
		#remove leading indentations
		line = re.sub("\t", "", str(line))
		line = re.sub("  ", "", str(line))

		# Sort out what to keep.
		substringToKeep = None
			#keep titles
		if line[:5] == '<title>': #maybe try line.find instead, for reuters
			substringToKeep = line
			#keep headers
		elif line[:3] == '<h1' or line[:12] == '</figure><h1' or line[:3] == '<h2' or line[:12] == '</figure><h2' or line[:3] == '<h3' or line[:3] == '<h4' or line[:3] == '<h5' or line[:3] == '<h6' or line[:3] == '<h7':
			substringToKeep = line
			#keep paragraphs
		# print(line.find('<p '),line.find('<p>')) # for debugging reuters articles
		elif line[:3] == '<p>' or line[:3] == '<p ' or line[:12] == '</figure><p ': #for wikipedia articles
		# if line.find('<p ')>0 or line.find('<p>')>0: #for reuters articles
			substringToKeep = line
			# print(line)
		# #keep ul, ol, and li
		# elif line[:4] == '<ul>' or line[:4] == '<ul ' or line[:4] == '<ol>' or line[:4] == '<ol ' or line[:4] == '<li>' or line[:4] == '<li ':
		# 	substringToKeep = line
		# #keep tables, tr, td
		# elif line[:4] == '<table>' or line[:4] == '<table ' or line[:4] == '<tr>' or line[:4] == '<tr ' or line[:4] == '<td>' or line[:4] == '<td ':
		# 	substringToKeep = line
		else:
			pass #don't keep anything else.
		
		# If there's anything in substringToKeep, clean it up and append it.
		if substringToKeep != None:
			# print("I identified a line to keep.")

			#remove attributes
			substringToKeep = re.sub(' action="[^\"]*"', "", substringToKeep) #remove action attributes
			substringToKeep = re.sub(' action=\'[^\"]*\'', "", substringToKeep) #same, but with single-quotes
			substringToKeep = re.sub(' alt="[^\"]*"', "", substringToKeep) #remove alt attributes
			substringToKeep = re.sub(' alt=\'[^\"]*\'', "", substringToKeep) #same, but with single-quotes
			substringToKeep = re.sub(' class="[^\"]*"', "", substringToKeep) #remove class attributes
			substringToKeep = re.sub(' class=\'[^\"]*\'', "", substringToKeep) #same, but with single-quotes
			substringToKeep = re.sub(' href="[^\"]*"', "", substringToKeep) #remove href attributes
			substringToKeep = re.sub(' href=\'[^\"]*\'', "", substringToKeep) #same, but with single-quotes
			substringToKeep = re.sub(' id="[^\"]*"', "", substringToKeep) #remove id attributes
			substringToKeep = re.sub(' id=\'[^\"]*\'', "", substringToKeep) #same, but with single-quotes
			substringToKeep = re.sub(' lang="[^\"]*"', "", substringToKeep) #remove lang attributes
			substringToKeep = re.sub(' lang=\'[^\"]*\'', "", substringToKeep) #same, but with single-quotes
			substringToKeep = re.sub(' title="[^\"]*"', "", substringToKeep) #remove title attributes
			substringToKeep = re.sub(' title=\'[^\"]*\'', "", substringToKeep) #same, but with single-quotes
			substringToKeep = re.sub(' style="[^\"]*"', "", substringToKeep) #remove style attributes
			substringToKeep = re.sub(' style=\'[^\"]*\'', "", substringToKeep) #same, but with single-quotes
			#remove certain opening tags
			substringToKeep = re.sub('\<.\>', "", substringToKeep) #all 1-character tags, incl. <p>
			substringToKeep = re.sub('\<..\>', "", substringToKeep) #all 2-character tags, incl. <p>
			substringToKeep = re.sub('\<...\>', "", substringToKeep) #all 3-character tags, incl. <p>
			substringToKeep = re.sub('<span>', "", substringToKeep)
			substringToKeep = re.sub('<strong>', "", substringToKeep)
			#remove ALL closing tags
			substringToKeep = re.sub("<\/[^>]*>", "", substringToKeep) 

			#clean up specific websites in a specific way
			if sourceToLoad == "wikipedia": #If it's wikipedia...
				substringToKeep = re.sub('\[.\]', "", substringToKeep) #delete 1-digit footnotes
				substringToKeep = re.sub('\[..\]', "", substringToKeep) #delete 2-digit footnotes
				substringToKeep = re.sub('\[...\]', "", substringToKeep) #delete 3-digit footnotes
				substringToKeep = re.sub('\[....\]', "", substringToKeep) #delete 3-digit tags
				substringToKeep = re.sub('\[citation', "", substringToKeep) #delete [citation needed] Note: this is not currently working - try printing the line here, to fix.
				substringToKeep = re.sub('\[citation need', "", substringToKeep) #same
				substringToKeep = re.sub('\[citation needed\]', "", substringToKeep) #same
				substringToKeep = re.sub('needed\]', "", substringToKeep) #same
				#delete these suseless headings:
				if substringToKeep == "Contents\n" or substringToKeep == "External links\n" or substringToKeep == "Further reading\n" or substringToKeep == "Navigation menu\n" or substringToKeep == "References\n" or substringToKeep == "See also\n" or substringToKeep == "In other projects\n" or substringToKeep == "Interaction\n":
					substringToKeep = ""
				elif substringToKeep == "Languages\n" or substringToKeep == "More\n" or substringToKeep == "Namespaces\n" or substringToKeep == "Navigation\n" or substringToKeep == "Notes\n" or substringToKeep == "Personal tools\n" or substringToKeep == "Print/export\n" or substringToKeep == "Tools\n" or substringToKeep == "Views\n" or substringToKeep == "Works cited\n":
					substringToKeep = ""
				else:
					pass
			if sourceToLoad == "bbc" and i == 0: #If it's BBC...
				substringToKeep = "" #delete the first index bc its just a bunch of javascript

			urlContent_ready.append(substringToKeep)
	del urlContent_raw #save some memory
	# print (urlContent_ready)
	if len(urlContent_ready) == 0:
		return ("BAD REQUEST\t\tNo content matched the criteria to push to temp_processing_text.txt.")

	#Push to temp_processing_text.txt
	with open(absolute_filepath+'/temp_processing_text.txt', 'w', encoding='utf-8') as f:
		for i in range (0,len(urlContent_ready)):
			f.write(urlContent_ready[i])
	del urlContent_ready #save some memory
def loadText(textToLoad):
	"""Push a string to temp_processing_text.txt.
	This function is called by read(). It should not be called directly.
	----------Dependencies:
	import os, absolute_filepath

	----------Parameters:
	textToLoad

	----------Returns:
	None (data is pushed directly to temp_processing_text.txt)
	"""
	textToLoad = str(textToLoad)
	textToLoad += "\n011001010110111001100100" #to make sure there is always at least one line in the txt file, so that doc can be saved.

	#Empty temp_preprocessing_text.txt (for consistency, because loadHtml does too).
	with open(absolute_filepath+'/temp_preprocessing_text.txt', 'w', encoding='utf-8') as f:
		f.write("")

	#Push textToLoad to temp_processing_text.txt
	with open(absolute_filepath+'/temp_processing_text.txt', 'w', encoding='utf-8') as f:
		f.write(textToLoad)
def tokenize(source,title):
	"""Pull text from temp_processing_text.txt, save its bag of terms and log having read it.
	----------Dependencies:
	temp_processing_text.txt (in this script's directory). This is the text that gets tokenized.
	known_corpus (folder in this script's directory)
	import os, absolute_filepath (global variable)
	generateUuid()
		import uuid

	----------Parameters:
	source (a string)
	title (a string)

	----------Returns:
	None
	"""
	#Pull text from temp_processing_text.txt
	textToTokenize = ""
	with open ('temp_processing_text.txt', 'r', encoding="utf8") as f:
		for line in f: #For each line of text, store in a string variable in the list urlContent_raw.
			textToTokenize += line+"\n"

	#generate a unique key for this reading
	docName = generateUuid()
	#create the doc and metadata (because tokenization can't happen until the doc is created)
	metadata = {
		'title': title,
		'source': source,
		'myKey' : docName} 
	doc = textacy.Doc(textToTokenize, metadata=metadata, lang="en") 

	#create a json bag of terms. convert it to a python list.
	docTermsJson = doc.to_bag_of_terms(ngrams=2, named_entities=True, normalize='lemma', as_strings=True)
	docTerms = []
	for key, value in docTermsJson.items():
		docTerms.append([key,value])
	del docTermsJson

	#sort the list
	docTerms = sortLists(docTerms,1,'largestToSmallest')

	#Place terms with above-average frequency (>1 mentions) into primaryTerms. Place all terms into secondaryTerms.
	primaryTerms = []
	secondaryTerms = []
	for i in range (0,len(docTerms)):
		if docTerms[i][1] > 1:
			primaryTerms.append(docTerms[i][0])
		secondaryTerms.append(docTerms[i][0])
	# set title = the most common term (if any terms exist)
	if len(docTerms) > 0:
		title = docTerms[0][0] 
	else:
		title = 'Untitled'
	#This is better than <h1> bc it is tokenized in the same way that the terms in other network nodes, are tokenized. But another option is to search through primaryTerms and find the first (or longest) one that matches the first line of temp_processing_text.txt, and use that term instead.
	
	#overwrite previous metadata now that there's a real title
	metadata = {
		'title': title,
		'source': source,
		'myKey' : docName} 
	doc = textacy.Doc(textToTokenize, metadata=metadata, lang="en") 
	
	#save the doc
	doc.save(absolute_filepath+'/known_corpus', name=docName)

	#generate final list of all data/vectors
	newTopic = [docName,knowledgePriorityLevel,title,[source],primaryTerms,secondaryTerms,False]

	# update known_corpus_tokenized.py
	newTopic = str(newTopic)+","+"\n] # the last line in the file must be a ]." # add ] to newTopic
	lines = open(absolute_filepath+'/known_corpus_tokenized.py', encoding="utf8").readlines()
	open(absolute_filepath+'/known_corpus_tokenized.py', encoding="utf8").close()
	w = open(absolute_filepath+'/known_corpus_tokenized.py','w', encoding="utf8")
	w.writelines([item for item in lines[:-1]]) #delete the last line of the file
	w.close()
	#add newTopic as the last 2 lines of the file
	with open(absolute_filepath+'/known_corpus_tokenized.py', 'a', encoding="utf8") as f: #a means append
		f.write(newTopic)
	#update the global variable 'knownCorpus'
	refreshKnownCorpus()

	# #save the name of this reading (docName) in the file table_of_contents.txt
	# with open(absolute_filepath+'/known_corpus/table_of_contents.txt', 'a') as f: #a means append
	#	 f.write('\n'+docName)
	print ("I've finished reading about %s." % title)
def read(readRequest):
	"""Use the format of a read request, to detrmine the reading's content and metadata. Then call a function to read it.
	----------Dependencies:
	tokenize()
		generateUuid ()

	----------Parameters:
	readRequest

	----------Returns:
	True: if it executes the whole function successfully.
	The learned data is saved directly to known_corpus_tokenized.txt and to /known_corpus
	"""
	sourceToRead = None
	textToRead = None
	titleToRead = None
	urlToRead = None
	requiresHtmlParse = None

	if readRequest[:9] == 'read http':
		#determine source
		wiki = None #if it's wikipedia, then it's wikipedia
		if readRequest.find("wikipedia.") > 0:
			sourceToRead = "wikipedia"
		else: #if it's not wikipedia, then the source is the domain name
			sourceToRead = readRequest[5:] #remove the word 'read '
			if sourceToRead[:4] == "http":
				startPos = 3 + re.search("://", sourceToRead).start()
			else:
				startPos = 0
			sourceToRead = sourceToRead[startPos:]
			periodPos = re.search("\.", sourceToRead).start()
			sourceToRead = sourceToRead[:periodPos]
		#determine text (the content)
		textToRead = None
		#title wont be determined until the text is tokenized
		titleToRead = "Unknown"
		requiresHtmlParse = True
		#determine urlToRead
		urlToRead = readRequest[5:] #everything after 'read '
		print ("I will try to read the following:")

	elif readRequest[:15] == 'read this from ':
		#determine source
		sourceToRead = readRequest[15:]
		colonPos = re.search(":", sourceToRead).start()
		sourceToRead = sourceToRead[:10]
		#determine text (the content)
		textToRead = re.split("read this from .*:", readRequest)
		textToRead = textToRead[1]
		titleToRead = 'Unknown' #final title wont be determined until the text is tokenized
		requiresHtmlParse = False
		print ("I will try to read the following:")

	else:
		sourceToRead = 'Unknown'
		#determine text (the content)
		textToRead = readRequest[5:]
		titleToRead = 'Unknown' #final title wont be determined until the text is tokenized
		requiresHtmlParse = False
		print ("I will try to read the following:")


	print ("\tsourceToRead:",sourceToRead)
	print ("\ttextToRead:",textToRead)
	print ("\ttitleToRead:",titleToRead)
	print ("\turlToRead:",urlToRead)
	print ("\trequiresHtmlParse:",requiresHtmlParse)

	#load content into temp_processing_text.txt and save doc & metadata to known_corpus folder
	if requiresHtmlParse == True:
		loadHtml(urlToRead,sourceToRead) 
	else:
		loadText(textToRead)

	#tokenize temp_processing_text.txt
	tokenize(sourceToRead,titleToRead)
	return True



#{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
#{}
#{}	@@		Remembering, Recalling, Reflecting
#{}
#{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
# 
refreshKnownCorpus()

#Remembering (one topic, in-depth)
# rememberedText = textacy.Doc.load('~/Desktop', name='myFolkReading')  #incomplete
# print('  rememberedText:')
# print(rememberedText)

#Recalling (many topics, shallowly)
def matchCorpusTopic_simple(inputTopic,thoroughness='med'):
	# currently this is written to search the corpus. I also need a version to scrub the search tree for knownTerms

	print("\tinputTopic: ",inputTopic) #for debugging
	matchedKeys = []
	matchedNames = []
	matchedTerms = []

	if thoroughness == 'low': #search titles only.
		topicListIndex = 4
		#(not written yet)
	elif thoroughness == 'med': #search primaryTerms (incl. titles)
		topicListIndex = 4
	for i in range (0,len(knownCorpus)): #for each topic...
		for j in range (0,len(knownCorpus[i][topicListIndex])): #in the appropriate list of terms..
			print ("\t\trunning...")
			#if its a match, change the boolean in index 6.
			if knownCorpus[i][topicListIndex][j] == inputTopic:
				knownCorpus[i][6] = True
				print("\t\tj=",j)
				break #no need to test the rest of that topic
			else:
				pass
	if thoroughness == 'high': #search secondaryTerms (incl. titles and primaryTerms)
		topicListIndex = 5
	elif thoroughness == 'highest':
		pass #incomplete
		#(not written yet)
		#compary secondary terms to secondary terms.




	#save the keys, names, and terms for all matches
	for i in range (0,len(knownCorpus)): #for each topic...
		if knownCorpus[i][6] == True:
			matchedKeys.append = knownCorpus[i][0] #add key to list
			matchedNames.append = knownCorpus[i][2] #add name to list
			for j in range (0,len(knownCorpus[i][topicListIndex])):
				matchedTerms.append = knownCorpus[i][topicListIndex][j] #add term to list


	print ("\toutput:", matchedNames) #for debugging
	return [matchedKeys, matchedNames, matchedTerms]
### def triggerNetwork() #incomplete

	# assert len(knownCorpus) > 0, "No content exists in the global variable knownCorpus. Most likely, known_corpus_tokenized.py was not successfully imported by updateTopicsKnown().\nImport that file before calling matchTopic()." 

	# #fetch the name of the inputTopic
	# for i in range (0,len(knownCorpus)):
	# 	print("len(knownCorpus): ",len(knownCorpus))
	# 	if knownCorpus[i][0] == inputKey:
	# 		inputName = knownCorpus[i][0]
	# #if no topics match, return an error
	# elif knownCorpus[i][len(knownCorpus)] and knownCorpus[i][0] != inputKey: 
	# 	currentError = "You passed a bad starting value to start the network. it doesnt exist."
	# 	return currentError

#Reflecting (learning, cleanup, pattern recognition on saved data)
def gerundsToVerbs(): #incomplete
	pass #change to an infinitive whenever the gerund can be found in knownTerms of compromiseConjugations.
def updateChildTerms(): #incomplete
	pass #this should be unnecessary once child tables can CASCADE/DELETE rows on UPDATE
def deleteSimpleDuplicates(): #incomplete
	#An overloaded function. takes the optional argument 'knownCorpus'. Otherwise, operates on 'knownTerms'.
	#delete duplicate entries and categories from knownTerms (or knownCorpus). pushToDisk() when done.
	pass
def updateDefComp():
	print ("\t\tupdating each def_comprehensive in the table 'terms'.")
	wordsWithDefComp = [
		["517223ec_2018-04-08_17-27", "def_comp_include.py"],
		["f71e490c_2018-04-08_17-27", "def_comp_define.py"],
	]

	for i in range (0,len(wordsWithDefComp)): #for each word with a comprehensive definition
		currentKey = wordsWithDefComp[i][0]
		currentFileName = absolute_filepath+"/learned_data/"+wordsWithDefComp[i][1]
		currentDefAsString = ""

		#pull contents of .py file into a string
		with open (currentFileName, 'r', encoding="utf8") as f:
			for line in f: #For each line of text, store in a string variable in the list urlContent_raw.
				currentDefAsString += line+"\n"

		#push the string to the database
		dbCursor.execute("""UPDATE terms SET def_comprehensive = ? WHERE key = ? """, (currentDefAsString,currentKey,))
	dbConn.commit()
def deduceTerms(): #incomplete
	#expand number of terms known, by creating new entries from any duplicate categories (e.g. color from entries with the category 'color')
	#could do the same with topics
	pass 
def deleteNestedDuplicates(): #incomplete
	pass #delete duplicate entries and categories from knownTerms (or knownCorpus). pushToDisk() when done.
def createNeuralShortcuts_1(): #incomplete
	pass #I haven't done any work on nerual shortcuts yet.
def reflectOnKnownData(): #incomplete
	#An overloaded function. takes optional arguments such as 'knownCorpus', 'knownTerms', and later, others.
	# If no argument is passed in, operates on every available argument, one at a time.
	#pushToDisk(knownTerms or knownCorpus or whatever other knownLibrary)
	pass 
#also: for every category that's not already a term, make it a term. then when reading, if the word is used, textacy can infer the POS. it can then be assigned. from one sample, yes. it can be validated periodically, later.
#also: expand findVerbs() somehow, to at least include the verb 'include' for all categories



#{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
#{}
#{}	@@		Writing
#{}
#{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}

#{}{}{}{}{}{}{}{}{}{}{}{}{}{}@@@  Known Meanings
#The core knownMeanings of some (but not all) knownTerms. The terms themselves are stored in known_terms.py. Meanings are recognized patterns, and therefore, some may exist which do not exist as terms in English. They may be represented as pandas DataFrames or something else.
#   General Utilities for knownMeanings *I may move these up to te Remembering section at some point.
#   Definitions of knownMeanings (storage)			 NOTES:
	# -None of these meanings should be nouns; nouns are defined by only their "defining categories," which are stored in known_terms.py. Instead these terms should be concepts which cannot be described using a platonic ideal.
	# -All of these functions are overloaded: 
		# whenever wordContext == "evaluate", the function will evaluate the accuracy of the term with respect to the arguments passed into the function
		# whenever wordContext == "learn", the function will attempt to integrate the input information, into known_terms.py; 
		# whenever wordContext == "perform", the function will attempt to perform the verb/become the adjective/perform the adverb/etc; 
def meaning_include(wordContext,myCategory,myWord,indirectObject):
	"""Defines the core meaning of the term "include". 
	----------Dependencies:
	isDefiningCategory()

	----------Parameters:
	wordContext = a string: "evaluate" or "learn" or "perform"
	myCategory = a string
	myWord = a string
	indirectObject = a string

	----------Returns:
	a boolean (True if term evaluates to True, or if the info is learned/performed successfuly in the wordContext. Else, False.)
	"""
	indirectObject = "havent written this yet" #I haven't yet gotten around to indirect objects in any of these definitions yet. also this is only needed in the imperative context; otherwise its just the subject. #incomplete

	#Handle errors non-fatally
	if wordContext != "evaluate" and wordContext != "learn" and wordContext != "perform": # validate wordContext
		print( "Error - an invalid 'wordContext' of '%s' was passed to one of the knownMeanings. wordContext must be 'evaluate' or 'learn' or 'perform'.  The function reutrned None, rather than a Boolean." % wordContext)
		return None
	for i in range (0, len(meaning_include)):
		if isinstance (meaning_include[i], str):
			pass
		else:
			print( "Error - a value which was not a string, was passed to one of the knownMeanings. The function reutrned None, rather than a Boolean.")
			return None


	# if wordContext is 'evaluate':
	if wordContext == "evaluate":
		if isDefiningCategory(myWord,myCategory) == True: # incomplete. write a utility search tree
			print("Evaluating...  The category %s includes %s." % (myCategory,myWord)) 
			return True
		else:
			print("Evaluating...  The category %s does not include %s." % (myCategory,myWord)) 
			return False

	# if wordContext is 'learn':
	# if wordContext == "perform":
	#	check if the myCategory already exists as an entry in knownTerms. if so, pass. else, create it. 
	#	append myWord to its index 3.
	#	When done reading the whole user input... (i.e., not in this function)
	#		pushToDisk(knownTerms)
	#		refreshKnownTerms()

	# if wordContext is 'perform':
	if wordContext == "perform":
		if indirectObject == None:
			print ("I was instructed to 'include' something within myself. However, I cannot modify my own code.") #incomplete
			return False
		else:
			print ("I was instructed to 'include' something within something else. However, I don't know how to do that.") #incomplete
			return False
def meaning_define(wordContext,subject,directObject):
	"""Defines the core meaning of the term "define". 
	----------Dependencies:
	findIndexOfString()

	----------Parameters:
	wordContext = a string: "evaluate" or "learn" or "perform"
	subject = a string
	directObject = a string
	indirectObject = a string

	----------Returns:
	if perform: a string (e.g. "Penguin is characterized by aquatic and not flying.")
	else: a boolean (True if term evaluates to True, or if the info is learned successfuly in the wordContext. Else, False.)
	"""
	indirectObject = "havent written this yet" #I haven't yet gotten around to indirect objects in any of these definitions yet #incomplete

	#Handle errors non-fatally
	if wordContext != "evaluate" and wordContext != "learn" and wordContext != "perform": # validate wordContext
		print( "Error - an invalid 'wordContext' of '%s' was passed to one of the knownMeanings. wordContext must be 'evaluate' or 'learn' or 'perform'.  The function reutrned None, rather than a Boolean." % wordContext)
		return None
	for i in range (0, len(meaning_define)):
		if isinstance (meaning_define[i], str):
			pass
		else:
			print( "Error - a value which was not a string, was passed to one of the knownMeanings. The function reutrned None, rather than a Boolean.")
			return None


	# if wordContext is 'perform':
	myDefCats = "" #i.e. 'my defining categories'
	miscProperties = [] #any category without a POS tag
	negation = '' #by default, there is no negation.
	subjectIndex = findIndexOfString(subject,knownTerms,0)

	#oops i forgot to return False or "i dont understand", whenever it's a bad request. #incomplete
	
	for i in range (0,len(knownTerms[subjectIndex][2])):
		myCategory = knownTerms[subjectIndex][2][i]
		if myCategory[:4] == 'not ':
			negation = 'not '
			myCategory = myCategory[4:]
			print("myCategory =",myCategory)
		if type(findIndexOfString(myCategory,knownTerms,0)) == int: #if the category is a term of its own...
			categoryIndex = findIndexOfString(myCategory,knownTerms,0)
			if knownTerms[categoryIndex][1] == 'NOUN':
				myDefCats += "being %sa %s " % (negation,knownTerms[categoryIndex][0])
			if knownTerms[categoryIndex][1] == 'VERB':
				myDefCats += "%sbeing able to %s " % (negation,knownTerms[categoryIndex][0])
			if knownTerms[categoryIndex][1] == 'ADJ':
				myDefCats += "%sbeing %s " % (negation,knownTerms[categoryIndex][0])
		else:
			myDefCats += "like %s " % myCategory

		#make the list more grammatical
		if i < len(knownTerms[subjectIndex][2])-1:
			myDefCats += "and "

	return("%s is characterized by %s." % (subject, myDefCats)) # this marks the exact moment when I realized I should've used a SQL database.

	# if wordContext is 'learn'
	#	check if the directObject already exists as an entry in knownTerms. if so, pass. else, create it. 
	#	append subject to its index 2.
	#	When done reading the whole user input... (i.e., not in this function)
	#		pushToDisk(knownTerms)
	#		refreshKnownTerms()

	# if wordContext is 'evaluate':
	if isDefiningCategory(directObject,subject) == True:
		return True
	else: # Note: even if the answer is unknown, this returns false.
		return False 
def meaning_number(wordContext,subject):
	"""Defines the core meaning of the term "number". 
	----------Dependencies:
	None

	----------Parameters:
	wordContext = a string: "evaluate" or "learn" or "perform"
	subject = a string
	----------Returns:
	a boolean (True if term evaluates to True, or if the info is learned successfuly in the wordContext. Else, False.)
	"""
	#Handle errors non-fatally
	if wordContext != "evaluate" and wordContext != "learn" and wordContext != "perform": # validate wordContext
		print( "Error - an invalid 'wordContext' of '%s' was passed to one of the knownMeanings. wordContext must be 'evaluate' or 'learn' or 'perform'.  The function reutrned None, rather than a Boolean." % wordContext)
		return None


	# if wordContext is 'evaluate':
	if wordContext == 'evaluate':
		subject = float(subject)
		if isinstance(subject, float) == True:
			print("Evaluating...  %s is a number." % (str(subject))) 
			return True
		else:
			print("Evaluating...  %s is not a number." % (str(subject))) 
			return False

	# if wordContext is 'learn':
	if wordContext == 'learn':
		print("Learning new types of numbers is both difficult and currently unnecessary. The function returned False.") # incomplete
		return False

	# if wordContext is 'perform':
	if wordContext == "perform":
		print ("I was instructed to 'perform' a number. However, this makes no conceptual sense. The function returned False.")
		return False
def meaning_longer(wordContext,subject,comparedObject):
	"""Defines the core meaning of the term "longer". 
	----------Dependencies:
	None

	----------Parameters:
	wordContext = a string: "evaluate" or "learn" or "perform"
	subject = preferably a string
	comparedObject = preferably a string

	----------Returns:
	a boolean (True if term evaluates to True, or if the info is learned successfuly in the wordContext. Else, False.)
	"""
	#Handle errors non-fatally
	if wordContext != "evaluate" and wordContext != "learn" and wordContext != "perform": # validate wordContext
		print( "Error - an invalid 'wordContext' of '%s' was passed to one of the knownMeanings. wordContext must be 'evaluate' or 'learn' or 'perform'.  The function reutrned None, rather than a Boolean." % wordContext)
		return None


	# if wordContext is 'evaluate':
	if wordContext == 'evaluate':
		subject = str(subject)
		comparedObject = str(comparedObject)
		if len(subject) > len(comparedObject):
			print("Evaluating...  %s is longer than %s." % (str(subject), str(comparedObject) )) 
			return True
		else:
			print("Evaluating...  %s is not longer than %s." % (str(subject), str(comparedObject) )) 
			return False

	# if wordContext is 'learn':
	if wordContext == 'learn':
		print ("I haven't written this part of the function yet") #incomplete
		return False

	# if wordContext is 'perform':
	if wordContext == "perform":
		print ("I was instructed to perform 'longer', which does not make sense without more context. The function returned False.")
		return False

#   Handler for knownMeanings 
	# This determines which definitions to call. If all of the called functions return True, then the term is applicable. Unfortunately this list can't be stored in a separate file, or else it can't access knownTerms.
knownMeanings = [ 
	# [ each line contains...
		# "the term", 
		# "the POS", 
		# [a test that evaluates to a boolean when wordContext=="evaluate". if all the booleans are True, then the meaning is applicable within a given wordContext],
		# use the customSearchTree in the meaning definition. If False, default to search tree scSearchTree
		# {'the types of information which the concept expresses': any object,},
	# ],
	["include", "VERB", [meaning_include], True, {'detail':True},],
	["define", "VERB", [meaning_define], True, {'general':True},],
	["number", "NOUN", [meaning_number], False, {'math':True,'detail':True},],
	["longer", "ADJ", [meaning_longer], False, {'compare':True,'physical':True,'size':True,'space':True,},],
	#other non-physical terms to learn:  say, find, difficult, know, know of, write, read, get, make
]


#{}{}{}{}{}{}{}{}{}{}{}{}{}{}@@@  Selecting Responses
def scSearchTree(inputTerm):
	pass #incomplete
	# find a fast way to pull al terms which metnion the inputTerm anywhere in the knownTerm.
	#Return a list of the knownTerms indeces which contain matching terms



#{}{}{}{}{}{}{}{}{}{}{}{}{}{}@@@  General writing utilities
def findObject(conceptType=None): #currently not being used at all
	"""Returns a list of objects which can be taken by a verb.
	----------Dependencies:
	learned_data.db
	----------Parameters:
	conceptType = a list of strings. see the table 'terms_conceptType' for suggested string values.
	*verb is not a parameter. because in English, pretty much any verb can take any noun as an object. I think.
	----------Returns:
	a list of strings which are appropriate verbs. 
	or None (rather than []), if none are found.
	"""
	possObj = []

	def appQR(qr):
		"""Append queryResults to possObj."""
		if isinstance(qr,list) and len(qr)>0: #fail gracefully
			for j in range(0,len(qr)):
				possObj.append(qr[j])	
	
	#error handling
	if isinstance(conceptType,str):
		conceptType = [conceptType] #in case user forgot to make conceptType a list

	#if only a conceptType was provided
	if isinstance(conceptType,list):
		# find the nouns that match the conceptType
		for i in range (0,len(conceptType)):
			# print (conceptType[i],"?")
			dbCursor.execute("""
				SELECT terms.term FROM terms
				INNER JOIN terms_conceptType on terms_conceptType.terms_key = terms.key
				WHERE partOfSpeech = "NOUN" AND conceptType = ?
				""", (conceptType[i],))
			queryResults = pullQueryResults()
			appQR(queryResults) #append results to possObj

	#if no arguments were provided, search for ALL nouns
	elif conceptType==None:
		dbCursor.execute("""
			SELECT term FROM terms
			WHERE partOfSpeech = 'NOUN';
			""")
		queryResults = pullQueryResults()
		appQR(queryResults) #append results to possObj
	
	else: #if none of the above options for the arguments
		print("\t\t\tA bad argument '%s' was passed to possObj(). Did not search for nouns. Returned None." % str(conceptType))
		return None
	
	if possObj == []:
		possObj = None
	return possObj
def findVerbs(conceptType=None,subject=None):
	"""Returns a list of verbs which match the provided criteria.
	----------Dependencies:
	learned_data.db
	----------Parameters:
	conceptType = a list of strings. see the table 'terms_conceptType' for suggested string values.
	subject = a string
	----------Returns:
	a list of strings which are appropriate verbs. 
	or None (rather than []), if none are found.
	"""
	possVerbs = []

	def appQR(qr):
		"""Append queryResults to possVerbs."""
		if isinstance(qr,list) and len(qr)>0: #fail gracefully
			for j in range(0,len(qr)):
				possVerbs.append(qr[j])	
	
	#error handling
	if isinstance(conceptType,str):
		conceptType = [conceptType] #in case user forgot to make conceptType a list

	#if only a conceptType was provided
	if (isinstance(conceptType,list) and subject==None):
		# find the verbs that match the conceptType
		for i in range (0,len(conceptType)):
			# print (conceptType[i],"?")
			dbCursor.execute("""
				SELECT terms.term FROM terms
				INNER JOIN terms_conceptType on terms_conceptType.terms_key = terms.key
				WHERE partOfSpeech = "VERB" AND conceptType = ?
				""", (conceptType[i],))
			queryResults = pullQueryResults()
			appQR(queryResults) #append results to possVerbs

	#if only a subject was provided
	elif (conceptType==None and isinstance(subject,str)):
		# find the verbs that match the subj
		subjectCateg = findCategories(subject)
		for i in range (0,len(subjectCateg)):
			# print (subjectCateg[i],"?")
			dbCursor.execute("""
				SELECT term FROM terms
				WHERE partOfSpeech = 'VERB' AND term = ?;
				""", (subjectCateg[i],))
			queryResults = pullQueryResults()
			appQR(queryResults) #append results to possVerbs

	#if both conceptType and subject were provided
	elif (isinstance(conceptType,list) and isinstance(subject,str)):
		#constrain found set by both
		subjectCateg = findCategories(subject)
		for h in range (0,len(subjectCateg)):
			for i in range (0,len(conceptType)):
				# print (conceptType[i],"?")
				dbCursor.execute("""
					SELECT terms.term FROM terms
					INNER JOIN terms_conceptType on terms_conceptType.terms_key = terms.key
					WHERE partOfSpeech = "VERB" AND terms.term = ? AND conceptType = ?;
					""", (subjectCateg[h],conceptType[i],))
				queryResults = pullQueryResults()
				appQR(queryResults) #append results to possVerbs

	#if no arguments were provided, search for ALL verbs
	elif (conceptType==None and subject==None):
		dbCursor.execute("""
			SELECT term FROM terms
			WHERE partOfSpeech = 'VERB';
			""")
		queryResults = pullQueryResults()
		appQR(queryResults) #append results to possVerbs
	
	else: #if none of the above options for the arguments
		print("\t\t\tA bad argument was passed to findVerbs(). Did not search for verbs. Returned None.")
		print("\t\t\t"+str(conceptType)+", "+str(subject))
		return None
	
	if possVerbs == []:
		possVerbs = None
	return possVerbs

# also priority communications, e.g. traditional Responses, executing/answering Imperatives, answering Questions, etc.
	
#{}{}{}{}{}{}{}{}{}{}{}{}{}{}@@@  Complex writing functions
def evalScTruth(statement):
	"""Evaluate whether a statement is true. Attempt to apply evaluation criteria in the following order:
		1. def_comprehensive
		2. def_deduced
		3. I dont remember.
	----------Dependencies:
	learned_data.db and maybe others idk.
	----------Parameters:
	statement = a list of lists containing Term-POS pairs.
	----------Returns:
	a boolean. Or, if there's literally no info, None.
	"""
	return statement #### STOPPED HERE FOR LOCAL HD. #incomplete
def freewrite_declarative(**kwargs): # start with kws and fill in blanks. save possibles.
	"""Tries to write a sentence with the words passed in. Recursive, but not infinitely recursive.
	----------Arguments:
		Can take the following kwargs, all of which are optional:
			miscList = a list of strings to try and make a sentence out of			
			conceptType = a string. see the table 'terms_conceptType' for suggested values.
			posTemplates = a list of lists of strings. Can be obtained using findPosTemplates().
			st = a boolean. stands for searchTree. Tells the function whether to cascade down category lists while trying to write a sentence (e.g. from duck to bird to vertebrate).
			n = an integer. the number of times this function has called itself. this should never be entered manually; it's automatic.
			
			subject = a string
			verb = a string
			... and hopefully more parts of speech one day. Be sure to update the "indvKwargs" and "recursive" sections below, if you add more kwargs. 
	
	----------Dependencies:
		determinePOS()
		findPosTemplates()
		orderByPos()
		removeDuplicates()
		findCategories(), which is located in learned_data/util_findCategories.py
		isCategoryInstance(), which is located in learned_data/util_isCategoryInstance.py
		and any of the following, depending on which kwargs were passed in...
			findObject() #this one's currently not being used, actually
			findVerbs()
			... etc.
	
	----------Returns:
	A list of lists of lists of strings. i.e.: 
		list = [sentence, sentence, ..., n]
			sentence = [termGroup, termGroup, ..., n]
				termGroup = ['term', 'POS']
	Or None, if nothing could be constructed.
	""" #Answer questions in some other, unrelated function. Note: when responding to statements or questions I usually evaluate sentence relevance and structure before searching for content.
	
	#Pull in the kwargs. Assign empty string kwargs = None.
	conceptType = kwargs["conceptType"] if ("conceptType" in kwargs) else None
	miscList = kwargs["miscList"] if ("miscList" in kwargs) else []
	n = kwargs["n"] if ("n" in kwargs) else 0
	posTemplates = kwargs["posTemplates"] if ("posTemplates" in kwargs) else None
	st = kwargs["st"] if ("st" in kwargs) else False #might change default to True. not sure yet.
	subject = kwargs["subject"] if ("subject" in kwargs) else None
	verb = kwargs["verb"] if ("verb" in kwargs) else None

	possSc = []
	# print("~~~~~New Rec.  n =",str(n)) #for debugging

	############## RECURSIVE STUFF - expanding miscList ##############

	if n == 0: 
		print("\tfreewrite_declarative()") #for debugging
		#Handle bad arguments.
		if isinstance(miscList,str):
			miscList = [miscList] #in case user forgot to make miscList a list

		#make all arguments lowercase #incomplete

		#infinitize all arguments #incomplete

		#regardless of whether miscList has any content, append each POS kwarg to miscList. Note: POS kwargs can be ignored whenever we're not in the outer-most scope.
		indvKwargs = [subject,verb]
		for i in range (0,len(indvKwargs)):
			if indvKwargs[i] != None:
				miscList.append(indvKwargs[i])

		#continue on to the non-recursive stuff.
	
	if n == 1: #If in first recursion:
		print ("\t\tfreewrite_declarative() is expanding the miscList...") #for debugging
		#if a subject or conceptType was provided, add all matching verbs.
		if subject != None or conceptType != None:
			addMe = findVerbs(conceptType,subject)
			addMeWithPOS = []
			if isinstance(addMe,list) and len(addMe) > 0: #fail gracefully
				addMeWithPOS = determinePOS(addMe) #Add a POS for each word
				if len(addMeWithPOS) > 0: #fail gracefully
					for i in range (0,len(addMeWithPOS)):
						miscList.append(addMeWithPOS[i])

		#add all the categories of each term
		if isinstance(miscList,list) and len(miscList)>0: #fail gracefully
			for i in range(0,len(miscList)):
				addMe = findCategories(miscList[i][0])
				addMeWithPOS = []
				if isinstance(addMe,list) and len(addMe) > 0: #fail gracefully
					addMeWithPOS = determinePOS(addMe) #Add a POS for each word
					if len(addMeWithPOS) > 0: #fail gracefully
						for h in range (0,len(addMeWithPOS)):
							miscList.append(addMeWithPOS[h])

		#continue on to the non-recursive stuff.

	if n == 2: #If in second recursion:
		# print ("\t\tfreewrite_declarative() is expanding miscList even more...") #for debugging
		#for every noun in miscList, add every verb/conceptType. no searchTree.
		verbsToAdd = []
		for i in range (0,len(miscList)):
			currTG = miscList[i]
			if currTG[1] == "NOUN":
				addMe = findVerbs(conceptType,currTG[0])
				if isinstance(addMe,list) and len(addMe) > 0: #fail gracefully
					for j in range (0,len(addMe)):
						verbsToAdd.append(addMe[j])
		# print("\t\t\tverbsToAdd=",str(verbsToAdd))
		
		if len(verbsToAdd) > 0: #fail gracefully
			for i in range (0,len(verbsToAdd)):
				addMeWithPOS = []
				currTerm = verbsToAdd[i]
				currPOS = determinePOS(currTerm) #Add a POS for each word
				if len(currPOS) > 0: #fail gracefully. This works, but note that currPOS = str, not a list.
					addMeWithPOS = [currTerm,currPOS]
					miscList.append(addMeWithPOS)

		
		#for every verb, in miscList, run findObject().
		# incomplete (findObject() doesn't test for most common objects...)

		#continue on to the non-recursive stuff.

	if n == 3: #If in third recursion:
		# print ("\t\tfreewrite_declarative() is expanding miscList to the max!") #for debugging
		pass #For each term in miscList, use word vectors/free association to add related terms #incomplete
		
		#continue on to the non-recursive stuff.

	if n >= 4:
		return None #Give up.

	############## NON-RECURSIVE STUFF - constructing sentences ##############	
	####### Construct word arrangements
	#If miscList contains any content...
	if isinstance(miscList,list) and len(miscList) > 0: #fail gracefully
		# print("miscList =",str(miscList)) #for debugging
		if n == 0:
			miscList = determinePOS(miscList) #Add a POS for each word in miscList
		
		#If no posTemplates...
		if posTemplates == None:
			#Pull ALL posTemplates
			reqTemplates = findPosTemplates()
			results = orderByPos(reqTemplates,miscList) #retrieve grammatical arrangements of the words
			#save the results
			if isinstance(results,list) and len(results) > 0: #fail gracefully
				for i in range(0,len(results)):
					possSc.append(results[i])

		#If posTemplates...
		elif isinstance(posTemplates,list):
			if len(posTemplates) > 0: #fail gracefully
				#retrieve grammatical arrangements of the words. 
				results = orderByPos(posTemplates,miscList)
				#save the results
				if isinstance(results,list) and len(results) > 0: #fail gracefully
					for j in range(0,len(results)):
						possSc.append(results[j])
			#In the future, maybe pull templates by their associated tags instead?

		possSc = removeDuplicates(possSc) #eliminate any duplicate sentences

	####### Filter by any requested specifications
	if len(possSc) > 0: #fail gracefully
		
		if isinstance(conceptType,str): # ...filter by conceptType.
			#Keep only the possible sentences with the requested conceptType.
			filteredSc = []
			for i in range (0,len(possSc)): #for each sentence:
				for j in range (0,len(possSc[i])): #for each word:
					dbCursor.execute("""SELECT conceptType FROM terms_conceptType WHERE term = ?;""", (possSc[i][j][0],))
					localCT = pullQueryResults()
					if isinstance(localCT,list): #fail gracefully
						for k in range (0,len(localCT)):
							#if the db conceptType == the requested one, append the term.
							if localCT[k] == conceptType: 
								filteredSc.append(possSc[i])
								break #no need to test the rest of the sentence
							else:
								pass
			possSc = []
			possSc = filteredSc
			possSc = removeDuplicates(possSc) #eliminate duplicate sentences
	
		if isinstance(subject,str): # ...filter by subject.
			#Keep only the possible sentences with the requested subject.
			filteredSc = []
			for i in range (0,len(possSc)): #for each sentence:
				for j in range (0,1): #keep it iff first or second word==subject.
					if possSc[i][j][0] == subject:
						filteredSc.append(possSc[i])
						break #no need to test the rest of the sentence
					else:
						print ("\t not appended")
			possSc = []
			possSc = filteredSc
		
		if isinstance(verb,str): # ...filter by verb.
			print("\t\tfreewrite_declarative() couldn't filter possSc by a verb because that's too complex of a task. No filtering took place.")
	else:
		pass #print ("\t\t\tfreewrite_declarative() tried to filter possSc, but it already empty...")

	####### Filter by truth + relevance
	#test each possSc for truth
	# scToEval = [] #sentences to evaluate #later

	#Determine which sentences are most relevant
	# -relevance to current conversation
	# -how many recursions were needed (0-1 by .20s)
	# -whate are the chances thatthe user already knows the info (0-1)
	# research more tests/weights
	# use ML to weight the coefficients of each test, then hard code those coefficients (for now)

	
	


	# print("miscList=",str(miscList)) #for debugging
	# print("possSc=",str(possSc)) #for debugging
	
	
	#Return results if there are any.
	if len(possSc) > 0:
		return possSc
	else:
		#start next recursion
		n = n+1
		moreResults = freewrite_declarative (
			conceptType = conceptType,
			miscList = miscList,
			n = n,
			posTemplates = posTemplates,
			st = st,
			subject = subject,
			verb = verb)
		return moreResults






#{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
#{}
#{}	@@		Main Loop
#{}
#{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
#This section exists simply for testing. The finalized file will call functions in a different way.

# availableSc = freewrite_declarative(miscList=["number"])
# print("\n---availableSc:")
# eow(availableSc,True) #prints results from eow()

finalResult = freewrite_declarative(miscList=["penguin"])
eow(finalResult,True)



print("\n===== Script Ended =====")