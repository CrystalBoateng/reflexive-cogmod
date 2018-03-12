#{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
#{}
#{}	@@		Load dependencies and global variables
#{}
#{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}

#load NLP dependencies
import textacy #to create docs/doc metadata, and to lemmatize and tokenize unstructured text
import os #to read and write from disk
import sys #to delete and reload python files
import re #to parse html
import json #to read doc metadata
import uuid #to generate unique IDs for topics
from operator import itemgetter #to sort lists of lists

#declare global variables
absolute_filepath = os.path.dirname(__file__) #the absolute filepath of this script.
knowledgePriorityLevel = 1
mySubject = myDO = myIO = myContext = "", #for reading and writing. DO/IO means Direct Object/Indirect Object
from nlp_resources.compromise_conjugations_mod import * #import variable compromiseConjugations, to help parse conjugated verbs


#{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
#{}
#{}	@@		General utilities
#{}
#{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
def generateUuid():
	"""Generate a reasonably unique ID string based on date and time.
	----------Dependencies:
	import uuid

	----------Parameters:
	None

	----------Returns:
	a string (e.g. '2017-11-26_9-13_85894b2f')
	"""
	from datetime import datetime
	dateAndTime = datetime.now()
	randomId = str(uuid.uuid4()) #generate a UUID
	randomId = randomId[:8] #truncate it because 36 digits is too long
	myUuid = "%s-%s-%s_%s-%s_%s" % (
		str(dateAndTime.year),
		str(dateAndTime.month),
		str(dateAndTime.day),
		str(dateAndTime.hour),
		str(dateAndTime.minute),
		randomId
		)
	print("Generated UUID: ",myUuid)
	return myUuid
def pushToDisk(cachedVar): #incomplete
	pass 
	#this pull everything before "#BEGIN CONTENT (do not edit or delete this line)." and save it to a string.#then it will concatenate the current cached version of 'knownTerms' or 'knownCorpus'.
	#then it will save all that to the disk.
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
def refreshKnownTerms(): #incomplete
	"""Update the global variable 'knownTerms', from the file known_terms.py.
	----------Dependencies:
	import os, import sys
	known_terms.py (in this script's directory)

	----------Parameters:
	None

	----------Returns:
	None (content is pushed straight to the global variable named knownTerms)
	"""
	print ("\texecuting known_terms.py to refresh knownTerms.")
	
	#exec 'For each line of text, concat to string.' then exec 'exec of that string'.
	exec("stringOfKnownTerms = '' \nwith open ('known_terms.py', 'rt', encoding='utf8') as f:\n\tfor line in f:\n\t\tstringOfKnownTerms+=line\nexec(stringOfKnownTerms)")
	
	# #update knownTerms_verbs using the updated knownTerms
	# print ("\tupdating knownTerms_verbs...")
	# global knownTerms_verbs
	# knownTerms_verbs = ['example verb'] # not yet written.
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
	#     f.write('\n'+docName)
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
#{}	@@		Writing
#{}
#{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}

#{}{}{}{}{}{}{}{}{}{}{}{}{}{}@@@  Known Meanings
#The core knownMeanings of some (but not all) knownTerms. The terms themeselves are stored in known_terms.py.

#update real-time variables so that the Meanings can look up known terms/topics
refreshKnownCorpus()
refreshKnownTerms()

#   General Utilities for knownMeanings
def isCategoryInstance (instance,finalCategory,defTraitsOnly=False):
	"""Returns True if the 'instance' fits in the category 'finalCategory'. Else, returns false.
	----------Dependencies:
	known_terms.py (in this script's directory)
	findIndexOfString()

	----------Parameters:
	instance = a string, such as 'guitar'
	finalCategory = a string, such as 'musical instrument'
	defTraitsOnly = only search for the categories that define the object. To do this, please use the function isDefiningCategory() instead.

	----------Returns:
	a boolean.
	"""

	def instance_searchTree(instance,finalCategory,instanceSearchesPerformed=0,visualizeTabs='',defTraitsOnly=False):
		"""A recursive function. Returns True if the 'instance' fits in the category 'finalCategory'. Else, returns false.
		This function gets called only by isCategoryInstance(). It should not be called directly.
		----------Dependencies:
		known_terms.py (in this script's directory)
		findIndexOfString()

		----------Parameters:
		instance = a string, such as 'guitar'
		finalCategory = a string, such as 'musical instrument'
		instanceSearchesPerformed = an autmoatically-generated integer, to track how many layers of this function have been called. Terminates the search after 21 layers, to halt infinite loops.
		visualizeTabs = a string conatining three spaces, to help with visualizing layers, during debugging.
		defTraitsOnly (optional boolean) = only search for the categories that define the object (knownTerms[2]), and not the others (knownTerms[3]).

		----------Returns:
		a boolean.
		"""

		#break out of infinite loops
		instanceSearchesPerformed += 1
		if instanceSearchesPerformed >= 20:
			print("%sinstanceSearchesPerformed=%s:   instance=%s   finalCategory=%s" % (visualizeTabs,instanceSearchesPerformed,instance,finalCategory))
			print ("\nWhile searching for instances of a category, a possible infinite loop was detected. 21 iterations were reached, so the search was terminated.\n")
			return False
		
		for i in range (0,instanceSearchesPerformed):
			visualizeTabs += '  '
		# print("%s%s:   instance=%s   finalCategory=%s" % (visualizeTabs,instanceSearchesPerformed,instance,finalCategory))

		#find the 'instance' string within knownTerms
		instanceIndex = findIndexOfString(instance,knownTerms,0)
		assert type(knownTerms[instanceIndex]) == list, "The object you're searching in, isn't a list. It's mostly likely a string, so if you search for an index within it, you'll only find one character."

		#loop through defining categories (recursive)
		for j in range(0,len(knownTerms[instanceIndex][2])):
			# print("%s (j=%s)" % (visualizeTabs,j))
			# print(visualizeTabs+" instance is:",knownTerms[instanceIndex][2][j])
			if knownTerms[instanceIndex][2][j] == finalCategory: #if the finalCategory matches
				# print("***MATCH!***")
				return True
			elif type(findIndexOfString(knownTerms[instanceIndex][2][j],knownTerms,0)) == int: #elif the category is a category of its own
				if instance_searchTree(knownTerms[instanceIndex][2][j],finalCategory,instanceSearchesPerformed,visualizeTabs,defTraitsOnly) == True:
					# print("***MATCH!***")
					return True
			else:
				pass #go to the next finalCategory in the list

		#loop through the other categories (recursive) (optional)
		if defTraitsOnly == False: #if user requested ALL relevant categories, not just defining ones.
			for k in range(0,len(knownTerms[instanceIndex][3])):
				# print("%s (k=%s)" % (visualizeTabs,k))
				# print(visualizeTabs+" instance is:",knownTerms[instanceIndex][3][k])
				if knownTerms[instanceIndex][3][k] == finalCategory: #if the finalCategory matches
					# print("***MATCH!***")
					return True
				elif type(findIndexOfString(knownTerms[instanceIndex][3][k],knownTerms,0)) == int: #elif the category is a category of its own
					if instance_searchTree(knownTerms[instanceIndex][3][k],finalCategory,instanceSearchesPerformed,visualizeTabs,defTraitsOnly) == True:
						# print("***MATCH!***")
						return True
				else:
					pass #go to the next finalCategory in the list

		return False # if no match was found at any point in this iteration of this function, return false

	### end of instance_searchTree()

	# print("instance,finalCategory:",instance,finalCategory)
	instanceSearchesPerformed = 0 # to detect infinite loops
	visualizeTabs = ''

	#verify that 'instance' is known
	stringIndex = findIndexOfString(instance,knownTerms,0)
	if knownTerms[stringIndex][0] == instance:
		instance = knownTerms[stringIndex]
	else:
		return "I don't know what '%s' is." % instance


	#search starting within defining categories (but optionally including the other categories).
	for i in range(0,len(instance[2])):
		instanceSearchesPerformed += 1
		# print(str(instanceSearchesPerformed)+":",instance[2][i])
		if instance[2][i] == finalCategory: #if the finalCategory matches
			# print("***MATCH!***")
			return True
		elif type(findIndexOfString(instance[2][i],knownTerms,0)) == int: #elif the finalCategory is a finalCategory of its own
			if defTraitsOnly == True: #search within defining categories only
				if instance_searchTree(instance[2][i],finalCategory,instanceSearchesPerformed,'',True) == True:
					# print("***MATCH!***")
					return True
			elif defTraitsOnly == False: #search within all relevant categories
				if instance_searchTree(instance[2][i],finalCategory,instanceSearchesPerformed,'') == True:
					# print("***MATCH!***")
					return True
		else:
			pass #go to the next finalCategory in the list


	#search starting within the other categories (optional)
	if defTraitsOnly == True:
		for k in range(0,len(instance[3])):
			instanceSearchesPerformed += 1
			# print(str(instanceSearchesPerformed)+":",instance[3][i])
			if instance[3][k] == finalCategory: #if the finalCategory matches
				# print("***MATCH!***")
				return True
			elif type(findIndexOfString(instance[3][k],knownTerms,0)) == int: #elif the finalCategory is a finalCategory of its own
				if instance_searchTree(instance[3][k],finalCategory,instanceSearchesPerformed,'') == True:
					# print("***MATCH!***")
					return True
			else:
				pass #go to the next finalCategory in the list

	#somehwere in/above here, add a place to store and check for negations!!! exceptions can be up to 49% of a category. example: penguins are birds but they cannot fly.


	return False
def isDefiningCategory (instance,finalCategory):
	"""Returns True if 'finalCategory' is one of the defining traits of 'instance'. Else, returns false.
	----------Dependencies:
	isCategoryInstance()
		known_terms.py (in this script's directory)
		findIndexOfString()

	----------Parameters:
	instance = a string, such as 'guitar'
	finalCategory = a string, such as 'musical instrument'

	----------Returns:
	a boolean.
	"""

	output = isCategoryInstance(instance,finalCategory,True)
	return output

#   Definitions of knownMeanings (storage)               NOTES:
    # -None of these terms should be nouns; nouns are defined by only their "defining categories," which are stored in known_terms.py.
    # -All of these functions are overloaded: 
	    # whenever context == "evaluate", the function will evaluate the accuracy of the term with respect to the arguments passed into the function
	    # whenever context == "learn", the function will attempt to integrate the input information, into known_terms.py; 
	    # whenever context == "perform", the function will attempt to perform the verb/become the adjective/perform the adverb/etc; 
def meaning_include(myCategory,myWord,indirectObject,context):
	"""Defines the core meaning of the term "include". 
	----------Dependencies:
	isDefiningCategory()

	----------Parameters:
	myCategory = a string
	myWord = a string
	indirectObject = a string

	----------Returns:
	a boolean (True if term evaluates to True, or if term is learned/performed successfuly. Else, False.)
	"""
	indirectObject = "havent written this yet" #I haven't yet gotten around to indirect objects in any of these definitions yet #incomplete

	#Handle errors non-fatally
	for i in range (0, len(meaning_include)):
		if isinstance (meaning_include[i], str):
			pass
		else:
			print( "Error - a value was passed to meaning_include() which was not a string. The function reutrned None, rather than a Boolean.")
			return None


	# if context is 'evaluate':
	if isDefiningCategory(myWord,myCategory) == True:
		print("Evaluating...  The category %s includes %s." % (myCategory,myWord)) 
		return True
	else:
		print("Evaluating...  The category %s does not include %s." % (myCategory,myWord)) 
		return False

	# if context is 'learn':
	#    check if the myCategory already exists as an entry in knownTerms. if so, pass. else, create it. 
	#    append myWord to its index 3.
	#    When done reading the whole user input... (i.e., not in this function)
	#        pushToDisk(knownTerms)
	#        refreshKnownTerms()

	# if context is 'perform':
	if context == "perform":
		if indirectObject == None:
			print ("I was instructed to 'include' something within myself. However, I cannot modify my own code.") #incomplete
			return False
		else:
			print ("I was instructed to 'include' something within something else. However, I don't know how to do that.") #incomplete
			return False
def meaning_define(subject,directObject,context):
	"""Defines the core meaning of the term "define". 
	----------Dependencies:
	findIndexOfString()

	----------Parameters:
	subject = a string
	directObject = a string
	indirectObject = a string

	----------Returns:
	if perform: a string (e.g. "Penguin is characterized by aquatic and not flying.")
	else: a boolean (True if term evaluates to True, or if term is learned successfuly. Else, False.)
	"""

	# if context is 'perform':
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

	# if context is 'learn'
	#    check if the directObject already exists as an entry in knownTerms. if so, pass. else, create it. 
	#    append subject to its index 2.
	#    When done reading the whole user input... (i.e., not in this function)
	#        pushToDisk(knownTerms)
	#        refreshKnownTerms()

	# if context is 'evaluate':
	if isDefiningCategory(directObject,subject) == True:
		return True
	else: # Note: even if the answer is unknown, this returns false.
		return False 

#   Handler for knownMeanings 
    # This determines which definitions to call. If all of the called functions return True, then the term is applicable. Unfortunately this list can't be stored in a separate file, or else it can't access knownTerms.
knownMeanings = [ 
	#[term, POS, [a test that evaluates to a boolean (if context=="evaluate"). if all the booleans are True, then the meaning is applicable within a given context.], ],
	["include", "VERB", [meaning_include], ],
	["define", "VERB", [meaning_define], ],
	#other non-physical terms to learn: find, difficult, know, know of, write, read
]


#{}{}{}{}{}{}{}{}{}{}{}{}{}{}@@@  Validating Grammar
	# #    idk if i'll end up using this. if I do, I'll probably save it in an external .py file in the folder /nlp_resources
	# grammaticalConstructions = [
	# 	['NOUN','VERB'],
	# 	['NOUN','VERB','NOUN'],
	# 	# etc.
	# ]
	# def checkGrammar (potentialSentence):
	# 	#return true if the POS order in potentialSentence is acceptable, as compared to a POS order in grammaticalConstructions
	# 	pass #incomplete



#{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
#{}
#{}	@@		Remembering, Recalling, Reflecting
#{}
#{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
# 
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
		pass
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
def deleteSimpleDuplicates(): #incomplete
	#An overloaded function. takes the optional argument 'knownCorpus'. Otherwise, operates on 'knownTerms'.
	#delete duplicate entries and categories from knownTerms (or knownCorpus). pushToDisk() when done.
	pass
def deduceTerms(): #incomplete
	#expand knownTerms by creating new netries from any duplicate categories
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



#{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
#{}
#{}	@@		Main Loop
#{}
#{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
#This loop exists simply for testing purposes. The finalized file will call functions in a different way.
cogmod_simple = True

while cogmod_simple == True:
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
		print ("\tinitiating shutdown sequence.")
		reflectOnKnownData()
		cogmod_simple = False
	#handle syntax errors
	if inputParsed == False:
		print ("I don't understand '%s'." % cogmod_simple_input)
print("\n===== Script Ended =====")