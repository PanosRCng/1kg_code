#
#	valuator module
#
#
#


def valueLangs(langs_lines, langs_freqs, projects_lines, projects_number):

	langs_weights = {}	

	for lang in langs_lines:
		langs_weights[lang] = value_lang(langs_lines[lang], langs_freqs[lang], projects_lines, projects_number)

	return langs_weights



def valueTags(tags_loads, tags_freqs, projects_lines, projects_number):

	tags_weights = {}

	for tag in tags_loads:
		tags_weights[tag] = value_tag(tags_loads[tag], tags_freqs[tag], projects_lines, projects_number)

	return tags_weights	



def value_lang(lang_load, lang_freq, projects_lines, projects_number):

	load = ( lang_load / float(projects_lines) ) * 100
	freq = ( lang_freq / float(projects_number) ) * 100

	return calc_lang_weight(freq, load)



def value_tag(tag_load, tag_freq, projects_lines, projects_number):

	load = ( tag_load / float(projects_lines) ) * 100
	freq = ( tag_freq / float(projects_number) ) * 100

	return calc_tag_weight(freq, load)



def calc_lang_weight(freq, load):
	return (0.5 * freq) + (0.5 * load) 



def calc_tag_weight(freq, load):
	return (0.5 * freq) + (0.5 * load) 



