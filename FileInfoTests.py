import unittest
from FolderCleanup import FileInfo

class FileInfoTests(unittest.TestCase):
	def test_File_Should_have_an_extension(self):
		filename = "C:\Python31\python.exe"
		info = FileInfo(filename)
		actual = info.extension()
		expected = "exe"
		self.assertEqual(actual, expected)

	def test_Should_get_lowercase_extension(self):
		filename = "C:\Python31\PYTHON.EXE"
		info = FileInfo(filename)
		actual = info.extension()
		expected = "exe"
		self.assertEqual(actual, expected)

if __name__ == '__main__':
	unittest.main()
