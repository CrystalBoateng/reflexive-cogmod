#{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
#{}
#{}	@@		Load dependencies and global variables
#{}
#{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}

# import dependencies
from datetime import datetime # to generate UUIDs
from learned_data.util_find_categories import * # to link terms
from learned_data.util_is_category_instance import * # to evaluate terms' category relationships
from operator import itemgetter # to sort lists of lists
import itertools #  to remove_duplicates()
import json # to read doc metadata
import os # to read and write from disk, and backup database
import re # to parse html
import shutil # for creating database backups
import sqlite3 # for reading/writing to database
import sys # to delete and reload python files
import textacy # to create docs/doc metadata, and to lemmatize and tokenize unstructured text
import uuid # to generate UUIDs

# declare global variables
absolute_filepath = os.path.dirname(__file__) # the absolute filepath of this script
knowledge_priority_level = 1
sentences_just_written = 0 # number of sentences written since last user input
max_sentences_at_once = 10 # limits how many sentences can be written without user input
test_mode = True
dbConn = sqlite3.connect(absolute_filepath+'/learned_data/learned_data.db') #connects to database
dbCursor = dbConn.cursor() #connects to database
# dbCursor.execute("PRAGMA foreign_keys=ON") #allows SQLite foreign key deletion/update on cascade
# TODO: imports variable compromiseConjugations, to help parse conjugated verbs:
# from nlp_resources.compromise_conjugations_mod import * 


#{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
#{}
#{}	@@		General utilities
#{}
#{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}

# Utilities with no dependencies on external files:
def every_other_word(input,p=False):
	"""Take a list of lists of lists of words. Return it, but with Every Other Word omitted. Useful for removing parts of speech from sentences to print.
		Or, if p == True, prints the altered list before returning it.
	----------Dependencies:
	None

	----------Parameters:
	input = list of lists of lists of words.
		Example: [
			[['bird', 'NOUN'], ['fly', 'VERB']], 
			[['number', 'NOUN'], ['include', 'VERB'], ['eight', 'ADV']]
		]
	p = a boolean. If True, prints directly from this function.
	
	----------Return:
	A list of lists of strings, e.g.:
		Example: [
			['bird', 'fly'], 
			['number', 'include', 'eight']
		]
	"""
	errors = 0
	output = []
	if input and isinstance(input,list):
		for i in range(len(input)):
			sentence = input[i]
			newSc = []
			if sentence and isinstance(sentence,list):
				for j in range(len(sentence)):
					termGroup = sentence[j]
					
					if termGroup and isinstance(termGroup,list):
						newSc.append(termGroup[0])
					else:
						errors += 1
						print("  ERROR - Bad value in every_other_word() parameter:",str(termGroup))
				if p and newSc: # print the input if requested.
					toPrint = ""
					for j in range(len(newSc)):
						toPrint = "%s %s" % (toPrint,newSc[j])
					print(" |",toPrint)
			else:
				errors += 1
				print("  ERROR - Bad value in every_other_word() parameter:",str(sentence))
			output.append(newSc)
	else:
		errors += 1
		print("  ERROR - Bad value passed to every_other_word().")
	if errors > 0:
		print("  The full list of values passed to every_other_word() was:",str(output))
	if p == False:
		return(output)
	else:
		return output
def find_possible_templates():
	"""Return every possible sentence template. 
	----------Dependencies:
	None.
	
	----------Parameters:
	None.
	
	----------Dependencies:
	A list of lists containing strings which are parts of speech.
	"""
	allSctemplates = [
		["NOUN", "VERB"],
		["NOUN", "VERB", "NOUN"],
	]
	return allSctemplates
def generate_uuid(order=None):
	"""Generate a reasonably unique ID string based on date and time.
	----------Dependencies:
	import uuid
	import os or from datetime import datetime

	----------Parameters:
	None

	----------Return:
	a string (e.g. '2018_11_26-9_13-85894b2f')
	"""
	dateAndTime = datetime.now()
	randomId = str(uuid.uuid4())[:6] # generate a UUID and truncate it
	if order == "random-first":
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
def remove_duplicates(myList):
	"""Take a list. Return it with only the unique values.
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
def sort_lists(myLists,index,order):
	"""Take a list of lists. Return it, sorted by a given index.
	----------Dependencies:
	from operator import itemgetter

	----------Parameters:
	myLists (a list of lists. one item in each of the lists should be an int.)
	index (the index to sort by)
	order Smallest-to-largest is Python's default. If that's not what you want, write 'largestToSmallest'

	----------Return:
	the same list you passed in, but sorted.
	"""
	sortedLists = sorted(myLists, key=itemgetter(index))
	if order == "largestToSmallest":
		sortedLists = list(reversed(sortedLists))
	return sortedLists

# Utilities with dependencies on external files:
def clean_up_temp_files():
	"""Delete the content in temp_preprocessing_text.txt and temp_processing_text.
	----------Dependencies:
	temp_preprocessing_text
	temp_processing_text.txt
	
	----------Return:
	True
	"""
	with open(absolute_filepath+'/temp_preprocessing_text.txt', 'w') as f:
		f.write("")
	with open(absolute_filepath+'/temp_processing_text.txt', 'w') as f:
		f.write("")
def infinitize(word,pos=None):
	pass 
	# TODO: try infinitizing using textacy, then (via regular expressions) the using learned_data.db and lastly, using compromise.
def order_by_pos(templates,words):
	"""Return every possible order of the words passed in, which is both the correct length AND has the correct parts of speech.
	----------Dependencies:
	None

	----------Parameters:
	templates = a list of lists containing strings which are parts of speech. find_possible_templates() can provide these templates.
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

	----------Return:
	A list containing all possible arrangements of those words, which match the POS in the templates. The arrangements are grammatical, but have not yet been tested for truth.
	"""
	validatedOrders = []
	
	#Error handling
	if templates == None or templates == []:
		print("\t\t\torder_by_pos() was called with templates = None or templates = []. Returned None.")
		return None
	if words == None or words == []:
		print("\t\t\torder_by_pos() was called with words = None or words = []. Returned None.")
		return None
	for h in range(0,len(templates)):
		currentTemplate = templates[h]
		startOrder = words
		def compareLen(testList,testTemplate):
			"""Take a list. Return the string '<' or '=' or '>'. """
			if len(testList) < len(testTemplate):
				return "<"
			elif len(testList) == len(testTemplate):
				return "="
			else:
				return ">"
		def comparePOS(testPOS,templatePOS):
			"""Compare the POS in test list, to the POS in template list, at the requestedindex only. If they match, return True.
			Note: Only test phrases vetted as the correct length ever get passed to this function."""
			threshold = len(testPOS)
			correctPOS = 0
			for p in range(0,len(testPOS)):
				if testPOS[p][1] == templatePOS[p]:
					correctPOS += 1
			if correctPOS >= threshold:
				return True
			else:
				return False
		def instance_lenMatch(templateIndex,jOrder,visualizeTabs=''):
			"""An infinitely recursive function. Append any orders with the correct length and POS', to validatedOrders."""
			#break out of infinite loops
			templateIndex += 1
			for m in range(0,templateIndex):
				visualizeTabs += '  '
			if templateIndex > len(currentTemplate):
				print("%stemplateIndex=%s:   jOrder=%s" % (visualizeTabs,templateIndex,jOrder))
				print("\na possible infinite loop was detected, so an instance_lenMatch() recursive search was terminated.\n")
				return False
			## display the tests and recursion level (for debugging).
			# print("%stemplateIndex=%s:   jOrder=%s" % (visualizeTabs,templateIndex,jOrder))
			# try adding an element to eval loop.
			for k in range(len(startOrder)):
				#recreate kOrder (to reset it)
				kOrder = []
				for a in range(0,len(jOrder)):
					kOrder.append(jOrder[a])
				# print the kOrder results
				kOrder.append(startOrder[k])
				kCurr = startOrder[k]
					# test the sentence's length
				lenVsTemplate = compareLen(kOrder,currentTemplate) 
				if lenVsTemplate == '>':
					break
				elif lenVsTemplate == '=':
					# if correct lengeth, test the sentence's parts of speech
					posVSTemplate = comparePOS(kOrder,currentTemplate) 
					if posVSTemplate:
						validatedOrders.append(kOrder)
				else: 
					# if lenVsTemplate == '<', template is too short. 
					# start a deeper recursion.
					instance_lenMatch(templateIndex,kOrder,visualizeTabs='')	
			### end of instance_lenMatch()
	
		# start the first eval loop
		for i in range(0,len(startOrder)):
			iOrder = [startOrder[i]] # declare iOrder (to reset it)
			# test for length and pos
			lenVsTemplate = compareLen(iOrder,currentTemplate) # test length
			if lenVsTemplate == '>':
				# sentence is too long
				break
			elif lenVsTemplate == '=':
				# sentence is of matching length
				posVSTemplate = comparePOS(iOrder,currentTemplate) # test pos
				if posVSTemplate:
					# sentence is of matching parts of speech
					validatedOrders.append(iOrder)
			else:
				# begin a recursive search
				instance_lenMatch(0,iOrder,'') 

	# if grammatically correct sentences were found anywhere, return them.
	if validatedOrders == []:
		return None
	else:
		return validatedOrders
def pull_query_results():
	"""Copies the most recent SQLite selection. Should ONLY be called after executing a SQLite query.
	----------Dependencies:
	import sqlite3
	learned_data.db in the folder learned_data
	the global variables 'dbConn' and 'dbCursor'

	----------Parameters:
	None
	----------Return:
	A list. If no results were passed in, the returned list will be empty.
	"""
	# pull in whatever results the most recent query selected
	dbData = dbCursor.fetchall() 
	# put those results into a list
	listToReturn = []
	for row in dbData:
		listToReturn.append(row[0])
	return listToReturn
def execute_def_comp(requestedTerm,wordContext,subject=None,vIerb=None,do=None,io=None,adjAdv=None):
	"""	Executes a currentDef() located in the column 'def_comprehensive' in the table 'terms'.
	Note: This function's query can only return ONE row at a time, from the table 'terms'. Avoid passing in any terms which could return >1 row.

	----------Dependencies:
	learned_data.db in the folder learned_data
	pull_query_results()
	
	----------Parameters:
	requestedTerm = a string. the term to execute the def_comprehensive of.
	wordContext = a string. options are: 'evaluate', 'learn', or 'perform'
	subject = a string. 
	verb = a string. 
	do = a string. 
	io = a string. 
	adjAdv = a string. 

	----------Return:
	Whatever the function currentDef returns, for a given term. This function can be found in the column def_comprehensive for a given term in the table terms.
	"""
	def print_arguments():
		print("\t\t\t\trequestedTerm=",requestedTerm)
		print("\t\t\t\twordContext=",wordContext)
		print("\t\t\t\tsubject=",subject)
		print("\t\t\t\tverb=",verb)
		print("\t\t\t\tdo=",do)
		print("\t\t\t\tio=",io)
		print("\t\t\t\tadjAdv=",adjAdv)
	dbCursor.execute("""SELECT def_comprehensive FROM terms WHERE term = ?;""", (requestedTerm,))
	dbData = pull_query_results()
	if isinstance(dbData,list):
		# report errors
		if len(dbData) == 0:
			print("\t\t\tA bad argument was passed to execute_def_comp(), so no def_comprehensive was found. Returned None. \n\t\t\t\tArguments passed in:")
			print_arguments()
			return None
		if len(dbData) > 1:
			print("\t\t\tA bad argument was passed to execute_def_comp(), resulting in mulltiple files found. Only the first result was used.\n\t\t\tArguments passed in:")
			print_arguments()
		# import the currentDef as string
		functionAsString = dbData[0]
		# call the currentDef() located in the executed string
		# print(functionAsString+"\t.\n\t.\n\t.")
		exec(functionAsString,globals()) # bring the currentDef into global scope
		defResult = currentDef(wordContext,subject,verb,do,io,adjAdv) # call the currentDef
		# print("\tresults=",str(defResult))
		return defResult
	else:
		print("\t\t\tA bad argument was passed to execute_def_comp(), so no def_comprehensive was found. Returned None. \n\t\t\tArguments passed in:")
		print_arguments()
		return None
def refresh_known_corpus():
	"""Update the global variable 'knownCorpus', from the file known_corpus_tokenized.py.
	----------Dependencies:
	import os, import sys
	known_corpus_tokenized.py (in this script's directory)

	----------Parameters:
	None

	----------Return:
	None (content is pushed straight to the global variable named knownCorpus)
	"""
	# execute 'For each line of text, concat to string.' 
	# then execute 'execution of that string'.
	exec("stringOfKnownCorpus = '' \nwith open ('known_corpus_tokenized.py', 'rt', encoding='utf8') as f:\n\tfor line in f:\n\t\tstringOfKnownCorpus+=line\nexec(stringOfKnownCorpus)")


#Utilities with both internal and external file dependencies:
def backup_database(): # internal dependency: generate_uuid()
	"""Save a backup of learned_data.db, in the folder backup_databases, under a unique name.
	----------Dependencies:
	generate_uuid()
	import os, import shutil
	learned_data.db in the folder learned_data
	
	----------Return:
	True (unless a fatal error occurs)
	"""
	print("\tcreating backup of learned_data.db")
	newFileName = "learned_data_"+str(generate_uuid())+".db"
	src_dir = absolute_filepath + "/learned_data"
	dst_dir = absolute_filepath + "/learned_data/backup_databases"
	src_file = os.path.join(src_dir, "learned_data.db")
	shutil.copy(src_file,dst_dir)
	dst_file = os.path.join(dst_dir, "learned_data.db")
	new_dst_file_name = os.path.join(dst_dir, newFileName)
	os.rename(dst_file, new_dst_file_name)
	return True
def determine_pos(termOrList,db=None): #internal dependency: pull_query_results() 
	"""Look up the part of speech of a term (or of a list of terms). Return it as a string (or list of strings). Recursive, but not infinitely recursive.
	----------Dependencies:
	pull_query_results() 
	learned_data.db
	# TODO: some compromise list
	# TODO: some yet-to-be-written textacy contextual analysis.
	
	----------Parameters:
	termOrList = The word(s) to look up. A string (or a list of strings). 
	db = a string. the database to reference. The options are: "learned_data", "compromise", "textacy", and maybe one day "context".
	
	----------Return:
	The POS (as a string). If none found, return 'Unknown POS'.
	"""
	
	#If termOrList is a list of strings...
	if isinstance(termOrList,list):

		if len(termOrList) == 0:
			print("\t\tdetermine_pos() was passed an empty list. Returned 'Unknown POS'.")

		listWithPos = []
		for i in range(len(termOrList)):
			iPOS = determine_pos(termOrList[i])
			listWithPos.append([termOrList[i], iPOS])
		return listWithPos

	#If termOrList is a string...
	elif isinstance(termOrList,str):
		if db == "learned_data":
			# TODO: try to infinitize() the term
			
			# determine POS 
			dbCursor.execute("""SELECT partOfSpeech FROM terms WHERE term = ?;""", (termOrList,))
			pos = pull_query_results()
			# proactive error handling. return results.
			if isinstance(pos,list):
				if len(pos) == 1:
					# return the one result. this is the most common scenario.
					return pos[0]
				elif len(pos) > 1:
					print("\t\t\tdetermine_pos() returned more than one POS for '%s'. It returned only the first result." % termOrList) 
					return pos[0] #return only the first search result
			elif len(pos) == 0:
				print("\t\t\tdetermine_pos() could not find the POS of '%s'. Returned 'Unknown POS'." % termOrList)
				return 'Unknown POS' # return a string no matter what.
			else:
				print("\t\t\tdetermine_pos() received a very unexpected error when querying the POS of '%s'. Returned 'Unknown POS'." % termOrList)
				return 'Unknown POS' # return a string no matter what.

		elif db == "compromise":
			# TODO: add parts-of-speech from compromise
			pos = None
	
		elif db == "textacy":
			# TODO: deduce part-of-speech using Textacy
			pos = None 
	
		elif db == None:
			# try calling this function using learned_data.db
			result = determine_pos (termOrList,"learned_data") 
			if result:
				return result
			# try calling this function using compromise
			result = determine_pos (termOrList,"compromise") 
			if result:
				return result
			# try calling this function using textacy
			result = determine_pos (termOrList,"textacy") 
			if result:
				return result
			else:
				# give up and return "Unknown POS".
				# print("\t\t\tdetermine_pos() couldn't find a POS for '%s' anywhere." % termOrList)
				return("Unknown POS")

		else:
			print("determine_pos() was asked to query a non-existent database:",str(db))
	# otherwise, if termOrList is not a string or a list...
	else:
		print("\t\tdetermine_pos() was passed a bad value - '%s'. Returned 'Unknown POS'." % termOrList)
		return("Unknown POS")



#{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
#{}
#{}	@@		Reading
#{}
#{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
def load_html(myURL,sourceToLoad="Unknown"):
	"""Download HTML from a webpage and push the useful parts of the text to temp_processing_text.txt.
	This function is called by read(). It should not be called directly.
	----------Dependencies:
	import os, import sys, import re, absolute_filepath

	----------Parameters:
	myURL (a string. must begin with http:// or https://)
	sourceToLoad (optional string)

	----------Return:
	None (data is pushed directly to temp_processing_text.txt and temp_preprocessing_text.txt)
	"""
	# download webpage content and push to temp_preprocessing_text.txt
	import urllib.request
	with urllib.request.urlopen(myURL) as response:
		urlContent = response.read()
		# write to disk so that this can then be converted to a real string.
		with open(absolute_filepath+'/temp_preprocessing_text.txt', 'wb') as f:
			f.write(urlContent)
	# pull from temp_preprocessing_text.txt
	urlContent_raw = []
	with open('temp_preprocessing_text.txt', 'rt', encoding="utf8") as f:
		for line in f:
			urlContent_raw.append(line)
	if len(urlContent_raw) < 1:
		print("There is no content to pull from temp_preprocessing_text.txt!")
	# parse the HTML 
	urlContent_ready = []
	for i in range(len(urlContent_raw)):
		line = urlContent_raw[i]
		#remove leading indentations
		line = re.sub("\t", "", str(line))
		line = re.sub("  ", "", str(line))
		# choose what text to keep.
		substringToKeep = None
			#keep titles
		if line[:5] == '<title>':
			substringToKeep = line
			# keep headers
		elif line[:3] == '<h1' or line[:12] == '</figure><h1' or line[:3] == '<h2' or line[:12] == '</figure><h2' or line[:3] == '<h3' or line[:3] == '<h4' or line[:3] == '<h5' or line[:3] == '<h6' or line[:3] == '<h7':
			substringToKeep = line
			# keep paragraphs
		elif line[:3] == '<p>' or line[:3] == '<p ' or line[:12] == '</figure><p ': #for wikipedia articles
			substringToKeep = line
		else:
			pass # don't keep anything else.
		# if there's anything in substringToKeep, clean it up and append it.
		if substringToKeep:
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
			#clean up specific wikipedia article in a specific way
			if sourceToLoad == "wikipedia":
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
			urlContent_ready.append(substringToKeep)
	if len(urlContent_ready) == 0:
		return ("BAD REQUEST\t\tNo content matched the criteria to push to temp_processing_text.txt.")
	# push content to temp_processing_text.txt
	with open(absolute_filepath+'/temp_processing_text.txt', 'w', encoding='utf-8') as f:
		for i in range(len(urlContent_ready)):
			f.write(urlContent_ready[i])
def load_text(textToLoad):
	"""Push a string to temp_processing_text.txt.
	This function is called by read(). It should not be called directly.
	----------Dependencies:
	import os, absolute_filepath

	----------Parameters:
	textToLoad

	----------Return:
	None (data is pushed directly to temp_processing_text.txt)
	"""
	textToLoad = str(textToLoad)
	# make sure there is always at least one line in the txt file, so that doc can be saved.
	textToLoad += "\n011001010110111001100100" 
	# empty temp_preprocessing_text.txt (for consistency, because loadHtml does too).
	with open(absolute_filepath+'/temp_preprocessing_text.txt', 'w', encoding='utf-8') as f:
		f.write("")
	# push textToLoad to temp_processing_text.txt
	with open(absolute_filepath+'/temp_processing_text.txt', 'w', encoding='utf-8') as f:
		f.write(textToLoad)
def tokenize(source,title):
	"""Pull text from temp_processing_text.txt, save its bag of terms and log having read it.
	----------Dependencies:
	temp_processing_text.txt (in this script's directory). This is the text that gets tokenized.
	known_corpus (folder in this script's directory)
	import os, absolute_filepath (global variable)
	generate_uuid()
		import uuid

	----------Parameters:
	source (a string)
	title (a string)

	----------Return:
	None
	"""
	# pull text from temp_processing_text.txt
	textToTokenize = ""
	with open('temp_processing_text.txt', 'r', encoding="utf8") as f:
		for line in f:
			textToTokenize += line+"\n"
	# generate a unique key for this reading
	docName = generate_uuid()
	# create the doc and metadata (because tokenization can't happen until the doc is created)
	metadata = {
		'title': title,
		'source': source,
		'myKey' : docName} 
	doc = textacy.Doc(textToTokenize, metadata=metadata, lang="en") 
	# create a json bag of terms. convert it to a python list.
	docTermsJson = doc.to_bag_of_terms(ngrams=2, named_entities=True, normalize='lemma', as_strings=True)
	docTerms = []
	for key, value in docTermsJson.items():
		docTerms.append([key,value])
	# sort the list
	docTerms = sort_lists(docTerms,1,'largestToSmallest')
	# place terms with above-average frequency (>1 mentions) into... 
	# ...primaryTerms. place all terms into secondaryTerms.
	primaryTerms = []
	secondaryTerms = []
	for i in range(len(docTerms)):
		if docTerms[i][1] > 1:
			primaryTerms.append(docTerms[i][0])
		secondaryTerms.append(docTerms[i][0])
	# set title = the most common term (if any terms exist)
	if len(docTerms) > 0:
		title = docTerms[0][0] 
	else:
		title = 'Untitled'
	# overwrite previous metadata now that a semantic title has been chosen
	metadata = {
		'title': title,
		'source': source,
		'myKey' : docName} 
	doc = textacy.Doc(textToTokenize, metadata=metadata, lang="en") 
	# save the doc
	doc.save(absolute_filepath+'/known_corpus', name=docName)
	# generate the final list of all data
	newTopic = [docName,knowledge_priority_level,title,[source],primaryTerms,secondaryTerms,False]
	# update known_corpus_tokenized.py
	newTopic = str(newTopic)+","+"\n] # the last line in the file must be a ]." # add ] to newTopic
	lines = open(absolute_filepath+'/known_corpus_tokenized.py', encoding="utf8").readlines()
	open(absolute_filepath+'/known_corpus_tokenized.py', encoding="utf8").close()
	w = open(absolute_filepath+'/known_corpus_tokenized.py','w', encoding="utf8")
	w.writelines([item for item in lines[:-1]]) #delete the last line of the file
	w.close()
	# add newTopic as the last 2 lines of the file. 'a' means append.
	with open(absolute_filepath+'/known_corpus_tokenized.py', 'a', encoding="utf8") as f: 
		f.write(newTopic)
	# update the global variable 'knownCorpus'
	refresh_known_corpus()
	print("I've finished reading about %s." % title)
def read(readRequest):
	"""Use the format of a read request, to detrmine the reading's content and metadata. Then call a function to read it.
	----------Dependencies:
	tokenize()
		generateUuid ()

	----------Parameters:
	readRequest

	----------Return:
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
		wiki = None
		if readRequest.find("wikipedia.") > 0:
			sourceToRead = "wikipedia"
		else: # if it's not wikipedia, then the source is the domain name
			sourceToRead = readRequest[5:] # remove the word 'read '
			if sourceToRead[:4] == "http":
				startPos = 3 + re.search("://", sourceToRead).start()
			else:
				startPos = 0
			sourceToRead = sourceToRead[startPos:]
			periodPos = re.search("\.", sourceToRead).start()
			sourceToRead = sourceToRead[:periodPos]
		# determine text (the content)
		textToRead = None
		# title wont be determined until the text is tokenized
		titleToRead = "Unknown"
		requiresHtmlParse = True
		# determine urlToRead
		urlToRead = readRequest[5:] #everything after 'read '
	elif readRequest[:15] == 'read this from ':
		# determine source
		sourceToRead = readRequest[15:]
		colonPos = re.search(":", sourceToRead).start()
		sourceToRead = sourceToRead[:10]
		# determine text (the content)
		textToRead = re.split("read this from .*:", readRequest)
		textToRead = textToRead[1]
		titleToRead = 'Unknown' # final title wont be determined until the text is tokenized
		requiresHtmlParse = False
	else:
		sourceToRead = 'Unknown'
		# pull out the text to read.
		textToRead = readRequest[5:]
		# use temporary title. final title isn't determined until text is tokenized.
		titleToRead = 'Unknown' 
		requiresHtmlParse = False
	print("I will try to read the following:")
	print("\tsourceToRead:",sourceToRead)
	print("\ttextToRead:",textToRead)
	print("\ttitleToRead:",titleToRead)
	print("\turlToRead:",urlToRead)
	print("\trequiresHtmlParse:",requiresHtmlParse)
	# load content into temp_processing_text.txt .
	# also, save doc & metadata to known_corpus folder.
	if requiresHtmlParse:
		load_html(urlToRead,sourceToRead) 
	else:
		load_text(textToRead)
	# tokenize temp_processing_text.txt
	tokenize(sourceToRead,titleToRead)
	return True



#{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
#{}
#{}	@@		Remembering, Recalling, Reflecting
#{}
#{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
# 
refresh_known_corpus()

#Remembering (one topic, in-depth)
def remember_text():
	pass # TODO: pull most common terms from the corpus reading. example:
	# rememberedText = textacy.Doc.load('~/Desktop', name='myFolkReading')  
	# print('  rememberedText:')
	# print(rememberedText)

#Recalling (many topics, shallowly)
def match_corpus_topic_simple(inputTopic,thoroughness='med'):
	# TODO: currently this is written to search the corpus. I also need a version to scrub the search tree for known terms.
	print("\tmatch_corpus_topic_simple():\n\tinputTopic: ",inputTopic) #for debugging only
	matchedKeys = []
	matchedNames = []
	matchedTerms = []
	if thoroughness == 'low': #search titles only.
		topicListIndex = 4
		#(not written yet)
	elif thoroughness == 'med': #search primaryTerms (incl. titles)
		topicListIndex = 4
	for i in range(len(knownCorpus)): #for each topic...
		for j in range(len(knownCorpus[i][topicListIndex])): #in the appropriate list of terms..
			print("\t\trunning...")
			#if its a match, change the boolean in index 6.
			if knownCorpus[i][topicListIndex][j] == inputTopic:
				knownCorpus[i][6] = True
				print("\t\tj=",j)
				break # no need to test the rest of that topic
			else:
				pass
	if thoroughness == 'high': #search secondaryTerms (incl. titles and primaryTerms)
		topicListIndex = 5
	elif thoroughness == 'highest':
		pass # TODO: compare secondary terms to secondary terms.

	# save the keys, names, and terms for all matches
	for i in range(len(knownCorpus)): # for each topic...
		if knownCorpus[i][6]:
			matchedKeys.append = knownCorpus[i][0] # add key to list
			matchedNames.append = knownCorpus[i][2] # add name to list
			for j in range(len(knownCorpus[i][topicListIndex])):
				matchedTerms.append = knownCorpus[i][topicListIndex][j] # add term to list
	# print("\toutput:", matchedNames) # for debugging only
	return [matchedKeys, matchedNames, matchedTerms]
def trigger_network(): 
	pass # TODO: initiate a recursive nerual network seearch
	# assert len(knownCorpus) > 0, "No content exists in the global variable knownCorpus. Most likely, known_corpus_tokenized.py was not successfully imported by updateTopicsKnown().\nImport that file before calling matchTopic()." 
	# #fetch the name of the inputTopic
	# for i in range(len(knownCorpus)):
	# 	print("len(knownCorpus): ",len(knownCorpus))
	# 	if knownCorpus[i][0] == inputKey:
	# 		inputName = knownCorpus[i][0]
	# #if no topics match, return an error
	# elif knownCorpus[i][len(knownCorpus)] and knownCorpus[i][0] != inputKey: 
	# 	currentError = "You passed a bad starting value to start the network. it doesnt exist."
	# 	return currentError

#Reflecting (learning, cleanup, pattern recognition on saved data)
def gerunds_to_verbs():
	pass # TODO: change to an infinitive whenever the gerund can be found in knownTerms of compromiseConjugations.
def update_child_terms():
	pass # TODO: write this function
	# this function is will become unnecessary once child tables can CASCADE/DELETE rows on UPDATE
def delete_simple_duplicates():
	pass # TODO: write this function.
	# An overloaded function. takes the optional argument 'knownCorpus'. Otherwise, operates on 'knownTerms'.
	# Deletes duplicate entries and categories from database (and/or known_corpus).
def deduce_terms(): 
	pass # TODO: write this function.
	# expand number of terms known, by creating new entries from any duplicate categories (e.g. a new color from two entries with the category 'color')
	# could do the same with topics
def delete_nested_duplicates():
	pass #TODO: delete duplicate entries and categories from learned_data.db
def reflect_on_known_data():
	pass # TODO: Run every function in the "reflecting"section above.
	# Takes optional arguments such as 'learned_data.db', 'knownTerms', and later, others.
	# If no argument is passed in, operates on every available argument, one at a time.
	#pushToDisk(knownTerms or knownCorpus or whatever other knownLibrary)



#{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
#{}
#{}	@@		Writing
#{}
#{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}

#{}{}{}{}{}{}{}{}{}{}{}{}{}{}@@@  Selecting Responses
def sentence_search_tree(inputTerm):
	pass # TODO:
	# efficiently pull all terms which mention the inputTerm anywhere in the knownTerm.
	# return a list of the knownTerms indeces which contain matching terms

#{}{}{}{}{}{}{}{}{}{}{}{}{}{}@@@  General writing utilities
def find_object(conceptType=None):
	"""Return a list of objects which can be taken by a verb.
	----------Dependencies:
	learned_data.db
	----------Parameters:
	conceptType = a list of strings. see the table 'terms_conceptType' for suggested string values.
	*verb is not a parameter. because in English, pretty much any verb can take any noun as an object. I think.
	----------Return:
	a list of strings which are appropriate verbs. 
	or None (rather than []), if none are found.
	"""
	possObj = []
	def append_to_possVerbs(qr):
		"""Append queryResults to possObj."""
		if qr and isinstance(qr,list):
			for j in range(0,len(qr)):
				possObj.append(qr[j])	
	
	# error handling
	if isinstance(conceptType,str):
		conceptType = [conceptType] # in case user forgot to make conceptType a list
	# if only a conceptType was provided
	if isinstance(conceptType,list):
		# find the nouns that match the conceptType
		for i in range(len(conceptType)):
			# print(conceptType[i],"?")
			dbCursor.execute("""
				SELECT terms.term FROM terms
				INNER JOIN terms_conceptType on terms_conceptType.terms_key = terms.key
				WHERE partOfSpeech = "NOUN" AND conceptType = ?
				""", (conceptType[i],))
			queryResults = pull_query_results()
			append_to_possVerbs(queryResults) # append results to possObj
	# if no arguments were provided, search for ALL nouns
	elif conceptType == None:
		dbCursor.execute("""
			SELECT term FROM terms
			WHERE partOfSpeech = 'NOUN';
			""")
		queryResults = pull_query_results()
		append_to_possVerbs(queryResults) # append results to possObj
	else: # otherwise, if none of the above options for the arguments....
		print("\t\t\tA bad argument '%s' was passed to possObj(). Did not search for nouns. Returned None." % str(conceptType))
		return None
	
	if possObj:
		return possObj
	else:
		return None
def find_verbs(conceptType=None,subject=None):
	"""Return a list of verbs which match the provided criteria.
	----------Dependencies:
	learned_data.db
	----------Parameters:
	conceptType = a list of strings. see the table 'terms_conceptType' for suggested string values.
	subject = a string
	----------Return:
	a list of strings which are appropriate verbs. 
	or None (rather than []), if none are found.
	"""
	possVerbs = []
	def append_to_possVerbs(qr):
		"""Append queryResults to possVerbs."""
		if qr and isinstance(qr,list):
			for j in range(0,len(qr)):
				possVerbs.append(qr[j])	
	
	# error handling
	if isinstance(conceptType,str):
		conceptType = [conceptType] # in case user forgot to make conceptType a list
	# if only a conceptType was provided
	if (isinstance(conceptType,list) and subject == None):
		# find the verbs that match the conceptType
		for i in range(len(conceptType)):
			dbCursor.execute("""
				SELECT terms.term FROM terms
				INNER JOIN terms_conceptType on terms_conceptType.terms_key = terms.key
				WHERE partOfSpeech = "VERB" AND conceptType = ?
				""", (conceptType[i],))
			queryResults = pull_query_results()
			append_to_possVerbs(queryResults) # append results to possVerbs
	# if only a subject was provided
	elif (conceptType == None and isinstance(subject,str)):
		# find the verbs that match the subject
		subjectCateg = find_categories(subject)
		for i in range(len(subjectCateg)):
			dbCursor.execute("""
				SELECT term FROM terms
				WHERE partOfSpeech = 'VERB' AND term = ?;
				""", (subjectCateg[i],))
			queryResults = pull_query_results()
			append_to_possVerbs(queryResults) # append results to possVerbs
	# if both conceptType and subject were provided
	elif (isinstance(conceptType,list) and isinstance(subject,str)):
		#constrain found set by both
		subjectCateg = find_categories(subject)
		for h in range(len(subjectCateg)):
			for i in range(len(conceptType)):
				# print(conceptType[i],"?")
				dbCursor.execute("""
					SELECT terms.term FROM terms
					INNER JOIN terms_conceptType on terms_conceptType.terms_key = terms.key
					WHERE partOfSpeech = "VERB" AND terms.term = ? AND conceptType = ?;
					""", (subjectCateg[h],conceptType[i],))
				queryResults = pull_query_results()
				append_to_possVerbs(queryResults) # append results to possVerbs
	# if no arguments were provided, search for ALL verbs
	elif (conceptType == None and subject == None):
		dbCursor.execute("""
			SELECT term FROM terms
			WHERE partOfSpeech = 'VERB';
			""")
		queryResults = pull_query_results()
		append_to_possVerbs(queryResults) # append results to possVerbs
	else: # if none of the above options for the arguments
		print("\t\t\tA bad argument was passed to find_verbs(). Did not search for verbs. Returned None.")
		print("\t\t\t"+str(conceptType)+", "+str(subject))
		return None
	if possVerbs:
		return possVerbs
	else:
		return None
# TODO: priority communications, e.g. traditional Responses, executing/answering Imperatives, answering Questions, etc.
	
#{}{}{}{}{}{}{}{}{}{}{}{}{}{}@@@  Complex writing functions
def evaluate_statement_truth(statement):
	"""Evaluate whether a statement is true. Attempt to apply evaluation criteria in the following order:
		1. def_comprehensive
		2. def_deduced
		3. definingCateg
		4. otherCateg
	----------Dependencies:
	learned_data.db and maybe others.
	----------Parameters:
	statement = a list of lists each containing Term-POS pairs.
	----------Return:
	A boolean. Or, if the statment can't be evaluated, None.
	"""
	return True # TODO: complete this function.
def freewrite_declarative(**kwargs): # start with kws and fill in blanks. save possibles.
	"""Tries to write a sentence with the words passed in. Recursive, but not infinitely recursive.
	----------Arguments:
		Can take the following kwargs, all of which are optional:
			miscList = a list of strings to try and make a sentence out of			
			conceptType = a string. see the table 'terms_conceptType' for suggested values.
			posTemplates = a list of lists of strings. Can be obtained using find_possible_templates().
			st = a boolean. stands for searchTree. Tells the function whether to cascade down category lists while trying to write a sentence (e.g. from duck to bird to vertebrate).
			n = an integer. the number of times this function has called itself. this should never be entered manually; it's automatic.
			
			subject = a string
			verb = a string
			... and hopefully more parts of speech at some point. If I add more kwargs, I will also need to update the "indvKwargs" and "recursive" sections. 
	
	----------Dependencies:
		determine_pos()
		find_possible_templates()
		order_by_pos()
		remove_duplicates()
		find_categories(), which is located in learned_data/util_findCategories.py
		is_category_instance(), which is located in learned_data/util_is_category_instance.py
		and any of the following, depending on which kwargs were passed in...
			find_object()
			find_verbs()
			... etc.
	
	----------Return:
	A list of lists of lists of strings. i.e.: 
		list = [sentence, sentence, ..., n]
			sentence = [termGroup, termGroup, ..., n]
				termGroup = ['term', 'POS']
	Or None, if nothing could be constructed.
	"""
	
	# pull in the kwargs. assign empty string kwargs = None.
	conceptType = kwargs["conceptType"] if ("conceptType" in kwargs) else None
	miscList = kwargs["miscList"] if ("miscList" in kwargs) else []
	n = kwargs["n"] if ("n" in kwargs) else 0
	posTemplates = kwargs["posTemplates"] if ("posTemplates" in kwargs) else None
	st = kwargs["st"] if ("st" in kwargs) else False #might change default to True. not sure yet.
	subject = kwargs["subject"] if ("subject" in kwargs) else None
	verb = kwargs["verb"] if ("verb" in kwargs) else None

	possSc = []
	# print("~~~~~New Rec.  n =",str(n)) #for debugging only

	############## RECURSIVE STUFF - expanding miscList ##############
	if n == 0: 
		print("\tfreewrite_declarative()") #for debugging only
		# handle bad arguments.
		if isinstance(miscList,str):
			miscList = [miscList]
		# TODO: make all arguments lowercase

		# TODO: infinitize all arguments

		#regardless of whether miscList has any content, append each POS kwarg to miscList. Note: POS kwargs can be ignored whenever we're not in the outer-most scope.
		indvKwargs = [subject,verb]
		for i in range(len(indvKwargs)):
			if indvKwargs[i] != None:
				miscList.append(indvKwargs[i])
		# continue on to the non-recursive stuff.
	
	if n == 1: # if in first recursion:
		#if a subject or conceptType was provided, add all matching verbs.
		if subject != None or conceptType != None:
			addMe = find_verbs(conceptType,subject)
			addMeWithPOS = []
			if addMe and isinstance(addMe,list):
				addMeWithPOS = determine_pos(addMe) # add a POS for each word
				if addMeWithPOS:
					for i in range(len(addMeWithPOS)):
						miscList.append(addMeWithPOS[i])
		#add all the categories of each term
		if miscList and isinstance(miscList,list):
			for i in range(0,len(miscList)):
				addMe = find_categories(miscList[i][0])
				addMeWithPOS = []
				if addMe and isinstance(addMe,list):
					addMeWithPOS = determine_pos(addMe) #Add a POS for each word
					if addMeWithPOS:
						for h in range(len(addMeWithPOS)):
							miscList.append(addMeWithPOS[h])
		# continue on to the non-recursive stuff.

	if n == 2: # if in second recursion:
		# for every noun in miscList, add every verb/conceptType. no searchTree.
		verbsToAdd = []
		for i in range(len(miscList)):
			currTG = miscList[i]
			if currTG[1] == "NOUN":
				addMe = find_verbs(conceptType,currTG[0])
				if addMe and isinstance(addMe,list):
					for j in range(len(addMe)):
						verbsToAdd.append(addMe[j])
		if verbsToAdd:
			for i in range(len(verbsToAdd)):
				addMeWithPOS = []
				currTerm = verbsToAdd[i]
				currPOS = determine_pos(currTerm) #Add a POS for each word
				if currPOS: # note: currPOS is a string, not a list.
					addMeWithPOS = [currTerm,currPOS]
					miscList.append(addMeWithPOS)
		pass # TODO: for every verb, in miscList, run find_object(). (find_object() doesn't test for most common objects...)
		# continue on to the non-recursive stuff.

	if n == 3: # if in third recursion:
		# print("\t\tfreewrite_declarative() is expanding miscList a lot") #for debugging only
		pass # TODO: for each term in miscList, use word vectors/free association to add related terms (both nouns and verbs)
		# continue on to the non-recursive stuff.

	if n >= 4:
		return None # give up.

	############## NON-RECURSIVE STUFF - constructing sentences ##############	
	####### Construct word arrangements
	# if miscList contains any content...
	if miscList and isinstance(miscList,list):
		if n == 0:
			miscList = determine_pos(miscList) # add a POS for each word in miscList
		# if no posTemplates...
		if posTemplates == None:
			# pull ALL posTemplates
			reqTemplates = find_possible_templates()
			# retrieve grammatical arrangements of the words
			results = order_by_pos(reqTemplates,miscList) 
			# save the results
			if results and isinstance(results,list):
				for i in range(0,len(results)):
					possSc.append(results[i])
		# if posTemplates...
		elif isinstance(posTemplates,list):
			if posTemplates:
				#retrieve grammatical arrangements of the words. 
				results = order_by_pos(posTemplates,miscList)
				#save the results
				if results and isinstance(results,list):
					for j in range(0,len(results)):
						possSc.append(results[j])
		possSc = remove_duplicates(possSc) # eliminate any duplicate sentences
	####### Filter by any requested specifications
	if possSc:
		if isinstance(conceptType,str): # ...filter by conceptType.
			# keep only the possible sentences with the requested conceptType.
			filteredSc = []
			for i in range(len(possSc)): # for each sentence:
				for j in range(len(possSc[i])): # for each word:
					dbCursor.execute("""
						SELECT conceptType FROM terms_conceptType WHERE term = ?;
						""", (possSc[i][j][0],))
					localCT = pull_query_results()
					if isinstance(localCT,list): # fail gracefully
						for k in range(len(localCT)):
							# if the db conceptType == the requested one, append the term.
							if localCT[k] == conceptType: 
								filteredSc.append(possSc[i])
								break # no need to test the rest of the sentence
							else:
								pass
			possSc = []
			possSc = filteredSc
	
		if isinstance(subject,str): # ...filter by subject.
			# keep only the possible sentences with the requested subject.
			filteredSc = []
			for i in range(len(possSc)): # for each sentence:
				for j in range(0,1): # keep it iff first or second word==subject.
					if possSc[i][j][0] == subject:
						filteredSc.append(possSc[i])
						break # no need to test the rest of the sentence
					else:
						print("\t not appended")
			possSc = []
			possSc = filteredSc
		
		if isinstance(verb,str): # ...filter by verb.
			print("\t\tfreewrite_declarative() couldn't filter possSc by a verb because that's too complex of a task. No filtering took place.")
	else:
		pass # print("\t\t\tfreewrite_declarative() tried to filter possSc, but it already empty...")

	####### Filter by truth and relevance
	# TODO: test each possSc for truth
	# scToEval = [] #sentences to evaluate #later

	# TODO: Determine which sentences are most relevant
	# -relevance to current conversation (maybe word vector distances)
	# -how many recursions were needed (0-1 by 0.2s)
	# -what are the chances that the user already knows the info (0-1)
	# -provide info about tone
	# research more tests/weights
	# use ML to weight the coefficients of each test, then hard code those coefficients (for now)
	
	# return results if there are any.
	if possSc:
		return possSc
	else:
		# start the next recursion.
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


#{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
#{}
#{}	@@		Main Loop
#{}
#{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
#This section exists simply for testing. The finalized file will call functions in a different way.

if test_mode:
	# clean_up_temp_files()
	availableSc = freewrite_declarative(miscList=["penguin"])
	print("\n---available sentences:")
	every_other_word(availableSc,True) # prints the results straight from every_other_word()
else: # The normal main loop
	cogmod_simple = True
	while cogmod_simple:
		inputParsed = False
		print("""
	\nAVAILABLE COMMANDS: 
		'abort' (exit without reflecting)
		'read' (e.g. read https://en.wikipedia.org/wiki/Carpinus_betulus)
		'read this from source: paragraph' (e.g. read this from wikipedia: A folksinger or folk singer is a person who sings folk music.)
		'exit'
		""")
		cogmod_simple_input = input('--> ')
		#exit without closeOut
		if cogmod_simple_input == 'abort':
			inputParsed = True
			cogmod_simple = False
		#if cogmod_simple_input starts with read
		if cogmod_simple_input[:5] == 'read ':
			readingSuccess = False
			inputParsed = True
			read(cogmod_simple_input)
		if cogmod_simple_input[:6] == 'match ':
			inputParsed = True
			print(cogmod_simple_input[6:])
			matchTopic(cogmod_simple_input[6:])
		#exit the main loop
		if cogmod_simple_input == 'exit':
			inputParsed = True
			"Exiting..."
			clean_up_temp_files()
			reflect_on_known_data()
			cogmod_simple = False
		#handle syntax errors
		if inputParsed == False:
			print("I don't understand '%s'." % cogmod_simple_input)

print("\n===== Script Ended =====")
