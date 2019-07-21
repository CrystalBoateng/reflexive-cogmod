from utilities.util_pull_query_results import *

#extended recursions
def instance_search_tree(instance,finalCategory,instanceSearchesPerformed,defTraitsOnly=False):
	"""An infinitely recursive function. Returns True if the 'instance' fits in the category 'finalCategory'. Else, returns false.
	This function gets called only by is_category_instance(). It should not be called directly.
	
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
	## visualizations (for debugging)
	# for i in range (0,instanceSearchesPerformed):
	# 	visualizeTabs += '  '
	# print("%s%s:   instance=%s   finalCategory=%s" % (visualizeTabs,instanceSearchesPerformed,instance,finalCategory))
	# find the key of the 'instance' term
	dbCursor.execute("""
		SELECT key FROM terms WHERE term = ?
		;""", (instance,)) # TODO: accommodate homonyms so they dont break this
	instanceKey = pull_query_results()
	# print("instanceKey=",str(instanceKey))
	if instanceKey and isinstance(instanceKey,list):
		instanceKey = instanceKey[0]
		# loop through defining categories (recursive)
		dbCursor.execute("""
			SELECT definingCateg FROM terms_definingCateg WHERE terms_key = ?
			;""", (instanceKey,))
		iDefCats = pull_query_results()
		if iDefCats and isinstance(iDefCats,list):
			for j in range(len(iDefCats)):
				# print("%s (j=%s)" % (visualizeTabs,j))
				# print(visualizeTabs+" instance is:",iDefCats[j])
				if iDefCats[j] == finalCategory: #if the finalCategory matches
					return True
				else:
					dbCursor.execute("""
						SELECT definingCateg FROM terms_definingCateg WHERE term = ?
						;""", (iDefCats[j],))
					moreIDC = pull_query_results()
					if moreIDC and isinstance(moreIDC,list): #elif the category is a category of its own
						if instance_search_tree(iDefCats[j],finalCategory,instanceSearchesPerformed,defTraitsOnly):
							return True
					else: #elif the found term is NOT a finalCategory of its own
						pass #go to the next finalCategory in the list
			#loop through the other categories (recursive) (optional)
			if defTraitsOnly == False: #if user requested ALL relevant categories, not just defining ones.
				dbCursor.execute("""
					SELECT otherCateg FROM terms_otherCateg WHERE terms_key = ?
					;""", (instanceKey,))
				iOthCats = pull_query_results()
				if iOthCats and isinstance(iOthCats,list):
					for j in range(len(iOthCats)):
						# print("%s (j=%s)" % (visualizeTabs,j))
						# print(visualizeTabs+" instance is:",iOthCats[j])
						if iOthCats[j] == finalCategory: #if the finalCategory matches
							return True
						else:
							dbCursor.execute("""
								SELECT otherCateg FROM terms_otherCateg WHERE term = ?
								;""", (iOthCats[j],))
							moreIOC = pull_query_results()
							if moreIOC and isinstance(moreIOC,list): #elif the category is a category of its own
								if instance_search_tree(iOthCats[j],finalCategory,instanceSearchesPerformed,defTraitsOnly):
									return True
							else: # elif the found term is NOT a finalCategory of its own
								pass # go to the next finalCategory in the list
			# if no match was found at any point in this iteration of this function, return false
			return False 

# the function for which this file gets called
def is_category_instance (instance,finalCategory,defTraitsOnly=False):
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
	# print ("running is_category_instance()")
	# print("instance,finalCategory:",instance,finalCategory)
	visualizeTabs = ''
	# verify that the 'instance' is known
	dbCursor.execute("""
		SELECT key FROM terms WHERE term = ?
		;""", (instance,)) # TODO: accommodate homonyms so they dont break this
	termKey = pull_query_results()
	if termKey and isinstance(termKey,list):
		termKey = termKey[0]
	else:
		print ("\t\t\tis_category_instance() can't find '%s' in the database. Returned None." % instance)
		return None
	# search starting within defining categories (but optionally include the other categories).
	dbCursor.execute("""
		SELECT definingCateg FROM terms_definingCateg WHERE terms_key = ?
		;""", (termKey,))
	defCats = pull_query_results()
	if defCats and isinstance(defCats,list): #fail gacefully
		for i in range(len(defCats)):
			if defCats[i] == finalCategory: #if the finalCategory matches
				return True
			else:
				dbCursor.execute("""
					SELECT definingCateg FROM terms_definingCateg WHERE term = ?
					;""", (defCats[i],))
				moreDC = pull_query_results()
				if moreDC and isinstance(moreDC,list): #elif the found term is a finalCategory of its own
					if defTraitsOnly: #search within defining categories only
						if instance_search_tree(defCats[i],finalCategory,1,True):
							return True
					elif defTraitsOnly == False: #search within all relevant categories
						if instance_search_tree(defCats[i],finalCategory,1,):
							return True
				else: #elif the found term is NOT a finalCategory of its own
					pass #go to the next finalCategory in the list
	#search starting within the other categories (optional)
	if defTraitsOnly == False:
		dbCursor.execute("""
			SELECT otherCateg FROM terms_otherCateg WHERE terms_key = ?
			;""", (termKey,))
		othCats = pull_query_results()
		if othCats and isinstance(othCats,list): #fail gacefully
			for i in range(len(othCats)):
				# print(str(1)+":",othCats[i])
				if othCats[i] == finalCategory: #if the finalCategory matches
					return True
				else:
					dbCursor.execute("""
						SELECT otherCateg FROM terms_otherCateg WHERE term = ?
						;""", (othCats[i],))
					moreOC = pull_query_results()
					if moreOC and isinstance(moreOC,list): #elif the found term is a finalCategory of its own
						if instance_search_tree(othCats[i],finalCategory,1,False):
							return True
					else:
						pass #go to the next finalCategory in the list
	# somehwere in/above here, add a place to store and check for negations. exceptions can be up to 49% of a category. example: penguins are birds but they cannot fly.
	return False