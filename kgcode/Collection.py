#
#	Collection class
#
#
#



try:
	import io
	import valuator
	from Project import Project
except ImportError:
	print 'Collection -- (!) module do not found '	
	exit()


class Collection:

	def __init__(self, json_file):

		self.projects = self.__load_projects(json_file)
		self.projects_number = len(self.projects)
		self.langs = self.__langs()
		self.tags = self.__tags()

		self.projects_lines = 0


	def read(self):
		for project in self.projects:
			project.read(verbose=False)

		self.projects_lines = self.__count_lines()


	def skills(self):

		[langs_weights, tags_weights] = self.__value()

		skills = langs_weights
		for tag in tags_weights:		
			skills[tag] = tags_weights[tag]

		return skills


	def conjunctions(self):

		conjunctions = {}

		lang_conjunctions = {}
		for lang in self.langs:
			lang_conjunctions[lang] = self.__getLangConjunctions(lang)

		tag_conjunctions = {}
		for tag in self.tags:
			tag_conjunctions[tag] = self.__getTagConjunctions(tag)
 
		for lang in lang_conjunctions:
			conjunctions[lang] = lang_conjunctions[lang]

		for tag in tag_conjunctions:
			conjunctions[tag] = tag_conjunctions[tag]

		return conjunctions



	def __getLangConjunctions(self, lang):

		conjunctions = []

		for project in self.projects:

			if lang in project.langs:
				conjunctions += project.langs
				conjunctions += project.tags

			conjunctions = list(set(conjunctions))

			if lang in conjunctions:
				conjunctions.remove(lang)

		return conjunctions


	def __getTagConjunctions(self, tag):

		conjunctions = []

		for project in self.projects:

			if tag in project.tags:
				conjunctions += project.langs
				conjunctions += project.tags

			conjunctions = list(set(conjunctions))

			if tag in conjunctions:
				conjunctions.remove(tag)

		return conjunctions


	def __langs(self):

		langs = []
		for project in self.projects:
			langs += project.langs

		return set(langs)


	def __tags(self):

		tags = []
		for project in self.projects:
			tags += project.tags

		return set(tags)


	def __value(self):

		langs_weights = valuator.valueLangs(self.__langsLines(), self.__langsFreqs(), self.projects_lines, self.projects_number)
		tags_weights = valuator.valueTags(self.__tagsLoads(), self.__tagsFreqs(), self.projects_lines, self.projects_number)

		return [langs_weights, tags_weights]


	def __langsLines(self):

		langs_lines = {}

		for project in self.projects:
			for lang in project.langs:
				if lang in langs_lines:
					langs_lines[lang] += project.lang_lines[lang]
				else:
					langs_lines[lang] = project.lang_lines[lang]

		return langs_lines


	def __langsFreqs(self):

		langs_freqs = {}

		for project in self.projects:
			for lang in project.langs:
				if lang in langs_freqs:
					langs_freqs[lang] += 1
				else:
					langs_freqs[lang] = 1

		return langs_freqs


	def __tagsLoads(self):

		tags_loads = {}

		for project in self.projects:
			for tag in project.tags:
				if tag in tags_loads:
					tags_loads[tag] += (project.lines * project.tags[tag])
				else:
					tags_loads[tag] = (project.lines * project.tags[tag])

		return tags_loads


	def __tagsFreqs(self):

		tags_freqs = {}

		for project in self.projects:
			for tag in project.tags:
				if tag in tags_freqs:
					tags_freqs[tag] += 1
				else:
					tags_freqs[tag] = 1

		return tags_freqs


	def __count_lines(self):
		lines = [project.lines for project in self.projects]
		return sum(lines)


	# loads the projects' values from the json file
	# return a list with instances of the Project class
	def __load_projects(self, input_file):

		input_data = io.load_json(input_file)

		projects = []	
		for p_data in input_data['projects']:
			projects.append( Project( p_data ) )
		return projects




