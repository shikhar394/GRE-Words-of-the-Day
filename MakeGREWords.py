from bs4 import BeautifulSoup, NavigableString
import unidecode
import urllib3
try:
    import cPickle as pickle
except ImportError:  # python 3.x
    import pickle

Word_Source_Economist_link = "https://gre.economist.com/gre-advice/gre-vocabulary/which-words-study/most-common-gre-vocabulary-list-organized-difficulty"
Word_Mnemonic_link_template = "https://mnemonicdictionary.com/word/"
Dictionary_com_template = "http://www.dictionary.com/browse/"

http = urllib3.PoolManager()
Word_Source_Economist_Response = http.request('GET', Word_Source_Economist_link)

class LearnWords():
  def __init__(self):
    self.word_structure = {} #{Word:{"Definition:"....", "Sentence":"....", "Synonym":".....", "Mnemonic":"...."}}
    self.words = [] # List of 3 lists, each corresponding to a diffifculty level 
    self.word_source_object = BeautifulSoup(Word_Source_Economist_Response.data, "lxml")
    #self.

  def extract_words_from_economist(self, buildObjects = True): #Extracts stuff from Economist GRE website.
    all_words_division = self.word_source_object.findAll('div', attrs={'class':'article-body wysiwyg'})
    words_by_difficulty = []
    for div in all_words_division:
      word_division = div.find('h2')
      for words in word_division.next_siblings:
        word_extracted = extract_word(words)
        print(word_extracted)
        if word_extracted.split(' ')[0] == "Level":
          self.words.append(words_by_difficulty)
          words_by_difficulty = []
          continue
        if buildObjects == True: #False when only word lists are needed to be accessed.
          self.build_word_object(word_extracted)
        words_by_difficulty.append(word_extracted)
      #print(self.words)
    self.words.append(words_by_difficulty)

  def build_word_object(self, word):
    definitions, mnemonic_extracted = extract_definition_mnemonic(unidecode.unidecode(word))
    #print(definitions)
    sentences = extract_sentence(unidecode.unidecode(word))
    self.word_structure[word] = {"Definition":definitions, "Mnemonic": mnemonic_extracted, 
          "Sentences": sentences}
    #print(self.word_source_object)
    #print(self.word_structure)
      


    
def extract_definition_mnemonic(word):
  """
  Extracts definitions and mnemonics from mnemonicdictionary.com
  """
  Mnemonic_Page_Link = Word_Mnemonic_link_template + word
  Mnemonic_Page_Response = http.request('GET', Mnemonic_Page_Link)
  Page_object = BeautifulSoup(Mnemonic_Page_Response.data, "lxml")
  mnemonics = extract_mnemonic_helper(Page_object)
  definitions = extract_definition_synonym_helper(Page_object)
  #print(definitions, mnemonics)
  return definitions, mnemonics



def extract_mnemonic_helper(Page_object):
  all_mnemonic_divisions = Page_object.findAll('ul', attrs={'class':'list-group media-list media-list-stream mb-4'})
  top_mnemonics = []
  
  for div in all_mnemonic_divisions:
    for text_fields in div.findAll('div', attrs={'media-body-text'}):
      for text in text_fields.findAll('p'):
        if text.contents[0].strip().split(" ")[0] != "Powered":
          top_mnemonics.append(text.contents[0].strip())
  return top_mnemonics[:3]


def extract_sentence(word):
  """
  Extracts sentences from Dictionary.com
  """
  Dictionary_Page_Link = Dictionary_com_template + word
  Dictionary_Page_Response = http.request('GET', Dictionary_Page_Link)
  Page_object = BeautifulSoup(Dictionary_Page_Response.data, "lxml")
  sentences = extract_sentence_helper(Page_object)
  #print(sentences)
  return sentences


def extract_sentence_helper(Page_object):
  all_sentence_divisions = Page_object.findAll('h4', attrs={'class':'css-it69we e15kc6du5'})
  top_sentences = []

  for div in all_sentence_divisions:
    top_sentences.append(div.get_text())

  return top_sentences[:3]


def extract_word(bs4_words):
  try:
    word_extracted = bs4_words.contents[0].get_text()
  except:
    word_extracted = bs4_words.contents[0].split(',')[0].split(':')[0]
  #print("Word extracted: ", word_extracted)
  return word_extracted


def extract_definition_synonym_helper(Page_object):
  all_word_divisions = Page_object.findAll('div', attrs={'style':'padding-bottom:0px;'})
  synonyms = [] #TODO
  definitions_list = [] #TODO Multiple definitions support.
  for div in all_word_divisions:
    for defintions in div.contents:
      if isinstance(defintions, NavigableString) and defintions.strip() != '':
        return [defintions.strip()]


def Make_WordLists():
  Object1 = LearnWords()
  Object1.extract_words_from_economist(False)
  #print(Object1.words)
  word_list1 = open("WordsEasy.txt", 'w')
  word_list2 = open("WordsMedium.txt", 'w')
  word_list3 = open("WordsHard.txt", 'w')
  word_lists = [word_list1, word_list2, word_list3]
  for wordlist in range(0, len(Object1.words)):
    cur_file = word_lists[wordlist]
    for word in Object1.words[wordlist]:
      cur_file.write(word+'\n')
    cur_file.close()

def Make_WordObjects():
  Object1 = LearnWords()
  Object1.extract_words_from_economist()
  with open("Words.json", 'wb') as fb:
    pickle.dump(Object1.word_structure, fb)


if __name__ == "__main__":
  Make_WordObjects()

    

