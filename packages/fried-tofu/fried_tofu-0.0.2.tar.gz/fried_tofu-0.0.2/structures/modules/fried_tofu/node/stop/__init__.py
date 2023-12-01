
'''
	import fried_tofu.node.stop as node_stop
	node_stop.attractively (
		process_ID_file_path,
		driver_port
	)
		
'''

'''
	notes:
		rethinkdb removes the pid file when stopped
		like this.
'''

import fried_tofu.node.cannot_connect as node_cannot_connect

import psutil

def attractively (
	process_ID_file_path,
	driver_port
):
	print ()
	print ("[stopping rethink node]")

	FP = open (process_ID_file_path)
	P_ID = int (FP.read ().strip ())

	p = psutil.Process (P_ID)
	p.terminate ()
	
	node_cannot_connect.attractively (
		loops = 2,
		driver_port = driver_port
	)
	
	return;