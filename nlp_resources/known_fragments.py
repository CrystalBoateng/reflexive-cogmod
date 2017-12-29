# This is a rough sketch. There will eventually be a need to store sentences and sentence fragments (and other larger structures), when they have more semantic meaning than the sum of their tokens alone (e.g. idioms). However I have no idea how to integrate this into the larger environment as of yet.

fragmentsKnown = [
	#[Fragment or sentence (unconjugated), [Conditions], ], #prose explanation of the conditions
	["Speak of the devil and he shall appear.", [], ], #when a source was mentioned in the last two inputs/outputs, and then new information is obtained from that source.
	["“o shit waddup!", [(readingLoop_input.lower()).find("here comes dat boi" > 0], ], #when user's input contains "here comes dat boi"
	["kill two birds with one stone.", [], ], #when an action causes two other actions
]