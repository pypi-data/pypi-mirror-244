

'''
	import botany.paths.directory.rsync as rsync
	rsync.process ({
		"from": "",
		"to": "",
		
		#
		#	if "no", return the process script, but don't run it
		#
		#	if "yes", start rsync
		#
		"start": "yes",
		
		#
		#	not implemented: "yes"
		#
		"ssh": "no"
	})
'''

'''
	import botany.paths.directory.rsync as rsync
	rsync_script_string = rsync.process ({
		"from": "",
		"to": "",
		
		#
		#	if "no", return the process script, but don't run it
		#
		#	if "yes", start rsync
		#
		"start": "no",
		
		#
		#	not implemented: "yes"
		#
		"ssh": "no"
	})
'''


rsync_path = "rsync"

import os

def process (shares):
	if ("start" in shares and shares ["start"] == "yes"):
		start = "yes"
	else:
		start = "no"

	assert ("from" in shares)
	assert ("to" in shares)

	from_dir = shares ["from"]
	to_dir = shares ["to"]

	'''
		--archive, -a            
			archive mode is -rlptgoD (no -A,-X,-U,-N,-H)
		
		--verbose, -v            
			increase verbosity
		
		--mkpath				
			make directories necessary
	'''
	activity = f'{ rsync_path } --mkpath --progress --delete -av "{ from_dir }/" "{ to_dir }"';
	
	if (start != "yes"):
		return activity
	
	os.system (activity)

	return;