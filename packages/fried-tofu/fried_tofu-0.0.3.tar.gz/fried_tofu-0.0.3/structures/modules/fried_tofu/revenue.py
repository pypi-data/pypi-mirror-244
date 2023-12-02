

'''
	import fried_tofu.revenue as fried_tofu_revenue
	fried_tofu_revenue.obtain ()
'''


import pathlib
from os.path import dirname, join, normpath
this_folder = pathlib.Path (__file__).parent.resolve ()

import revenue


def obtain ():
	revenue.start ({
		"directory": str (this_folder),
		"extension": ".r.HTML",
		"relative path": str (this_folder)
	})