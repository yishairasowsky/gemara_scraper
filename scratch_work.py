import re
import sys
import requests

def get_url(masechta,daf,amud,url_type,positive_index=None):
	assert(url_type in {'text','links'})
	if url_type == 'text':
		return f'http://www.sefaria.org/api/texts/{masechta}.{daf}{amud}'
	if url_type == 'links':
		return f'http://www.sefaria.org/api/links/{masechta}.{daf}{amud}.{positive_index}'

def get_json(url):
	return requests.get(url).json()

def select_gemara_data(gemara_json):
	title = gemara_json['heRef']
	hebrew_text = gemara_json['he']
	num_segments = len(hebrew_text)
	return title, hebrew_text, num_segments

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def is_wanted(commentary_choice, comment_title, comment_type):
  is_sought = None
  is_current = None  
  if comment_type == 'Mishneh Torah':
    is_sought = commentary_choice == 'Mishneh Torah'
    is_current = comment_title.startswith("Mishneh Torah")
  else:
    is_sought = commentary_choice != 'Mishneh Torah'
    is_current = f"{commentary_choice} on {masechta}" in comment_title
  return is_sought and is_current

# daf = 99
daf = 36
amud = 'a'
# masechta = 'Pesachim'
masechta = 'Yevamot'

text = ''
# segments_limit = 5
segments_limit = None

wanted_commentaries = {
    'Rashi':'רש"י',
    'Rashbam':'רשב"ם',
    'Tosafot':"תוס'",
    'Chidushei Halachot':'מהרש"א',
    # 'Rashba':'רשב"א',
    # 'Mishneh Torah':'רמב"ם'
		}

gemara_url = get_url(masechta,daf,amud,'text')
gemara_json = get_json(gemara_url)
title, hebrew_text, num_segments = select_gemara_data(gemara_json)

text += title + '\n'
for section_index in range(num_segments)[:segments_limit]:
	positive_index = section_index + 1 # Commentaries index first segment as 1, not 0.
	gemara_segment = hebrew_text[section_index]

	text += gemara_segment + '\n'
	links_url = get_url(masechta,daf,amud,'links',positive_index)
	links_json = get_json(links_url)

	for wanted_commentary,commentary_nickname in wanted_commentaries.items():
		for link in links_json:
			comment_title = link['index_title']
			if is_wanted(wanted_commentary, comment_title,'Mishneh Torah') or is_wanted(wanted_commentary,comment_title,'mefaresh'):
				comment = link['he']
				if comment[-1] in {':','.',' '}:
					comment = comment[:-1]
				text += comment
				text += ' (' + commentary_nickname +  ').' + '\n'

text = cleanhtml(text)

with open('output.txt', 'w',encoding='utf-8') as file:  # Use file to refer to the file object
	file.write(text)