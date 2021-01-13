import re 
import requests

class DafManager:

	def __init__(self,masechta,first_daf,first_amud,daf_amount):

		self.masechta = masechta
		self.first_daf = first_daf
		self.first_amud = first_amud
		self.daf_amount = daf_amount


	def get_final_text(self):
		final_text = ''
		return final_text


	def get_next_amud(daf,amud):

		if amud=='a':
			return daf,'b'  
		if amud=='b':
			return daf+1,'a'


	def cleanhtml(raw_html):
		cleanr = re.compile('<.*?>')
		cleantext = re.sub(cleanr, '', raw_html)
		return cleantext

	def get_links_json(masechta,daf,amud,positive_index):
		links_url = f'http://www.sefaria.org/api/links/{masechta}.{daf}{amud}.{positive_index}'
		links_response = requests.get(links_url)
		links_json = links_response.json()
		return links_json