

'''
	priorities:
		import pathlib
		from os.path import dirname, join, normpath
		this_folder = pathlib.Path (__file__).parent.resolve ()
		
		import fried_tofu.node.process_IDs.remove as remove_process_IDs
		remove_process_IDs.attractively (
			glob_string = str (normpath (join (this_folder, "assurances"))) + "**/tofu.process_ID"
		)
'''

import glob
import os

def attractively (
	glob_string
):
	paths_found = glob.glob (glob_string)

	for path_found in paths_found:
		if (os.path.isfile (path_found)):
			os.remove (path_found)

	return;