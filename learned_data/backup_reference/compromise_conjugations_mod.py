#All verb conjugations in this file are pulled from the javascript NLP Project 'compromise', published under a copyleft MIT license. View the 'compromise' license and the source code here: github.com/nlp-compromise/compromise The license is also included in this directory (/nlp_resources), which is required.
#View the 'compromise' main website here: http://compromise.cool
# View the unmodified code here: https://github.com/nlp-compromise/compromise/blob/master/data/conjugations.js

#The contents below have been modified to match the syntax of known_terms.py. When a verb conjugation in a piece of text is not found in known_terms.py, read() searches this file. If the verb is found in here, then the term is pushed to known_terms.py. ...or at least it will once I write get around to writing it. #incomplete

#{}{}{}{}{}{}{}{}{}{}{} STATS:
#{}
#{}  PastTense: 112 instances
#{}  Participle : 109 instances
#{}  Gerund : 43 instances
#{}  Actor: 20 instances
#{}  PresentTense : 14 instances
#{}  PluPerfectTense: 5 instances
#{}  FuturePerfect: 4 instances
#{}  PerfectTense : 3 instances
#{}  Infinitives are not defined, because they are already listed as the first string in the list
#{}  FutureTense is not defined, because you simply add 'will ' to the infinitive.
#{}
#{}{}{}{}{}{}{}{}{}{}{}


compromiseConjugations = [
    ['take', "VERB", [], [], {
        'PerfectTense': 'have taken',
        'PluPerfectTense': 'had taken',
        'PastTense': 'took',
        'FuturePerfect': 'will have taken'
    },],
    ['can', "VERB", [], [], {
        'Gerund': '',
        'PresentTense': 'can',
        'PastTense': 'could',
        'PerfectTense': 'could',
        'PluPerfectTense': 'could',
        'FuturePerfect': 'can',
        'Actor': ''
    },],
    ['free', "VERB", [], [], {
        'Gerund': 'freeing',
        'Actor': ''
    },],
    ['puke', "VERB", [], [], {
        'Gerund': 'puking'
    },],
    ['arise', "VERB", [], [], {
        'PastTense': 'arose',
        'Participle': 'arisen'
    },],
    ['babysit', "VERB", [], [], {
        'PastTense': 'babysat',
        'Actor': 'babysitter'
    },],
    ['be', "VERB", [], [], {
        'PastTense': 'was',
        'Participle': 'been',
        'PresentTense': 'is',
        'Actor': '',
        'Gerund': 'am' #this verb has many conjugations and therefore is a good case study for how to cascade downwards when some of them are missing. see also "is", below.
    },],
    ['is', "VERB", [], [], {
        'PastTense': 'was',
        'PresentTense': 'is',
        'Actor': '',
        'Gerund': 'being'
    },],
    ['beat', "VERB", [], [], {
        'Gerund': 'beating',
        'Actor': 'beater',
        'Participle': 'beaten'
    },],
    ['begin', "VERB", [], [], {
        'Gerund': 'beginning',
        'PastTense': 'began',
        'Participle': 'begun'
    },],
    ['ban', "VERB", [], [], {
        'PastTense': 'banned',
        'Gerund': 'banning',
        'Actor': ''
    },],
    ['bet', "VERB", [], [], {
        'Actor': 'better',
        'Participle': 'bet'
    },],
    ['bite', "VERB", [], [], {
        'Gerund': 'biting',
        'PastTense': 'bit',
        'Participle': 'bitten'
    },],
    ['bleed', "VERB", [], [], {
        'PastTense': 'bled',
        'Participle': 'bled'
    },],
    ['breed', "VERB", [], [], {
        'PastTense': 'bred'
    },],
    ['bring', "VERB", [], [], {
        'PastTense': 'brought',
        'Participle': 'brought'
    },],
    ['broadcast', "VERB", [], [], {
        'PastTense': 'broadcast'
    },],
    ['build', "VERB", [], [], {
        'PastTense': 'built',
        'Participle': 'built'
    },],
    ['buy', "VERB", [], [], {
        'PastTense': 'bought',
        'Participle': 'bought'
    },],
    ['choose', "VERB", [], [], {
        'Gerund': 'choosing',
        'PastTense': 'chose',
        'Participle': 'chosen'
    },],
    ['cost', "VERB", [], [], {
        'PastTense': 'cost'
    },],
    ['deal', "VERB", [], [], {
        'PastTense': 'dealt',
        'Participle': 'dealt'
    },],
    ['die', "VERB", [], [], {
        'PastTense': 'died',
        'Gerund': 'dying'
    },],
    ['dig', "VERB", [], [], {
        'Gerund': 'digging',
        'PastTense': 'dug',
        'Participle': 'dug'
    },],
    ['draw', "VERB", [], [], {
        'PastTense': 'drew',
        'Participle': 'drawn'
    },],
    ['drink', "VERB", [], [], {
        'PastTense': 'drank',
        'Participle': 'drunk'
    },],
    ['drive', "VERB", [], [], {
        'Gerund': 'driving',
        'PastTense': 'drove',
        'Participle': 'driven'
    },],
    ['eat', "VERB", [], [], {
        'Gerund': 'eating',
        'PastTense': 'ate',
        'Actor': 'eater',
        'Participle': 'eaten'
    },],
    ['fall', "VERB", [], [], {
        'PastTense': 'fell',
        'Participle': 'fallen'
    },],
    ['feed', "VERB", [], [], {
        'PastTense': 'fed',
        'Participle': 'fed'
    },],
    ['feel', "VERB", [], [], {
        'PastTense': 'felt',
        'Actor': 'feeler'
    },],
    ['fight', "VERB", [], [], {
        'PastTense': 'fought',
        'Participle': 'fought'
    },],
    ['find', "VERB", [], [], {
        'PastTense': 'found'
    },],
    ['fly', "VERB", [], [], {
        'PastTense': 'flew',
        'Participle': 'flown'
    },],
    ['blow', "VERB", [], [], {
        'PastTense': 'blew',
        'Participle': 'blown'
    },],
    ['forbid', "VERB", [], [], {
        'PastTense': 'forbade'
    },],
    ['edit', "VERB", [], [], {
        'Gerund': 'editing'
    },],
    ['forget', "VERB", [], [], {
        'Gerund': 'forgeting',
        'PastTense': 'forgot',
        'Participle': 'forgotten'
    },],
    ['forgive', "VERB", [], [], {
        'Gerund': 'forgiving',
        'PastTense': 'forgave',
        'Participle': 'forgiven'
    },],
    ['freeze', "VERB", [], [], {
        'Gerund': 'freezing',
        'PastTense': 'froze',
        'Participle': 'frozen'
    },],
    ['get', "VERB", [], [], {
        'PastTense': 'got'
    },],
    ['give', "VERB", [], [], {
        'Gerund': 'giving',
        'PastTense': 'gave',
        'Participle': 'given'
    },],
    ['go', "VERB", [], [], {
        'PastTense': 'went',
        'PresentTense': 'goes',
        'Participle': 'gone'
    },],
    ['hang', "VERB", [], [], {
        'PastTense': 'hung',
        'Participle': 'hung'
    },],
    ['have', "VERB", [], [], {
        'Gerund': 'having',
        'PastTense': 'had',
        'PresentTense': 'has',
        'Participle': 'had'
    },],
    ['hear', "VERB", [], [], {
        'PastTense': 'heard',
        'Participle': 'heard'
    },],
    ['hide', "VERB", [], [], {
        'PastTense': 'hid',
        'Participle': 'hidden'
    },],
    ['hold', "VERB", [], [], {
        'PastTense': 'held',
        'Participle': 'held'
    },],
    ['hurt', "VERB", [], [], {
        'PastTense': 'hurt',
        'Participle': 'hurt'
    },],
    ['lay', "VERB", [], [], {
        'PastTense': 'laid',
        'Participle': 'laid'
    },],
    ['lead', "VERB", [], [], {
        'PastTense': 'led',
        'Participle': 'led'
    },],
    ['leave', "VERB", [], [], {
        'PastTense': 'left',
        'Participle': 'left'
    },],
    ['lie', "VERB", [], [], {
        'Gerund': 'lying',
        'PastTense': 'lay'
    },],
    ['light', "VERB", [], [], {
        'PastTense': 'lit',
        'Participle': 'lit'
    },],
    ['lose', "VERB", [], [], {
        'Gerund': 'losing',
        'PastTense': 'lost'
    },],
    ['make', "VERB", [], [], {
        'PastTense': 'made',
        'Participle': 'made'
    },],
    ['mean', "VERB", [], [], {
        'PastTense': 'meant',
        'Participle': 'meant'
    },],
    ['meet', "VERB", [], [], {
        'Gerund': 'meeting',
        'PastTense': 'met',
        'Actor': 'meeter',
        'Participle': 'met'
    },],
    ['pay', "VERB", [], [], {
        'PastTense': 'paid',
        'Participle': 'paid'
    },],
    ['read', "VERB", [], [], {
        'PastTense': 'read',
        'Participle': 'read'
    },],
    ['ring', "VERB", [], [], {
        'PastTense': 'rang',
        'Participle': 'rung'
    },],
    ['rise', "VERB", [], [], {
        'PastTense': 'rose',
        'Gerund': 'rising',
        'PluPerfectTense': 'had risen',
        'FuturePerfect': 'will have risen',
        'Participle': 'risen'
    },],
    ['run', "VERB", [], [], {
        'Gerund': 'running',
        'PastTense': 'ran',
        'Participle': 'run'
    },],
    ['say', "VERB", [], [], {
        'PastTense': 'said',
        'Participle': 'said',
        'PresentTense': 'says'
    },],
    ['see', "VERB", [], [], {
        'PastTense': 'saw',
        'Participle': 'seen'
    },],
    ['sell', "VERB", [], [], {
        'PastTense': 'sold',
        'Participle': 'sold'
    },],
    ['shine', "VERB", [], [], {
        'PastTense': 'shone',
        'Participle': 'shone'
    },],
    ['shoot', "VERB", [], [], {
        'PastTense': 'shot',
        'Participle': 'shot'
    },],
    ['show', "VERB", [], [], {
        'PastTense': 'showed'
    },],
    ['sing', "VERB", [], [], {
        'PastTense': 'sang',
        'Participle': 'sung'
    },],
    ['sink', "VERB", [], [], {
        'PastTense': 'sank',
        'PluPerfectTense': 'had sunk'
    },],
    ['sit', "VERB", [], [], {
        'PastTense': 'sat'
    },],
    ['slide', "VERB", [], [], {
        'PastTense': 'slid',
        'Participle': 'slid'
    },],
    ['speak', "VERB", [], [], {
        'PastTense': 'spoke',
        'PerfectTense': 'have spoken',
        'PluPerfectTense': 'had spoken',
        'FuturePerfect': 'will have spoken',
        'Participle': 'spoken'
    },],
    ['spin', "VERB", [], [], {
        'Gerund': 'spinning',
        'PastTense': 'spun',
        'Participle': 'spun'
    },],
    ['stand', "VERB", [], [], {
        'PastTense': 'stood'
    },],
    ['steal', "VERB", [], [], {
        'PastTense': 'stole',
        'Actor': 'stealer'
    },],
    ['stick', "VERB", [], [], {
        'PastTense': 'stuck'
    },],
    ['sting', "VERB", [], [], {
        'PastTense': 'stung'
    },],
    ['stream', "VERB", [], [], {
        'Actor': 'streamer'
    },],
    ['strike', "VERB", [], [], {
        'Gerund': 'striking',
        'PastTense': 'struck'
    },],
    ['swear', "VERB", [], [], {
        'PastTense': 'swore'
    },],
    ['swim', "VERB", [], [], {
        'PastTense': 'swam',
        'Gerund': 'swimming'
    },],
    ['swing', "VERB", [], [], {
        'PastTense': 'swung'
    },],
    ['teach', "VERB", [], [], {
        'PastTense': 'taught',
        'PresentTense': 'teaches'
    },],
    ['tear', "VERB", [], [], {
        'PastTense': 'tore'
    },],
    ['tell', "VERB", [], [], {
        'PastTense': 'told'
    },],
    ['think', "VERB", [], [], {
        'PastTense': 'thought'
    },],
    ['understand', "VERB", [], [], {
        'PastTense': 'understood'
    },],
    ['wake', "VERB", [], [], {
        'PastTense': 'woke'
    },],
    ['wear', "VERB", [], [], {
        'PastTense': 'wore'
    },],
    ['win', "VERB", [], [], {
        'Gerund': 'winning',
        'PastTense': 'won'
    },],
    ['withdraw', "VERB", [], [], {
        'PastTense': 'withdrew'
    },],
    ['write', "VERB", [], [], {
        'Gerund': 'writing',
        'PastTense': 'wrote',
        'Participle': 'written'
    },],
    ['tie', "VERB", [], [], {
        'Gerund': 'tying',
        'PastTense': 'tied'
    },],
    ['ski', "VERB", [], [], {
        'PastTense': 'skiied'
    },],
    ['boil', "VERB", [], [], {
        'Actor': 'boiler'
    },],
    ['miss', "VERB", [], [], {
        'PresentTense': 'miss'
    },],
    ['act', "VERB", [], [], {
        'Actor': 'actor'
    },],
    ['compete', "VERB", [], [], {
        'Gerund': 'competing',
        'PastTense': 'competed',
        'Actor': 'competitor'
    },],
    ['being', "VERB", [], [], {
        'Gerund': 'are',
        'PastTense': 'were',
        'PresentTense': 'are'
    },],
    ['imply', "VERB", [], [], {
        'PastTense': 'implied',
        'PresentTense': 'implies'
    },],
    ['ice', "VERB", [], [], {
        'Gerund': 'icing',
        'PastTense': 'iced'
    },],
    ['develop', "VERB", [], [], {
        'PastTense': 'developed',
        'Actor': 'developer',
        'Gerund': 'developing'
    },],
    ['wait', "VERB", [], [], {
        'Gerund': 'waiting',
        'PastTense': 'waited',
        'Actor': 'waiter'
    },],
    ['aim', "VERB", [], [], {
        'Actor': 'aimer',
        'Gerund': 'aiming',
        'PastTense': 'aimed'
    },],
    ['spill', "VERB", [], [], {
        'PastTense': 'spilt',
        'Participle': 'spilled'
    },],
    ['drop', "VERB", [], [], {
        'Gerund': 'dropping',
        'PastTense': 'dropped'
    },],
    ['log', "VERB", [], [], {
        'Gerund': 'logging',
        'PastTense': 'logged'
    },],
    ['rub', "VERB", [], [], {
        'Gerund': 'rubbing',
        'PastTense': 'rubbed'
    },],
    ['smash', "VERB", [], [], {
        'PresentTense': 'smashes'
    },],
    ['egg', "VERB", [], [], {
        'PastTense': 'egged'
    },],
    ['suit', "VERB", [], [], {
        'Gerund': 'suiting',
        'PastTense': 'suited',
        'Actor': 'suiter'
    },],
    ['age', "VERB", [], [], {
        'PresentTense': 'ages',
        'PastTense': 'aged',
        'Gerund': 'ageing'
    },],
    ['shed', "VERB", [], [], {
        'PresentTense': 'sheds',
        'PastTense': 'shed',
        'Gerund': 'shedding'
    },],
    ['break', "VERB", [], [], {
        'PastTense': 'broke'
    },],
    ['catch', "VERB", [], [], {
        'PastTense': 'caught'
    },],
    ['do', "VERB", [], [], {
        'PastTense': 'did',
        'PresentTense': 'does'
    },],
    ['bind', "VERB", [], [], {
        'PastTense': 'bound'
    },],
    ['spread', "VERB", [], [], {
        'PastTense': 'spread'
    },],
    ['become', "VERB", [], [], {
        'Participle': 'become'
    },],
    ['bend', "VERB", [], [], {
        'Participle': 'bent'
    },],
    ['brake', "VERB", [], [], {
        'Participle': 'broken'
    },],
    ['burn', "VERB", [], [], {
        'Participle': 'burned'
    },],
    ['burst', "VERB", [], [], {
        'Participle': 'burst'
    },],
    ['cling', "VERB", [], [], {
        'Participle': 'clung'
    },],
    ['come', "VERB", [], [], {
        'Participle': 'come',
        'PastTense': 'came'
    },],
    ['creep', "VERB", [], [], {
        'Participle': 'crept'
    },],
    ['cut', "VERB", [], [], {
        'Participle': 'cut'
    },],
    ['dive', "VERB", [], [], {
        'Participle': 'dived'
    },],
    ['dream', "VERB", [], [], {
        'Participle': 'dreamt'
    },],
    ['flee', "VERB", [], [], {
        'Participle': 'fled'
    },],
    ['fling', "VERB", [], [], {
        'Participle': 'flung'
    },],
    ['got', "VERB", [], [], {
        'Participle': 'gotten'
    },],
    ['grow', "VERB", [], [], {
        'Participle': 'grown'
    },],
    ['hit', "VERB", [], [], {
        'Participle': 'hit'
    },],
    ['keep', "VERB", [], [], {
        'Participle': 'kept'
    },],
    ['kneel', "VERB", [], [], {
        'Participle': 'knelt'
    },],
    ['know', "VERB", [], [], {
        'Participle': 'known'
    },],
    ['leap', "VERB", [], [], {
        'Participle': 'leapt'
    },],
    ['lend', "VERB", [], [], {
        'Participle': 'lent'
    },],
    ['loose', "VERB", [], [], {
        'Participle': 'lost'
    },],
    ['prove', "VERB", [], [], {
        'Participle': 'proven'
    },],
    ['put', "VERB", [], [], {
        'Participle': 'put'
    },],
    ['quit', "VERB", [], [], {
        'Participle': 'quit'
    },],
    ['ride', "VERB", [], [], {
        'Participle': 'ridden'
    },],
    ['seek', "VERB", [], [], {
        'Participle': 'sought'
    },],
    ['send', "VERB", [], [], {
        'Participle': 'sent'
    },],
    ['set', "VERB", [], [], {
        'Participle': 'set'
    },],
    ['sew', "VERB", [], [], {
        'Participle': 'sewn'
    },],
    ['shake', "VERB", [], [], {
        'Participle': 'shaken'
    },],
    ['shave', "VERB", [], [], {
        'Participle': 'shaved'
    },],
    ['shut', "VERB", [], [], {
        'Participle': 'shut'
    },],
    ['seat', "VERB", [], [], {
        'Participle': 'sat'
    },],
    ['slay', "VERB", [], [], {
        'Participle': 'slain'
    },],
    ['sleep', "VERB", [], [], {
        'Participle': 'slept'
    },],
    ['sneak', "VERB", [], [], {
        'Participle': 'snuck'
    },],
    ['speed', "VERB", [], [], {
        'Participle': 'sped'
    },],
    ['spend', "VERB", [], [], {
        'Participle': 'spent'
    },],
    ['spit', "VERB", [], [], {
        'Participle': 'spat'
    },],
    ['split', "VERB", [], [], {
        'Participle': 'split'
    },],
    ['spring', "VERB", [], [], {
        'Participle': 'sprung'
    },],
    ['stink', "VERB", [], [], {
        'Participle': 'stunk',
        'PastTense': 'stunk'
    },],
    ['strew', "VERB", [], [], {
        'Participle': 'strewn'
    },],
    ['sware', "VERB", [], [], {
        'Participle': 'sworn'
    },],
    ['sweep', "VERB", [], [], {
        'Participle': 'swept'
    },],
    ['thrive', "VERB", [], [], {
        'Participle': 'thrived'
    },],
    ['undergo', "VERB", [], [], {
        'Participle': 'undergone'
    },],
    ['upset', "VERB", [], [], {
        'Participle': 'upset'
    },],
    ['weave', "VERB", [], [], {
        'Participle': 'woven'
    },],
    ['weep', "VERB", [], [], {
        'Participle': 'wept'
    },],
    ['wind', "VERB", [], [], {
        'Participle': 'wound'
    },],
    ['wring', "VERB", [], [], {
        'Participle': 'wrung'
    },],
]