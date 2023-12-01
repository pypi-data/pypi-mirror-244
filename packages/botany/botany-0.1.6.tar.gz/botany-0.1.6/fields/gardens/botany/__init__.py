

'''
	botany
'''

import json
import pathlib
from os.path import dirname, join, normpath

'''
	import botany
	botany.show ({})
	botany.show ("", {})
'''
def show (* positionals):
	if (
		type (positionals [0]) == dict and
		len (positionals) == 1
	):
		print (json.dumps (positionals [0], indent = 4))
		return;
		
	if (
		type (positionals [0]) == str and
		type (positionals [1]) == dict and
		len (positionals) == 2
	):
		print (positionals [0], json.dumps (positionals [1], indent = 4))
		return;
		
		
	print ("botany.show:", positionals)
	

'''
	import botany
	botany.this_directory_path ()
	botany.this_directory_path ("a_path/after/the_this_directory")
'''
def this_directory_path (* positionals):
	this_directory_trail = pathlib.Path (__file__).parent.resolve ();

	if (
		type (positionals [0]) == str and
		len (positionals) == 1
	):
		return str (normpath (join (this_directory_trail, positionals [0])))

	return str (this_directory_trail)

