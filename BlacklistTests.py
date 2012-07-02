import os

import unittest
import sys
from FolderCleanup import Blacklist
from FolderCleanup import Log

class BlacklistTests(unittest.TestCase):
	def test_Blacklist_should_contain_executing_script(self):
		currentScript = os.path.split(sys.argv[0])[1]
		blacklist = Blacklist()
		self.assertTrue(blacklist.contains(currentScript))

	def test_Blacklist_should_not_contain_a_random_file(self):
		randomFile = "text.txt"
		blacklist = Blacklist()
		self.assertFalse(blacklist.contains(randomFile))

	def test_Blacklist_should_contain_revert_file(self):
		revertFile = Log.revertFileName
		blacklist = Blacklist()
		self.assertTrue(blacklist.contains(revertFile))

	def test_Blacklist_should_contain_any_python_script(self):
		pythonFile = "xyz.py"
		blacklist = Blacklist()
		self.assertTrue(blacklist.contains(pythonFile))

if __name__ == '__main__':
	unittest.main()
