import os
import sys
import shutil

class RootDirectory:
	def __init__(self, path):
		self.rootPath = path

	def getDirectories(self):
		thatAreDirectories = lambda path: os.path.isdir(path)
		directories = self.getItems(thatAreDirectories)
		return directories

	def getFiles(self):
		thatAreFiles = lambda path: os.path.isfile(path)
		files = self.getItems(thatAreFiles)
		return files

	def getItems(self, criterion):
		items_found = []
		for file in os.listdir(self.rootPath):
			path = os.path.join(self.rootPath, file)
			if criterion(path):
				items_found.append(file)
		return items_found

class Log:
	revertFileName = "revert.txt"
	changes = []

	def addChange(self, source, target):
		self.changes.append([source, target])

	def createLogLine(self, change):
		source = change[0]
		target = change[1]
		logItem = source + ":" + target + "\n"
		return logItem

	def write(self):
		f = open(self.revertFileName, "w")
		for change in self.changes:
			line = self.createLogLine(change)
			f.write(line)
		f.close()

class DirectoryStructure:
	map = dict(
		Archives = ["zip", "rar", "7z", "tar", "gz", "bz2", "tgz"],
		Binaries = ["exe", "dll", "msi", "vsix", "xpi"],
		Books = ["epub", "mobi"],
		Documents = ["doc", "docx", "txt", "pdf", "xps", "dotx", "odt", "html"],
		Images = ["iso","mkv","mdf"],
		Movies = ["avi","mpg","mpeg","mov","mp4", "flv"],
		Music = ["mp3","wav", "ogg", "wma"],
		Pictures = ["jpg","png","jpeg", "tif", "gif"],
		Presentations=["ppt", "pptx"],
		Sourcecode = ["cs","css","cpp","h","c", "js", "php", "py", "java", "pyc", "xaml", "xml", "rb", "config"],
		Spreadsheets = ["csv","xlsx", "xls", "json"]
	)

	def __init__(self, directory):
		self.directory = directory

	def ensureDirectoryStructure(self):
		directories_expected = self.map
		directories_found = self.directory.getDirectories()
		for directory in directories_expected:
			if directory not in directories_found:
				self.createMissingDirectory(directory)

	def createMissingDirectory(self, directoryName):
		missingDirectory = os.path.join(self.directory.rootPath, directoryName)
		os.mkdir(missingDirectory)

class Blacklist:
	def __init__(self):
		self.list = ["py"]

	def contains(self, path):
		filename = os.path.split(path)[1]
		return self.isExecutingScript(filename) or self.isRevertFileName(filename) or self.isHasForbiddenExtension(filename)

	def isExecutingScript(self, filename):
		executingScript = os.path.split(sys.argv[0])[1]
		return filename == executingScript

	def isRevertFileName(self, filename):
		revertFileName = Log.revertFileName
		return filename == revertFileName

	def isHasForbiddenExtension(self, filename):
		return FileInfo(filename).extension() in self.list

class FolderCleanup:
	def __init__(self, directory):
		self.directory = RootDirectory(directory)
		self.structure = DirectoryStructure(self.directory)
		self.blacklist = Blacklist()
		self.log = Log()

	def cleanup(self):
		self.structure.ensureDirectoryStructure()
		self.arrangeFiles()
		self.log.write()

	def arrangeFiles(self):
		files = self.directory.getFiles()
		for file in files:
			if self.blacklist.contains(file):
				continue
			category = self.categorizeFile(file)
			if(category == "Unknown"):
				continue
			self.moveFileToCategory(file, category)

	def categorizeFile(self, file):
		extension = FileInfo(file).extension()
		category = self.identifyCategory(extension)
		return category

	def moveFileToCategory(self, file, category):
		directory = self.directory
		source = os.path.join(directory.rootPath, file)
		target = os.path.join(directory.rootPath, category)
		print("Moving " + source + " to " + target)
		try:
			shutil.move(source, target)
			self.log.addChange(source, target)
		except shutil.Error:
			print("File " + file + " already exists in target category " + category)

	def identifyCategory(self, extension):
		for folderName in self.structure.map:
			if extension in self.structure.map[folderName]:
				return folderName
		return "Unknown"

class FileInfo:
	def __init__(self, filename):
		self.filename = filename
	def extension(self):
		rawExtension = os.path.splitext(self.filename)[1]
		extension = rawExtension.lstrip(".").lower()
		return extension

class Program:
	def run(self):
		args = sys.argv
		path = self.identifyRootPath(args)
		# currentScript = self.identifyExecutingScript(args)
		cleanup  = FolderCleanup(path)
		cleanup.cleanup()

	def identifyRootPath(self, args):
		root = ""
		if len(args) > 1 and os.path.isdir(args[1]):
			root = args[1]
		else:
			root = os.getcwd()
		return root

	def identifyExecutingScript(self, args):
		return os.path.split(args[0])[1]

# Allows this file to be executed or to be loaded as a module, see
# http://docs.python.org/tutorial/modules.html#executing-modules-as-scripts
# for further reference
# This is required so that the unittests don't actually execute the program
# Using the following lines the program is only executed if this script is called directly
if __name__ == '__main__':
	Program().run()