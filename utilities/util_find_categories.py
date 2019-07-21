#import dependencies
import os.path, sqlite3
dbConn = sqlite3.connect(os.path.dirname(__file__)
	+ '/learned_data.db')
dbCursor = dbConn.cursor()
from utilities.util_pull_query_results import *

# main functionality
def find_categories (inputTerm,defTraitsOnly=False):
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
	def instance_cat_tree(inputTerm,inputTermSearchesPerformed=0,defTraitsOnly=False):
		"""An infinitely recursive function. Appends the appropriate categories to the variable allCats (which is decalred outside of this function.)
		This function gets called only by find_categories(). It should not be called directly.
		
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
			print ("\nWhile searching for term categories, instance_cat_tree() detected a possible infinite loop. 21 iterations were reached, so the search was terminated.\n")
			return True
		## visualizations (for debugging)
		# for i in range (0,inputTermSearchesPerformed):
		# 	visualizeTabs += '  '
		# print("%s%s:   inputTerm=%s" % (visualizeTabs,inputTermSearchesPerformed,inputTerm))
		#find the key of the inputTerm
		dbCursor.execute("""
			SELECT key FROM terms WHERE term = ?;
			""", (inputTerm,)) # TODO: accommodate homonyms so they dont break this
		inputTermKey = pull_query_results()
		if inputTermKey and isinstance(inputTermKey,list):
			inputTermKey = inputTermKey[0]
			#loop through defining categories (recursive)
			dbCursor.execute("""
				SELECT definingCateg FROM terms_definingCateg WHERE terms_key = ?;
				""", (inputTermKey,))
			iDefCats = pull_query_results()
			if iDefCats and isinstance(iDefCats,list):
				for j in range(len(iDefCats)):
					# print("%s (j=%s)" % (visualizeTabs,j))
					# print(visualizeTabs+" inputTerm is:",iDefCats[j])
					allCats.append(iDefCats[j])

					dbCursor.execute("""
						SELECT definingCateg FROM terms_definingCateg WHERE term = ?;
						""", (iDefCats[j],))
					moreIDC = pull_query_results()
					if moreIDC and isinstance(moreIDC,list): #elif that term is a category of its own, call self again.
						instance_cat_tree(iDefCats[j],inputTermSearchesPerformed,defTraitsOnly)
					else: # elif that term is NOT a category of its own
						pass
			#loop through the other categories (recursive) (optional)
			if defTraitsOnly == False: #if user requested ALL relevant categories, not just defining ones.
				dbCursor.execute("""
					SELECT otherCateg FROM terms_otherCateg WHERE terms_key = ?;
					""", (inputTermKey,))
				iOthCats = pull_query_results()
				if iOthCats and isinstance(iOthCats,list):
					for j in range(len(iOthCats)):
						# print("%s (j=%s)" % (visualizeTabs,j))
						# print(visualizeTabs+" inputTerm is:",iOthCats[j])
						allCats.append(iOthCats[j])
						dbCursor.execute("""
							SELECT otherCateg FROM terms_otherCateg WHERE term = ?;
							""", (iOthCats[j],))
						moreIDC = pull_query_results()
						if moreIDC and isinstance(moreIDC,list): #elif that term is a category of its own, call self again.
							instance_cat_tree(iOthCats[j],inputTermSearchesPerformed,defTraitsOnly)
						else: #elif that term is NOT a category of its own
							pass
		return True #when finished, cascade back up to the most recent call
		### end of instance_cat_tree()
	# print ("running find_categories()")
	allCats = []
	inputTermSearchesPerformed = 0 # to detect infinite loops
	visualizeTabs = ''
	#verify that the 'inputTerm' is known
	if type(inputTerm) == str: 
		#get the key of inputTerm
		# print("1:   "+inputTerm) #for vizualization
		dbCursor.execute("""
			SELECT key FROM terms WHERE term = ?;
			""", (inputTerm,)) # TODO: accommodate homonyms so they dont break this
		termKey = pull_query_results()
		if termKey and isinstance(termKey,list):
			termKey = termKey[0]
			# print("termKey=",str(termKey))
		else:
			print ("\t\t\tfind_categories() couldn't find '%s' in the database. Therefore, no categories were found." % inputTerm)
			return []
	else:
		#give up
		print("find_categories() in util_find_categories.py was passed a non-string argument: %s. Returned []." % str(inputTerm))
		return []
	#search starting within defining categories (but optionally include the other categories).
	dbCursor.execute("""SELECT definingCateg FROM terms_definingCateg WHERE terms_key = ?;
		""", (termKey,))
	defCats = pull_query_results()
	if defCats and isinstance(defCats,list):
		for i in range(len(defCats)):
			inputTermSearchesPerformed += 1
			# print(str(inputTermSearchesPerformed)+":",defCats[i])
			allCats.append(defCats[i])
			dbCursor.execute("""
				SELECT definingCateg FROM terms_definingCateg WHERE term = ?;
				""", (defCats[i],)) 
			moreDC = pull_query_results()
			if moreDC and isinstance(moreDC,list): #elif the found term is a category of its own
				instance_cat_tree(defCats[i],inputTermSearchesPerformed,defTraitsOnly)
	#search starting within the other categories (optional)
	if defTraitsOnly == False:
		dbCursor.execute("""
			SELECT otherCateg FROM terms_otherCateg WHERE terms_key = ?;
			""", (termKey,))
		othCats = pull_query_results()
		if othCats and isinstance(othCats,list):
			for i in range(len(othCats)):
				inputTermSearchesPerformed += 1
				# print(str(inputTermSearchesPerformed)+":",othCats[i])
				allCats.append(othCats[i])
				dbCursor.execute("""SELECT otherCateg FROM terms_otherCateg WHERE term = ?;
					""", (othCats[i],))
				moreOC = pull_query_results()
				if moreOC and isinstance(moreOC,list): #elif the found term is a category of its own
					instance_cat_tree(othCats[i],inputTermSearchesPerformed,defTraitsOnly)
				#go to the next category in the list
	return allCats