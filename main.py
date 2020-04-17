import requests
from bs4 import BeautifulSoup, Comment
import en_core_web_sm
import random

def read_urls(urls):
  content_string = ''
  for page in urls:
    print(f'Scraping URL: {page}')
    # Synchronous request to page, and store returned markup
    scrape = requests.get(page).content

    # Parse the returned markup with BeautifulSoup's html5 parser
    soup = BeautifulSoup(scrape, "html5lib")
    
    # loop script tags and remove them
    for script_tag in soup.find_all('script'):
      script_tag.extract()

    # loop style tags and remove them
    for style_tag in soup.find_all('style'):
      style_tag.extract()

    # find all comments and remove them
    for comment in soup(text=lambda text: isinstance(text, Comment)):
      comment.extract()

    # Join all the scraped text content
    text = ''.join(soup.findAll(text=True))
    # Append to previously scraped text
    content_string += text

  return content_string

def get_tokens(corpus):
  # load the pretrained english model
  nlp = en_core_web_sm.load()
  # parse the corpus and return the processed data
  return nlp(corpus)

def get_word_list(tokens, part_of_speech):
  # extract a list of lemmas and capitalise them
  list_of_words = [
    word.lemma_.capitalize() # <-- update .text to .lemma_
    for word in tokens 
    if word.pos_ == part_of_speech 
    and not word.is_stop
    and not word.is_punct
  ]
  
  # make the list unique by casting it to a set
  unique_list = set(list_of_words)

  # cast it back to a set and return
  return list(unique_list)

# create a list of urls to scrape
# For illustration, I'm using my website 
# but replace with any urls of your choice
CORPUS = read_urls([
  'https://robbowen.digital/',
  'https://robbowen.digital/work',
  'https://robbowen.digital/about'
])

# parse the corpus and tokenize
TOKENS = get_tokens(CORPUS)

# extract a unique list of noun lemmas from the token list
nouns = get_word_list(TOKENS, "NOUN")

# extract a unique list of adjective lemmas from the token list
adjectives = get_word_list(TOKENS, "ADJ")

# create a random list of 500 nouns and adjective-noun combos
# cast to a set to make sure that we only get unique results
list_of_combos = set(
  [
    # String interpolation of an adjective and a noun...
    f'{random.choice(adjectives)} {random.choice(nouns)}' 
    # 50% of the time...
    if random.choice([True, False]) is True
    # else return a random noun
    else random.choice(nouns)
    # and repeat this 500 times
    for x in range(500)
  ]
)

# Write list of combinations to a text file
output_file = open("./output.txt", 'w')
for item in list_of_combos:
  output_file.write(f'{item}\r\n')