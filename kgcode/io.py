#
#
#	io module
#
#


try:
	import json
	import os
except ImportError:
	print 'io -- (!) module do not found '	
	exit()


# loads a json file
def load_json(filename):
	with open(filename) as json_file:
		return json.load(json_file)


# returns all filenames (paths) in the given directory with the specified suffixes
def getFiles(directory, suffixes):

	filenames = []

	for root, dirs, files in os.walk(directory):
		for filename in files:

			if os.path.splitext(filename)[1] in suffixes:
				filepath = os.path.join(root, filename)
				filenames.append( filepath )

	return filenames


# returns the number of lines in the specified file
def countLines(filename):
	return sum(1 for line in open(filename))













