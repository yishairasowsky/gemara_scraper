
from tqdm import tqdm
from DafManager import DafManager

masechta = 'Pesachim'
first_daf=50
first_amud='a'
daf_amount = 0.5

dm = DafManager(masechta,first_daf,first_amud,daf_amount)

commentary_names = ['Rashi','Rashbam','Tosafot','Rashba','Maharsha']

daf = first_daf
amud = first_amud
dapim_covered = 0

text = ''

while dapim_covered < daf_amount:
  
  gemara_json = dm.get_gemara_json(masechta,daf,amud)

  title = gemara_json['heRef']
  hebrew_text = gemara_json['he']
  num_segments = len(hebrew_text)

  commentary_json = {}

  comments = {}

  text += title + '\n'

  print(f"Fetching Daf {daf}{amud}")

  for section_index in tqdm(range(num_segments)[:]):

    text += hebrew_text[section_index] + '\n'

    positive_index = section_index + 1

    links_json = get_links_json(masechta,daf,amud,positive_index)
    pass
    rambam_objects = [
      (
        json_object['he'],
        json_object['sourceHeRef'],
        )
      for json_object in links_json 
      if json_object['ref'].startswith('Mishneh Torah')
      ]

    for commentary_choice in commentary_choices:
      try:
        pass
      # comments[commentary_choice] = [
        # (
        #   json_object['he'],
        #   json_object['sourceHeRef'],
        #   )
        # for json_object in links_json 
        # if json_object['ref'].startswith('Mishneh Torah')
        ]

        # commentary_url = f'http://www.sefaria.org/api/texts/{commentary_choice}_on_{masechta}.{daf}{amud}.{commentary_index}'
        # commentary_response = requests.get(commentary_url)
        # commentary_json = commentary_response.json()
        # comment_lst = commentary_json['he']

      except:
        # continue
        pass

      commentary_name = commentary_json['heCommentator']


      if comment_lst:
        text += '\n'
        text += commentary_name

      for comment in comment_lst:
        if comment:
          text += '\n'
          if comment[-1]==':':
            comment = comment[:-1]
          text += comment
          text += ' (' + commentary_name[:5] + ').'
          pass

    if rambam_objects:
      for rambam in rambam_objects:
        
        din = rambam[0]
        if din[-1]==':':
          din = din[:-1]
        
        src = rambam[1]
        
        text += '\n'
        text += 'כתב הרמב"ם: '
        
        text += din
        text += ' '
        text += '(' + src[17:] + ').'
        pass

        text += '\n'

  daf,amud = next_amud(daf,amud)
  dapim_covered += 0.5

text = cleanhtml(text)

with open('output.txt', 'w', encoding='utf-8') as file:
  file.write(text)

pass