#import dependencies
import os.path, sqlite3
absolute_filepath = os.path.dirname(__file__)
dbConn = sqlite3.connect(absolute_filepath+'/learned_data.db')
dbCursor = dbConn.cursor()
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

#the actual function to call
def findCategories (inputTerm,defTraitsOnly=False):
	"""Returns a list containing all of the known categories, into which the input term fits.
	----------Dependencies:
	learned_data.py, which is in the folder learned_data

	----------Parameters:
	inputTerm = a string. the term to search for, such as 'penguin'
	defTraitsOnly = a boolean. If True, only search for the categories that 'define' the object (aka terms_definingCateg).

	----------Returns:
	a list of strings. 
	if nothing was found, returns [].
	"""

	def instance_catTree(inputTerm,inputTermSearchesPerformed=0,defTraitsOnly=False):
		"""An infinitely recursive function. Appends the appropriate categories to the variable allCats (which is decalred outside of this function.)
		This function gets called only by findCategories(). It should not be called directly.
		
		----------Dependencies:
		learned_data.py, which is in the folder learned_data

		----------Parameters:
		inputTerm = a string, such as 'guitar'
		inputTermSearchesPerformed = an autmoatically-generated integer, to track how many layers of this function have been called. Terminates the search after 21 layers, to halt infinite loops.
		defTraitsOnly = a boolean. If True, only search for the categories which define the object (terms_definingCateg table), and not for others (terms_otherCateg table). Optional.

		----------Returns:
		True. 
		Also, appends strings to allCats, but doesn't return that.
		"""
		visualizeTabs='' #to help with visualizing layers, for debugging.

		#break out of infinite loops
		inputTermSearchesPerformed += 1
		if inputTermSearchesPerformed >= 20:
			print("%sinputTermSearchesPerformed=%s:   inputTerm=%s" % (visualizeTabs,inputTermSearchesPerformed,inputTerm))
			print ("\nWhile searching for term categories, instance_catTree() detected a possible infinite loop. 21 iterations were reached, so the search was terminated.\n")
			return True
		
		# #visualizations (for debugging)
		# for i in range (0,inputTermSearchesPerformed):
		# 	visualizeTabs += '  '
		# print("%s%s:   inputTerm=%s" % (visualizeTabs,inputTermSearchesPerformed,inputTerm))

		#find the key of the inputTerm
		dbCursor.execute("""SELECT key FROM terms WHERE term = ?;""", (inputTerm,)) #homonyms will break this #incomplete
		inputTermKey = pullQueryResults()

		if isinstance(inputTermKey,list) and len(inputTermKey)>0: #fail gracefully
			inputTermKey = inputTermKey[0]

			#loop through defining categories (recursive)
			dbCursor.execute("""SELECT definingCateg FROM terms_definingCateg WHERE terms_key = ?;""", (inputTermKey,))
			iDefCats = pullQueryResults()
			if isinstance(iDefCats,list) and len(iDefCats)>0: #fail gracefully
				for j in range(0,len(iDefCats)):
					# print("%s (j=%s)" % (visualizeTabs,j))
					# print(visualizeTabs+" inputTerm is:",iDefCats[j])
					allCats.append(iDefCats[j])

					dbCursor.execute("""SELECT definingCateg FROM terms_definingCateg WHERE term = ?;""", (iDefCats[j],))
					moreIDC = pullQueryResults()
					if isinstance(moreIDC,list) and len(moreIDC)>0: #elif that term is a category of its own, call self again.
						instance_catTree(iDefCats[j],inputTermSearchesPerformed,defTraitsOnly)
					else: #elif that term is NOT a category of its own
						pass
		
			#loop through the other categories (recursive) (optional)
			if defTraitsOnly == False: #if user requested ALL relevant categories, not just defining ones.
				dbCursor.execute("""SELECT otherCateg FROM terms_otherCateg WHERE terms_key = ?;""", (inputTermKey,))
				iOthCats = pullQueryResults()
				if isinstance(iOthCats,list) and len(iOthCats)>0: #fail gracefully
					for j in range(0,len(iOthCats)):
						# print("%s (j=%s)" % (visualizeTabs,j))
						# print(visualizeTabs+" inputTerm is:",iOthCats[j])
						allCats.append(iOthCats[j])

						dbCursor.execute("""SELECT otherCateg FROM terms_otherCateg WHERE term = ?;""", (iOthCats[j],))
						moreIDC = pullQueryResults()
						if isinstance(moreIDC,list) and len(moreIDC)>0: #elif that term is a category of its own, call self again.
							instance_catTree(iOthCats[j],inputTermSearchesPerformed,defTraitsOnly)
						else: #elif that term is NOT a category of its own
							pass

		return True #when finished, cascade back up to the most recent call
		### end of instance_catTree()


	# print ("running findCategories()")
	allCats = []
	inputTermSearchesPerformed = 0 # to detect infinite loops
	visualizeTabs = ''

	#verify that the 'inputTerm' is known
	if type(inputTerm) == str: 
		#get the key of inputTerm
		# print("1:   "+inputTerm) #for vizualization
		dbCursor.execute("""SELECT key FROM terms WHERE term = ?;""", (inputTerm,)) #homonyms will break this #incomplete
		termKey = pullQueryResults()
		if isinstance(termKey,list) and len(termKey)>0: #fail gracefully
			termKey = termKey[0]
			# print("termKey=",str(termKey))
		else:
			print ("\t\t\tfindCategories() couldn't find '%s' in the database. Therefore, no categories were found." % inputTerm)
			return []
	else:
		#give up
		print("findCategories() in util_findCategories.py was passed a non-string argument: %s. Returned []." % str(inputTerm))
		return []

	#search starting within defining categories (but optionally include the other categories).
	dbCursor.execute("""SELECT definingCateg FROM terms_definingCateg WHERE terms_key = ?;""", (termKey,))
	defCats = pullQueryResults()
	if isinstance(defCats,list) and len(defCats)>0: #fail gracefully
		for i in range(0,len(defCats)):
			inputTermSearchesPerformed += 1
			# print(str(inputTermSearchesPerformed)+":",defCats[i])
			allCats.append(defCats[i])

			dbCursor.execute("""SELECT definingCateg FROM terms_definingCateg WHERE term = ?;""", (defCats[i],)) 
			moreDC = pullQueryResults()
			if isinstance(moreDC,list) and len(moreDC)>0: #elif the found term is a category of its own
				instance_catTree(defCats[i],inputTermSearchesPerformed,defTraitsOnly)

	#search starting within the other categories (optional)
	if defTraitsOnly == False:
		dbCursor.execute("""SELECT otherCateg FROM terms_otherCateg WHERE terms_key = ?;""", (termKey,))
		othCats = pullQueryResults()

		if isinstance(othCats,list) and len(othCats)>0: #fail gracefully
			for i in range(0,len(othCats)):
				inputTermSearchesPerformed += 1
				# print(str(inputTermSearchesPerformed)+":",othCats[i])
				allCats.append(othCats[i])

				dbCursor.execute("""SELECT otherCateg FROM terms_otherCateg WHERE term = ?;""", (othCats[i],))
				moreOC = pullQueryResults()
				if isinstance(moreOC,list) and len(moreOC)>0: #elif the found term is a category of its own
					instance_catTree(othCats[i],inputTermSearchesPerformed,defTraitsOnly)
				#go to the next category in the list

	return allCats