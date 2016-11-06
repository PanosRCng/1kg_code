#
#	Project class
#
#
#

try:
	import Config
	import io
except ImportError:
	print 'Project -- (!) module do not found '	
	exit()


class Project:

	def __init__(self, json_data):

		self.name = json_data['name']
		self.src_dir = json_data['src_dir']
		self.langs = json_data['langs']
		self.tags = json_data['tags']
		self.ignore_list = json_data['ignore_list']

		self.lines = 0
		self.lang_lines = {}


	def read(self, verbose=True):

		for lang in self.langs:
			lines = self.__getLines(lang, verbose)

			self.lang_lines[lang] = lines
			self.lines += lines


	def __getLines(self, lang, verbose):

		source_files = self.__getSource(lang)

		if verbose == True:
			self.__show_files(lang, source_files)

		lines = [io.countLines(filename) for filename in self.__getSource(lang)]
		return sum(lines)


	def __getSource(self, lang):

		source_files = io.getFiles( self.src_dir, Config.suffixes[lang] )
		return [source_file for source_file in source_files if not self.__isIgnored(source_file)]


	def __show_files(self, lang, source_files):

		print self.name, lang
		for source in source_files:
			print source
		print '\n\n'


	def __isIgnored(self, filename):

		for ignore in self.ignore_list:
			if ignore in filename:
				return True
		return False


