import os
import json


# set any suffixes here
suffixes = { '.py' : 'python',
	     '.cpp' : 'c++',
	     '.h' : 'c++',
	     '.java' : 'java', 
	     '.php' : 'php',
	     '.js' : 'javascript',
	     '.css' : 'css'}


# set the json input file
input_file = 'input.json'

# set the range for min-max normalization
pref_min = 0.5
pref_max = 1.0


def main():

	projects = getProjects(input_file)

	langs_stats = {}
	ufs = {}

	for project in projects:

		langs_lines = countLines(project)

		for lang in langs_lines:

			if lang in langs_stats.keys():
				ufs[lang] = ufs[lang] + 1
				langs_stats[lang] += langs_lines[lang]
			else:
				ufs[lang] = float(1)
				langs_stats[lang] = float(langs_lines[lang])

	print langs_stats

	langs_stats = weighted_by_usage_frequency(langs_stats, ufs)

	langs_stats = min_max_normalization(langs_stats, pref_min, pref_max)

	print langs_stats


def getProjects(input_file):
  
	with open(input_file) as json_file:

		input_data = json.load(json_file)

		return input_data['projects']


def isIgnored(ignore_list, filename):

	for ignore in ignore_list:
		if ignore in filename:
			return True
	return False


def countLines(project):

	lang_files = {}
	langs_lines = {}

	for lang in project['langs']:
		lang_files[lang] = list()
		langs_lines[lang] = 0		

	for root, dirs, files in os.walk(project['src_dir']):
		for filename in files:

			if os.path.splitext(filename)[1] in suffixes.keys():

				lang = suffixes[os.path.splitext(filename)[1]]

				filepath = os.path.join(root, filename)

				if (lang in project['langs']) and (not isIgnored(project['ignore_list'], filepath) ):
					lang_files[lang].append(filepath)

	for lang in project['langs']:
		
		files = lang_files[lang]

		for filename in files:
	
			langs_lines[lang] += sum(1 for line in open(filename))


	return langs_lines


def weighted_by_usage_frequency(langs_stats, ufs):

	for lang in langs_stats:
		langs_stats[lang] = (langs_stats[lang] * ufs[lang])

	return langs_stats


def min_max_normalization(langs_stats, pref_min, pref_max):

	max_lines = langs_stats[ max(langs_stats, key=langs_stats.get) ]
	min_lines = langs_stats[ min(langs_stats, key=langs_stats.get) ]

	for lang in langs_stats:

		langs_stats[lang] = ( (langs_stats[lang] - min_lines) / (max_lines - min_lines) ) * ( pref_max - pref_min ) + pref_min 

	return langs_stats





if __name__ == "__main__":

	main()


