

'''
	import pathlib
	import fried_tofu.node.start as start_node
	ly = start_node.attractively (
		proxy = "yes",
		server_name = "node-1",
		ports = {
			"driver": 0,
			"cluster": 0,
			"http": 0	
		},
		process = {
			"cwd": pathlib.Path (__file__).parent.resolve ()
		},
		rethink_params = [
			f"--daemon",
			f"--pid-file {}"
		]
	)
'''

import shlex
import subprocess
import time
import datetime
	
import fried_tofu.node.start.assertions as node_start_assertions
import fried_tofu.node.connect as connect_to_node
	
def attractively (
	proxy = "no",
	
	rethink_params = [],
	ports = {},
	
	records = 1,
	
	** keywords
):
	print ()
	print ("[starting rethink node]")

	#
	process_keys = keywords ["process"]

	#
	driver_port = str (ports ["driver"])
	cluster_port = str (ports ["cluster"])
	http_port = str (ports ["http"])
	
	node_string = "rethinkdb"
	if (proxy == "yes"):
		#
		#	proxies can't have names maybe.
		#
		node_string += " proxy"
	
	'''
	#timestamp = datetime.datetime ().timestamp()
	timestamp = ''.join (str (datetime.datetime.now().timestamp()).split ('.'))
	print ('timestamp:', timestamp)
	f"--server-tag { timestamp }",
	'''
	
	script = " ".join ([
		node_string,
		
		f"--driver-port { driver_port }",
		f"--cluster-port { cluster_port }",
		f"--http-port { http_port }",
		
		* rethink_params
	])
	
	print ("script:", script)
	
	process = subprocess.Popen (
		shlex.split (script),
		** process_keys
	)
	
	time.sleep (1)
	
	[ r, c ] = connect_to_node.attractively (
		driver_port = driver_port,
		loops = 5,
		delay = 1
	)
	
	'''
	assert (r.db('rethinkdb').table('server_config').count ().run (c) == 1)
	server_config = r.db('rethinkdb').table('server_config').run (c)
	for config in server_config:
		assert (timestamp in config ["tags"]), [
			config,
			timestamp
		]
	'''
	
	'''
	server_data = c.server ();
	print ("server_data:", server_data)
	assert (server_data ["name"] == server_name)
	'''
	
	node_start_assertions.check (r, c)		
	c.close ()

	return;