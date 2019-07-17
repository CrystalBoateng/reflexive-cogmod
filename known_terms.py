print ("\t\tknown_terms.py opened successfully.")
global knownTerms
knownTerms = [ 
	# Each list contains the following:
		# ["the term", 
		# "Part Of Speech" - For a complete list, see http://universaldependencies.org/u/pos/
		# [defining categories - the categories which define the object ontologically, and into which ALL instances can be classified. example: every time someone 'defines' something, they are 'describing' it.
		# [any other category into which ALL instances can be classified. example: ALL instances of 'defining' are 'stating'.] 
		# {various forms of the term, e.g. conjugation for verbs or plaurality for nouns or whatever}
		 	#  Some of the keys in this dictionary are: 
				# 'Plaural': 	*defaults to the singular form plus 's'
				# 'PastTense':
				# 'PresentTense':
				# 'Gerund':
				# 'Actor':		*defaults to the gerund form minus "ing" plus "er".
				# 'Singular3rdPersonPerfectTense':
				# 'PerfectTense':
				# 'Pluperfect':
				# (and for the verb "be": 'PluralPastTense', 'PluralPresentTense', 'PluralInfinitive').
			# 'Infinitive' is omitted because it's already included in index 0.
			# 'FutureTense' is omitted because it's simply "will " + the infinitive.
			

		# ],
#BEGIN CONTENT (do not edit or delete this line).
	["instrument", "NOUN",
			["object",], [], {},
	],
	["inanimate", "ADJ",
			["object",], [], {},
	],
	["musical instrument", "NOUN",
			["instrument","tool","inanimate",], [], {},
	],
	["object shaped like a guitar", "NOUN",
			["object",], [], {'Plaural':"objects shaped like guitars"},
	],
	["guitar", "NOUN",
			["musical instrument", "object shaped like a guitar",], ["bridged",], {},
	],
	["physical object owned by me", "NOUN",
			["object","owned by me",], [], {'Plaural':"physical objects which I own"},
	],
	["dominionstats", "NOUN",
			["software","owned by me",], [],
	],
	["huntokar", "NOUN",
			["guitar","black","physical object owned by me",], [], {},
	],
	["black", "ADJ",
			["color","dark",], [], {},
	],
	["run", "VERB",
			["action","locomote","use",], [], {'PastTense':"ran",'Gerund':"running",'Singular3rdPersonPerfectTense':"has run",'PerfectTense':"have run",'Pluperfect':"had run",},
	],


	["fly", "VERB",
			["in air",], [], {'PastTense':"flew",'Gerund':"flying",'Singular3rdPersonPerfectTense':"has flown",'PerfectTense':"have flown",'Pluperfect':"had flown",'Participle':"flown",},
	],
	["bird", "NOUN",
			["fly","animal",], ["winged",], {},
	],
	["goose", "NOUN",
			["bird","aquatic","waterfowl",], ["migrational",], {'Plaural':"geese"},
	],
	["penguin", "NOUN",
			["bird","tuxedo-wearing","aquatic","not fly",], [], {},
	],
	["duck", "NOUN",
			["bird","aquatic","waterfowl",], [], {},
	],
	["aquatic", "ADJ",
			["live in water",], [], {},
	],


	["include", "VERB",
			[], [], {'PastTense':"included",'Gerund':"including",'PerfectTense':"have included",'Pluperfect':"had included",},
	],
	["define", "VERB",
			["describe",], ["state",], {'PastTense':"defined",'Gerund':"defining",'Singular3rdPersonPerfectTense':"has defined",'PerfectTense':"have defined",'Pluperfect':"had defined",},
	],
	["number", "NOUN",
			["CONCEPT",], ["symbol","word","abstraction",], {},
	],
	["longer", "ADJ",
			["comparative",], ["long",], {},
	],
] #END CONTENT (do not edit or delete this line).