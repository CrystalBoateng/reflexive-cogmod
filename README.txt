reflexive-cogmod    version 0.03    2019


LONG-TERM PROJECT GOALS
--------------------
1. Process natural language to facilitate a UI. Persist new information to disk.
2. Emulate one layer of reflexivity by compressing or modelling info about the most frequently-referenced topics and neural pathways.
3. Emulate modelling of self and information sources, by stacking multiple layers of the reflexive models.
4? Be able to write and optimize real python code.
5? Modify own Python code during runtime.
6? Track and optimize performance and resource usage.


SHORT-TERM PROJECT GOALS
--------------------
Load newly-learned words/topics into the current runtime, without restarting the program.
Categorize words and store words for fast retrieval. Use POS tags to write grammatical english.
Centralize error reporting and speaking tasks.
Look up words/topics using something like a neural network. Hard-code decay patterns and other basic network behaviors.
Work on pattern compression (for writing grammatical english) and nerual pathway compression (for the network).


DEPENDENCIES/SYSTEM REQUIREMENTS
--------------------
Python 3.5.4 or higher (https://www.python.org/downloads/)
NumPy+mkl (https://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy)
scikit-learn (http://scikit-learn.org/stable/)
spaCy 2.0.2 (https://spacy.io/usage/)
textacy (https://textacy.readthedocs.io/en/latest/index.html)
DB Browser for SQLite (http://sqlitebrowser.org/) is helpful for manually managing the database, but is not required.

I'm using WinPython 3.5.4Qt5 IDLEX on Windows, but other IDEs should work as well. 

A working internet connection is required for this program to access webpages to read. Using an online proxy server or running this program in a cloud computing environment may cause complications or prevent the page's content from downloading.


CHANGE LOG
--------------------
2018-05-20 Moved persisted data from Python lists (in various locations), to a SQLite databse in learned_data. But kept known_corpus_tokenized.py as a Python list for now. 
See git commits for more detailed updates.


LICENSING
--------------------
This code is provided under a GNU General Public License (GPLv3), and is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. Additionally, each of the dependencies listed above, has its own licensing agreement; none of the dependencies listed above, come packaged with this code. See the GNU General Public License for more details.


OTHER CREDITS:
--------------------
Conjugation column names and the conjugations for the following verbs, come from 'compromise', an open-source NLP JavaScript project published under a copyleft MIT license. The license and source codeare available at: github.com/nlp-compromise/compromise or at http://compromise.cool The license is also included in this repo (as required), in the folder /learned_data/backup_reference.
	'take','can','free','puke','arise','babysit','be','is','beat','begin','ban','bet','bite','bleed','breed','bring','broadcast','build','buy','choose','cost','deal','die','dig','draw','drink','drive','eat','fall','feed','feel','fight','find','fly','blow','forbid','edit','forget','forgive','freeze','get','give','go','hang','have','hear','hide','hold','hurt','lay','lead','leave','lie','light','lose','make','mean','meet','pay','read','ring','rise','run','say','see','sell','shine','shoot','show','sing','sink','sit','slide','speak','spin','stand','steal','stick','sting','stream','strike','swear','swim','swing','teach','tear','tell','think','understand','wake','wear','win','withdraw','write','tie','ski','boil','miss','act','compete','being','imply','ice','develop','wait','aim','spill','drop','log','rub','smash','egg','suit','age','shed','break','catch','do','bind','spread','become','bend','brake','burn','burst','cling','come','creep','cut','dive','dream','flee','fling','got','grow','hit','keep','kneel','know','leap','lend','loose','prove','put','quit','ride','seek','send','set','sew','shake','shave','shut','seat','slay','sleep','sneak','speed','spend','spit','split','spring','stink','strew','sware','sweep','thrive','undergo','upset','weave','weep','wind','wring'.

ASCII art by Jon McGorrill from http://www.chris.com/ascii/index.php?art=art%20and%20design/borders
