import unittest
import os
from FolderCleanup import Log

class LogTests(unittest.TestCase):
	def setUp(self):
		self.cleanupLog = Log()
		self.cleanupLog.addChange("source", "target")

	def test_Should_log_an_item(self):
		cleanupLog = Log()
		cleanupLog.addChange("source", "target")
		source = cleanupLog.changes[0][0]
		target = cleanupLog.changes[0][1]
		self.assertEqual("source", source)
		self.assertEqual("target", target)

	def test_Should_create_log_item(self):
		change = self.cleanupLog.changes[0]
		line = self.cleanupLog.createLogLine(change)
		self.assertEqual("source:target\n", line)

	def test_01_Should_write_to_file(self):
		self.cleanupLog.write()
		fileExists = os.path.isfile(self.cleanupLog.revertFileName)
		self.assertTrue(fileExists)

	def test_02_Should_contain_changes(self):
		expectedLine = self.cleanupLog.createLogLine(self.cleanupLog.changes[0])
		line = open(self.cleanupLog.revertFileName, "r").readline()
		self.assertEqual(expectedLine, line)

	def tearDown_Remove_created_revert_file(self):
		file = self.cleanupLog.revertFileName
		if os.path.isfile(file):
			os.remove(file)

if __name__ == '__main__':
	unittest.main()