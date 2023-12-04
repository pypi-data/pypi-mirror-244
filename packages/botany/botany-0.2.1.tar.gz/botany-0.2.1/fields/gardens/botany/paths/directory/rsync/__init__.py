

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
		"ssh": "no",
		
		"sense": "yes"
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
import botany.paths.directory.sense as sense
import botany.cadence.filter as cadence_filter	

rsync_path = "rsync"

import os

def process (shares_param):
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
		CF = cadence_filter.start (every = 1)
		def cadence_action (is_delayed, parameters):
			synchronize (shares_param)
	
		def sense_event (* pos, ** keys):
			CF.attempt (
				action = cadence_action,
				parameters = []
			)	

		sense.changes (
			directory = shares_param ["from"],
			action = sense_event
		)
		
		synchronize (shares_param)
	else:
		synchronize (shares_param)

	return;