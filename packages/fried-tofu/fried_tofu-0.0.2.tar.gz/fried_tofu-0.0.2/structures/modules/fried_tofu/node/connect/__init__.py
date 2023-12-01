




'''
	import fried_tofu.node.connect as connect_to_node
	[ r, c ] = connect_to_node.attractively (
		driver_port = "",
		loops = 3,
		delay = 2
	)
'''


from rethinkdb import RethinkDB

import botany.cycle as cycle
import botany.modules.exceptions.parse as parse_exception

class connection_exception (Exception):
	pass


def attractively (
	loops = 10,
	delay = 1,
	
	driver_port = None,
	host = "localhost",
	
	label = "connect",
	
	assert_cannot_connect = False
):
	if (driver_port == None):
		ports = climate.find ("ports")
		driver_port = ports ["driver"]

	connection_attempt = 1;
	def connect (* positionals, ** keywords):	
		nonlocal connection_attempt;
		print (
			f"{ label }: Attempt '{ connection_attempt }' to connect to rethink at: { host }:{ driver_port }", 	
		)
		
		connection_attempt += 1
		
		r = RethinkDB ()
		c = r.connect (
			host = host,
			port = driver_port
		)

		print (f'Connection to rethink at "{ host }:{ driver_port }" was established.');	

		return [ r, c ];
		
	connection_loop_exception_occurred = False
	try:
		connection = cycle.loops (
			connect, 
			cycle.presents ([]),
			
			loops = loops,
			delay = delay,
			
			records = 0
		)
		
	except Exception as E:
		if (assert_cannot_connect):
			connection_loop_exception_occurred = True
			
		else:
			parsed_exception = parse_exception.now (E)
			print ("connection loop exception:", str (E))		
			raise connection_exception (f'''
			
				"{ loops }" connection attempts were made,
				however a connection could not be established.
				
			''')
		
	if (assert_cannot_connect):
		assert (connection_loop_exception_occurred == True)
		return;
	
	return connection;
