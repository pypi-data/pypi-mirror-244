

'''
	import botany.paths.directory.rsync.remote as rsync_to_remote
	rsync_to_remote.splendidly ({
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
		"ssh": "no",
		
		"sense": "yes"
	})
'''

import botany.paths.directory.sense as sense
	
rsync_path = "rsync"

import os

def splendidly (shares_param):
	def synchronize (shares):
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

	

	if ("sense" in shares_param and shares_param ["sense"] == "yes"):
		def action (* pos, ** keys):
			synchronize (shares_param)

		sense.changes (
			directory = shares_param ["from"],
			action = action
		)
	else:
		synchronize (shares_param)

	return;