


'''
import fried_tofu.node.cannot_connect as fried_tofu_cannot_connect
fried_tofu_cannot_connect.attractively (
	loops = 3,
	driver_port = driver_port
)
'''

import fried_tofu.node.connect as connect

def attractively (
	loops = 5,
	driver_port = None
):
	int (driver_port)

	connect.attractively (
		label = "asserting that can't connect",
		driver_port = driver_port,
		loops = loops,
		assert_cannot_connect = True
	)






