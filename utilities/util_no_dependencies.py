# globally-useful utilities which have no dependencies on external files
from datetime import datetime
import uuid
import itertools
from operator import itemgetter
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