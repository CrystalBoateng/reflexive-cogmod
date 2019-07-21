import os
import sqlite3
dbConn = sqlite3.connect(os.path.dirname(__file__)+'/../learned_data/learned_data.db')
dbCursor = dbConn.cursor()
def pull_query_results():
	"""Copies the most recent SQLite selection. 
	This function should only be called after executing a SQLite query.
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