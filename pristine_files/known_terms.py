#The reason this file is stored in the root directory is so that it can be written-to/read, without starting a new runtime. This requires executing it within an execution. The function which performs this task is refreshKnownTerms().

#Conjugation key names and the conjugations for the following verbs are from the 'compromise', an open-source NLP project published under a copyleft MIT license. A copy of the license is provided here, under /nlp_resources/compromise's MIT License.txt. View the source code and the license, at: github.com/nlp-compromise/compromise or at http://compromise.cool 
	#'take','can','free','puke','arise','babysit','be','is','beat','begin','ban','bet','bite','bleed','breed','bring','broadcast','build','buy','choose','cost','deal','die','dig','draw','drink','drive','eat','fall','feed','feel','fight','find','fly','blow','forbid','edit','forget','forgive','freeze','get','give','go','hang','have','hear','hide','hold','hurt','lay','lead','leave','lie','light','lose','make','mean','meet','pay','read','ring','rise','run','say','see','sell','shine','shoot','show','sing','sink','sit','slide','speak','spin','stand','steal','stick','sting','stream','strike','swear','swim','swing','teach','tear','tell','think','understand','wake','wear','win','withdraw','write','tie','ski','boil','miss','act','compete','being','imply','ice','develop','wait','aim','spill','drop','log','rub','smash','egg','suit','age','shed','break','catch','do','bind','spread','become','bend','brake','burn','burst','cling','come','creep','cut','dive','dream','flee','fling','got','grow','hit','keep','kneel','know','leap','lend','loose','prove','put','quit','ride','seek','send','set','sew','shake','shave','shut','seat','slay','sleep','sneak','speed','spend','spit','split','spring','stink','strew','sware','sweep','thrive','undergo','upset','weave','weep','wind','wring'.

print ("\t\tknown_terms.py opened successfully.")
global knownTerms
	#RULES: 
	# category lists are sparse (i.e. not comprehensive), and are subjective.
	# the rest of these rules are just suggestions; none of this needs to be perfect in order to function.
	# all nouns should be singular and nominative case (e.g. "I", not "me"). all verbs should be infinitive present-tense, without the word 'to' (e.g. "fly", not "to fly").
	# 'negated' categories (e.g. 'not animal') are only allowed if they're exceptions to a rule. For example, "not fly" is allowed for "penguin" because bird has the property "fly"). They can also be allowed if they're stand-alone terms on their own (e.g. 'non-smoking' or 'inanimate').
	# nested categories are NOT required! also, no category is required to link to a root category; free-floating branches are fine.
	# terms can be longer sentence fragments, but ideally they will be words or phrases. this maximizes pattern-recognition during reflection.
knownTerms = [ 
	#Each list contains the following:
		# ["the term", 
		# "Part Of Speech" - For a complete list, see http://universaldependencies.org/u/pos/
		# [defining categories - the categories which define the object ontologically, and into which ALL instances can be classified. example: every time someone 'defines' something, they are 'describing' it.
		# [any other category into which ALL instances can be classified. example: ALL instances of 'defining' are 'stating'.] 
		# {various forms of the term, e.g. conjugation for verbs or plaurality for nouns or whatever}
		 	#  Some of the keys in this dictionary are: 
				# 'Plaural': 	# defaults to the singular form plus 's'
				# 'PastTense':
				# 'PresentTense':
				# 'Gerund':
				# 'Actor':		# defaults to the gerund form minus "ing" plus "er".
				# 'Singular3rdPersonPerfectTense':
				# 'PerfectTense':
				# 'Pluperfect':
				# (and for the verb "be": 'PluralPastTense', 'PluralPresentTense', 'PluralInfinitive').
			# 'Infinitive' is omitted because it's already included in index 0.
			# 'FutureTense' is omitted because it's just "will " + the infinitive.
			
			# The dictionary doesn't need to be comprehensive, because I intend to write a conjugation function which cascades to the next-most-appropriate conjugation, whenever the requested conjugation is unavailable.
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
] #END CONTENT (do not edit or delete this line).