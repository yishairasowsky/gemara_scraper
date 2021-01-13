import unittest

from DafManager import DafManager

class KnownValues(unittest.TestCase):
    

    def test_get_text_json_for_dapim(self):

        json = DafManager.get_text_json(masechta='Zevachim',daf=95,amud='b')
        result = json['text'][0][:29]
        expected = "The Gemara rejects a solution"
        self.assertEqual(expected,result)


    def test_get_final_text_for_dapim(self):

        result = DafManager.get_final_text(3)
        expected = ""
        self.assertEqual(expected,result)
         

    def test_get_links_json_for_dapim(self):

        json = DafManager.get_links_json(masechta='Nedarim',daf=33,amud='a',positive_index=3)
        result = json[0]['index_title']
        expected = "Rosh on Nedarim"
        self.assertEqual(expected,result)
         

    def test_get_next_amud_for_dapim(self):

        result = DafManager.get_next_amud(95,'b')
        expected = 96,'a'
        self.assertEqual(expected,result)

        result = DafManager.get_next_amud(115,'a')
        expected = 115,'b'
        self.assertEqual(expected,result)


if __name__ == '__main__':
    unittest.main()