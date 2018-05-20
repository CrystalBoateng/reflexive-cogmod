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

#extended recursions
def instance_searchTree(instance,finalCategory,instanceSearchesPerformed,defTraitsOnly=False):
	"""An infinitely recursive function. Returns True if the 'instance' fits in the category 'finalCategory'. Else, returns false.
	This function gets called only by isCategoryInstance(). It should not be called directly.
	
	----------Dependencies:
	learned_data.py, which is in the folder learned_data

	----------Parameters:
	instance = a string, such as 'guitar'
	finalCategory = a string, such as 'musical instrument'
	instanceSearchesPerformed = an autmoatically-generated integer, to track how many layers of this function have been called. Terminates the search after 21 layers, to halt infinite loops.
	defTraitsOnly = a boolean. If True, only search for the categories that define the object (terms_definingCateg table), and not for others (terms_otherCateg table). Optional.

	----------Returns:
	a boolean.
	"""
	visualizeTabs='' #to help with visualizing layers, for debugging.

	#break out of infinite loops
	instanceSearchesPerformed += 1
	if instanceSearchesPerformed >= 20:
		print("%sinstanceSearchesPerformed=%s:   instance=%s   finalCategory=%s" % (visualizeTabs,instanceSearchesPerformed,instance,finalCategory))
		print ("\nWhile searching for instances of a category, a possible infinite loop was detected. 21 iterations were reached, so the search was terminated.\n")
		return False
	
	#visualizations (for debugging)
	# for i in range (0,instanceSearchesPerformed):
	# 	visualizeTabs += '  '
	# print("%s%s:   instance=%s   finalCategory=%s" % (visualizeTabs,instanceSearchesPerformed,instance,finalCategory))

	#find the key of the 'instance' term
	dbCursor.execute("""SELECT key FROM terms WHERE term = ?;""", (instance,)) #homonyms will break this #incomplete
	instanceKey = pullQueryResults()
	# print("instanceKey=",str(instanceKey))

	if isinstance(instanceKey,list) and len(instanceKey)>0: #fail gracefully
		instanceKey = instanceKey[0]

		#loop through defining categories (recursive)
		dbCursor.execute("""SELECT definingCateg FROM terms_definingCateg WHERE terms_key = ?;""", (instanceKey,))
		iDefCats = pullQueryResults()
		if isinstance(iDefCats,list) and len(iDefCats)>0: #fail gracefully
			for j in range(0,len(iDefCats)):
				# print("%s (j=%s)" % (visualizeTabs,j))
				# print(visualizeTabs+" instance is:",iDefCats[j])
				if iDefCats[j] == finalCategory: #if the finalCategory matches
					# print("***MATCH!***")
					return True
				else:
					dbCursor.execute("""SELECT definingCateg FROM terms_definingCateg WHERE term = ?;""", (iDefCats[j],))
					moreIDC = pullQueryResults()
					if isinstance(moreIDC,list) and len(moreIDC)>0: #elif the category is a category of its own
						if instance_searchTree(iDefCats[j],finalCategory,instanceSearchesPerformed,defTraitsOnly) == True:
							# print("***MATCH!***")
							return True
					else: #elif the found term is NOT a finalCategory of its own
						pass #go to the next finalCategory in the list
	
			#loop through the other categories (recursive) (optional)
			if defTraitsOnly == False: #if user requested ALL relevant categories, not just defining ones.
				dbCursor.execute("""SELECT otherCateg FROM terms_otherCateg WHERE terms_key = ?;""", (instanceKey,))
				iOthCats = pullQueryResults()
				if isinstance(iOthCats,list) and len(iOthCats)>0: #fail gacefully
					for j in range(0,len(iOthCats)):
						# print("%s (j=%s)" % (visualizeTabs,j))
						# print(visualizeTabs+" instance is:",iOthCats[j])
						if iOthCats[j] == finalCategory: #if the finalCategory matches
							# print("***MATCH!***")
							return True
						else:
							dbCursor.execute("""SELECT otherCateg FROM terms_otherCateg WHERE term = ?;""", (iOthCats[j],))
							moreIOC = pullQueryResults()
							if isinstance(moreIOC,list) and len(moreIOC)>0: #elif the category is a category of its own
								if instance_searchTree(iOthCats[j],finalCategory,instanceSearchesPerformed,defTraitsOnly) == True:
									# print("***MATCH!***")
									return True
							else: #elif the found term is NOT a finalCategory of its own
								pass #go to the next finalCategory in the list
	
			return False # if no match was found at any point in this iteration of this function, return false

#the main function to call
def isCategoryInstance (instance,finalCategory,defTraitsOnly=False):
	"""Returns True if the 'instance' fits in the category 'finalCategory'. Else, returns false.
	----------Dependencies:
	learned_data.py, which is in the folder learned_data

	----------Parameters:
	instance = a string, such as 'guitar'
	finalCategory = a string, such as 'musical instrument'
	defTraitsOnly = only search for the categories that define the object. To do this, please use the function isDefiningCategory() instead.

	----------Returns:
	a boolean.
	"""
	# print ("running isCategoryInstance()")
	# print("instance,finalCategory:",instance,finalCategory)
	visualizeTabs = ''

	#verify that the 'instance' is known
	dbCursor.execute("""SELECT key FROM terms WHERE term = ?;""", (instance,)) #homonyms will break this #incomplete
	termKey = pullQueryResults()
	if isinstance(termKey,list) and len(termKey)>0:
		termKey = termKey[0]
	else:
		print ("\t\t\tisCategoryInstance() can't find '%s' in the database. Returned None." % instance)
		return None


	#search starting within defining categories (but optionally include the other categories).
	dbCursor.execute("""SELECT definingCateg FROM terms_definingCateg WHERE terms_key = ?;""", (termKey,))
	defCats = pullQueryResults()
	if isinstance(defCats,list) and len(defCats)>0: #fail gacefully
		for i in range(0,len(defCats)):
			# print(str(1)+":",defCats[i])
			if defCats[i] == finalCategory: #if the finalCategory matches
				# print("***MATCH!***")
				return True
			else:
				dbCursor.execute("""SELECT definingCateg FROM terms_definingCateg WHERE term = ?;""", (defCats[i],))
				moreDC = pullQueryResults()
				if isinstance(moreDC,list) and len(moreDC)>0: #elif the found term is a finalCategory of its own
					if defTraitsOnly == True: #search within defining categories only
						if instance_searchTree(defCats[i],finalCategory,1,True) == True:
							# print("***MATCH!***")
							return True
					elif defTraitsOnly == False: #search within all relevant categories
						if instance_searchTree(defCats[i],finalCategory,1,) == True:
							# print("***MATCH!***")
							return True
				else: #elif the found term is NOT a finalCategory of its own
					pass #go to the next finalCategory in the list


	#search starting within the other categories (optional)
	if defTraitsOnly == False:
		dbCursor.execute("""SELECT otherCateg FROM terms_otherCateg WHERE terms_key = ?;""", (termKey,))
		othCats = pullQueryResults()
		if isinstance(othCats,list) and len(othCats)>0: #fail gacefully
			for i in range(0,len(othCats)):
				# print(str(1)+":",othCats[i])
				if othCats[i] == finalCategory: #if the finalCategory matches
					# print("***MATCH!***")
					return True
				else:
					dbCursor.execute("""SELECT otherCateg FROM terms_otherCateg WHERE term = ?;""", (othCats[i],))
					moreOC = pullQueryResults()
					if isinstance(moreOC,list) and len(moreOC)>0: #elif the found term is a finalCategory of its own
						if instance_searchTree(othCats[i],finalCategory,1,False) == True:
							# print("***MATCH!***")
							return True
					else:
						pass #go to the next finalCategory in the list

	#somehwere in/above here, add a place to store and check for negations!!! exceptions can be up to 49% of a category. example: penguins are birds but they cannot fly.


	return False