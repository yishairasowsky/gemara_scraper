import re
import requests

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

text = ''

masechta = 'Pesachim'
daf = 97
amud = 'b'

commentary_choices = ['Rashi','Tosafot']

gemara_url = f'http://www.sefaria.org/api/texts/{masechta}.{daf}{amud}'
gemara_response = requests.get(gemara_url)

title = gemara_response.json()['heRef']
hebrew_text = gemara_response.json()['he']
num_segments = len(hebrew_text)

text += title

for section_index in range(num_segments)[-1:]:

  positive_index = section_index + 1

  text += '\n'
  text += '\n'
  text += hebrew_text[section_index]

  commentary_index = section_index + 1
  for commentary_choice in commentary_choices:

    commentary_url = f'http://www.sefaria.org/api/texts/{commentary_choice}_on_{masechta}.{daf}{amud}.{commentary_index}'
    commentary_response = requests.get(commentary_url)

    comment_lst = commentary_response.json()['he']
    commentary_name = commentary_response.json()['heCommentator']

    text += '\n'
    text += '\n'

    if comment_lst:
      text += commentary_name

    for comment in comment_lst:
      if comment:
        text += '\n'
        text += comment

text = cleanhtml(text)

with open('output.txt', 'w', encoding='utf-8') as file:  # Use file to refer to the file object
  file.write(text)

pass