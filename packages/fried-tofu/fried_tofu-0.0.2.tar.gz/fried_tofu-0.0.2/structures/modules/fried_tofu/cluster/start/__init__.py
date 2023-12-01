

'''
	# for status checks

	import pathlib
	from os.path import dirname, join, normpath
	this_directory = pathlib.Path (__file__).parent.resolve ()	
	cluster_directory = normpath (join (this_directory, "tofu_cluster"))
	import fried_tofu.cluster.start as start_cluster
	ly = start_cluster.attractively (
		proxy = {
			"ports": []
		},
		nodes = [{
			"ports": []
		},{
			"ports": []
		},{
			"ports": []
		}]
	)
'''

'''	
	import fried_tofu.cluster.start as start_cluster
	ly = start_cluster.attractively (
		proxy = {
			"ports": []
		},
		nodes = [{
			"ports": []
		},{
			"ports": []
		},{
			"ports": []
		}]
	)
'''

'''
	rethinkdb proxy --join 127.0.0.1:29016 --daemon
	
	rethinkdb -o 1 --bind all --daemon
		# Listening for intracluster connections on port 29016
		# Listening for client driver connections on port 28016
		# Listening for administrative HTTP connections on port 8081
	
	rethinkdb -o 2 --join 127.0.0.1:29016 --daemon
	rethinkdb -o 3 --join 127.0.0.1:29016 --daemon
'''

'''
	"join" needs one of the hosts allowed with "--bind", etc.
	
		Listening on cluster addresses: 127.0.0.1, 192.168.0.11, ::1, fe80::b3d:4b55:4fab:7aa1%2
		Listening on driver addresses: 127.0.0.1, 192.168.0.11, ::1, fe80::b3d:4b55:4fab:7aa1%2
		Listening on http addresses: 127.0.0.1, 192.168.0.11, ::1, fe80::b3d:4b55:4fab:7aa1%2
'''

import pathlib
from os.path import dirname, join, normpath
import os

import botany
import botany.flow.demux_mux2 as demux_mux2

import fried_tofu.node.stop as node_stop
import fried_tofu.node.start as start_node



import inspect
import os

def retrieve_caller ():
	return os.path.abspath ((inspect.stack () [1]) [1])

def attractively (
	proxy = {
		"ports": []
	},
	nodes = [],
	
	#
	#	tofu_cluster in caller directory if not sent.
	#
	cluster_directory = "",
	process_ID_file_name = "tofu.pid"
):
	shutdown_list = []
	
	if (len (cluster_directory) == 0):
		cluster_directory = str (normpath (join (
			os.path.dirname (os.path.abspath ((inspect.stack () [1]) [1])), 
			"tofu_cluster"
		)))

	print ("cd", cluster_directory);

	node_tally = 1
	def start (parameters):
		nonlocal node_tally
		nonlocal cluster_directory

		node_path = str (normpath (join (cluster_directory, str (node_tally))))
		process_ID_file_path = str (normpath (join (node_path, process_ID_file_name)))
		os.makedirs (node_path, exist_ok = True)
		
		ports = parameters ["ports"]
		driver_port = ports [0]

		ly = start_node.attractively (
			proxy = "no",
			server_name = f"node-{ node_tally }",
			ports = {
				"driver": driver_port,
				"cluster": ports [1],
				"http": ports [2]	
			},
			process = {
				"cwd": node_path
			},
			rethink_params = [
				f"--daemon",
				f"--pid-file { process_ID_file_path }"
			]
		)
		
		shutdown_list.append ({
			"process_ID_file_path": process_ID_file_path,
			"driver_port": driver_port
		})
		
		node_tally += 1

	proceeds_statement = demux_mux2.start (
		start, 
		nodes
	)

	return;
















