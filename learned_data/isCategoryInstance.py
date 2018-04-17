def currentDef (instance,finalCategory,defTraitsOnly=False): #function is used in knownMeanings defs
	print ("running isCategoryInstance()")
	return True
	# """Returns True if the 'instance' fits in the category 'finalCategory'. Else, returns false.
	# ----------Dependencies:
	# known_terms.py (in this script's directory)
	# findIndexOfString()

	# ----------Parameters:
	# instance = a string, such as 'guitar'
	# finalCategory = a string, such as 'musical instrument'
	# defTraitsOnly = only search for the categories that define the object. To do this, please use the function isDefiningCategory() instead.

	# ----------Returns:
	# a boolean.
	# """

	# def instance_searchTree(instance,finalCategory,instanceSearchesPerformed=0,visualizeTabs='',defTraitsOnly=False):
	# 	"""A recursive function. Returns True if the 'instance' fits in the category 'finalCategory'. Else, returns false.
	# 	This function gets called only by isCategoryInstance(). It should not be called directly.
	# 	----------Dependencies:
	# 	known_terms.py (in this script's directory)
	# 	findIndexOfString()

	# 	----------Parameters:
	# 	instance = a string, such as 'guitar'
	# 	finalCategory = a string, such as 'musical instrument'
	# 	instanceSearchesPerformed = an autmoatically-generated integer, to track how many layers of this function have been called. Terminates the search after 21 layers, to halt infinite loops.
	# 	visualizeTabs = a string conatining three spaces, to help with visualizing layers, during debugging.
	# 	defTraitsOnly (optional boolean) = only search for the categories that define the object (knownTerms[2]), and not the others (knownTerms[3]).

	# 	----------Returns:
	# 	a boolean.
	# 	"""

	# 	#break out of infinite loops
	# 	instanceSearchesPerformed += 1
	# 	if instanceSearchesPerformed >= 20:
	# 		print("%sinstanceSearchesPerformed=%s:   instance=%s   finalCategory=%s" % (visualizeTabs,instanceSearchesPerformed,instance,finalCategory))
	# 		print ("\nWhile searching for instances of a category, a possible infinite loop was detected. 21 iterations were reached, so the search was terminated.\n")
	# 		return False
		
	# 	for i in range (0,instanceSearchesPerformed):
	# 		visualizeTabs += '  '
	# 	# print("%s%s:   instance=%s   finalCategory=%s" % (visualizeTabs,instanceSearchesPerformed,instance,finalCategory))

	# 	#find the 'instance' string within knownTerms
	# 	instanceIndex = findIndexOfString(instance,knownTerms,0)
	# 	assert type(knownTerms[instanceIndex]) == list, "The object you're searching in, isn't a list. It's mostly likely a string, so if you search for an index within it, you'll only find one character."

	# 	#loop through defining categories (recursive)
	# 	for j in range(0,len(knownTerms[instanceIndex][2])):
	# 		# print("%s (j=%s)" % (visualizeTabs,j))
	# 		# print(visualizeTabs+" instance is:",knownTerms[instanceIndex][2][j])
	# 		if knownTerms[instanceIndex][2][j] == finalCategory: #if the finalCategory matches
	# 			# print("***MATCH!***")
	# 			return True
	# 		elif type(findIndexOfString(knownTerms[instanceIndex][2][j],knownTerms,0)) == int: #elif the category is a category of its own
	# 			if instance_searchTree(knownTerms[instanceIndex][2][j],finalCategory,instanceSearchesPerformed,visualizeTabs,defTraitsOnly) == True:
	# 				# print("***MATCH!***")
	# 				return True
	# 		else:
	# 			pass #go to the next finalCategory in the list

	# 	#loop through the other categories (recursive) (optional)
	# 	if defTraitsOnly == False: #if user requested ALL relevant categories, not just defining ones.
	# 		for k in range(0,len(knownTerms[instanceIndex][3])):
	# 			# print("%s (k=%s)" % (visualizeTabs,k))
	# 			# print(visualizeTabs+" instance is:",knownTerms[instanceIndex][3][k])
	# 			if knownTerms[instanceIndex][3][k] == finalCategory: #if the finalCategory matches
	# 				# print("***MATCH!***")
	# 				return True
	# 			elif type(findIndexOfString(knownTerms[instanceIndex][3][k],knownTerms,0)) == int: #elif the category is a category of its own
	# 				if instance_searchTree(knownTerms[instanceIndex][3][k],finalCategory,instanceSearchesPerformed,visualizeTabs,defTraitsOnly) == True:
	# 					# print("***MATCH!***")
	# 					return True
	# 			else:
	# 				pass #go to the next finalCategory in the list

	# 	return False # if no match was found at any point in this iteration of this function, return false

	# ### end of instance_searchTree()

	# # print("instance,finalCategory:",instance,finalCategory)
	# instanceSearchesPerformed = 0 # to detect infinite loops
	# visualizeTabs = ''

	# #verify that 'instance' is known
	# stringIndex = findIndexOfString(instance,knownTerms,0)
	# if knownTerms[stringIndex][0] == instance:
	# 	instance = knownTerms[stringIndex]
	# else:
	# 	return "I don't know what '%s' is." % instance


	# #search starting within defining categories (but optionally including the other categories).
	# for i in range(0,len(instance[2])):
	# 	instanceSearchesPerformed += 1
	# 	# print(str(instanceSearchesPerformed)+":",instance[2][i])
	# 	if instance[2][i] == finalCategory: #if the finalCategory matches
	# 		# print("***MATCH!***")
	# 		return True
	# 	elif type(findIndexOfString(instance[2][i],knownTerms,0)) == int: #elif the finalCategory is a finalCategory of its own
	# 		if defTraitsOnly == True: #search within defining categories only
	# 			if instance_searchTree(instance[2][i],finalCategory,instanceSearchesPerformed,'',True) == True:
	# 				# print("***MATCH!***")
	# 				return True
	# 		elif defTraitsOnly == False: #search within all relevant categories
	# 			if instance_searchTree(instance[2][i],finalCategory,instanceSearchesPerformed,'') == True:
	# 				# print("***MATCH!***")
	# 				return True
	# 	else:
	# 		pass #go to the next finalCategory in the list


	# #search starting within the other categories (optional)
	# if defTraitsOnly == True:
	# 	for k in range(0,len(instance[3])):
	# 		instanceSearchesPerformed += 1
	# 		# print(str(instanceSearchesPerformed)+":",instance[3][i])
	# 		if instance[3][k] == finalCategory: #if the finalCategory matches
	# 			# print("***MATCH!***")
	# 			return True
	# 		elif type(findIndexOfString(instance[3][k],knownTerms,0)) == int: #elif the finalCategory is a finalCategory of its own
	# 			if instance_searchTree(instance[3][k],finalCategory,instanceSearchesPerformed,'') == True:
	# 				# print("***MATCH!***")
	# 				return True
	# 		else:
	# 			pass #go to the next finalCategory in the list

	# #somehwere in/above here, add a place to store and check for negations!!! exceptions can be up to 49% of a category. example: penguins are birds but they cannot fly.


	# return False
