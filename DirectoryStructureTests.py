import os
from FolderCleanup import RootDirectory
from FolderCleanup import DirectoryStructure
import unittest

class DirectoryStructureTests(unittest.TestCase):

    testDirectory = "testDirectory"

    def removeFolder(self, path):
        if os.path.isdir(path):
           os.rmdir(path)

    def setUp(self):
        self.removeFolder(self.testDirectory)

    def test_Should_not_create_folder_if_it_already_exists(self):
        root = RootDirectory(".")
        structure = DirectoryStructure(root)
        structure.map = dict( testDirectory = [])
        structure.ensureDirectoryStructure()
        self.assertTrue(os.path.isdir(self.testDirectory))

    def tearDown(self):
        self.removeFolder(self.testDirectory)

if __name__ == '__main__':
    unittest.main()
