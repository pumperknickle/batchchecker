import re
import string
from DefinedNounsExtractor import toLemmas
from abbreviations import schwartz_hearst

rx = r"\b[A-Z](?=([&.]?))(?:\1[A-Za-z])*(?:\1[A-Z])\b"

# regex to match acronyms
def extractAllAcronyms(text):
  acronyms = [x.group() for x in re.finditer(rx, text)]
  # lowercase and remove punctuations
  regAcronyms = list(map(lambda x: x.lower().translate(str.maketrans('', '', string.punctuation)), acronyms))
  return list(set(regAcronyms))

# Exact match
def exact_abbrev(abbrev, text):
  regAbbr=abbrev.lower().translate(str.maketrans('', '', string.punctuation))
  text=text.lower()
  words=text.split()
  letters=[word[0] for word in words]
  return "".join(letters) == regAbbr

# Matches loose acronym
def is_abbrev(abbrev, text):
  abbrev=abbrev.lower()
  text=text.lower()
  words=text.split()
  if not abbrev:
    return True
  if abbrev and not text:
    return False
  if abbrev[0]!=text[0]:
    return False
  else:
    return (is_abbrev(abbrev[1:],' '.join(words[1:])) or any(is_abbrev(abbrev[1:]," ".join(words[i+1:])) for i in range(len(words[0]))))

def abbrev_first(abbrev, text):
  words=text.split()
  return is_abbrev(abbrev, words[0])

# Get map of all lemmatized phrases to potential Acronyms
def extractAcronymsAndPhrases(text):
  pairs = schwartz_hearst.extract_abbreviation_definition_pairs(doc_text=text)
  phraseAcronymLinks = {}
  for acronym, phrase in pairs.items():
    print(phrase)
    phraseAcronymLinks[toLemmas(str(phrase))] = acronym.lower()
  return phraseAcronymLinks

# Given list of acronyms and sorted phrases, a matching algorithm for acronym and phrases, get all matches for acronym and phrases
def extractAcronymsFromPhrases(allAcronyms, phrases):
  if len(phrases) == 0 or len(allAcronyms) == 0:
    return dict()
  acronym = allAcronyms.pop(0)
  for phrase in phrases:
    # Check for exact matches
    if exact_abbrev(acronym, phrase[1]):
      phrases.remove(phrase)
      recursiveChild = extractAcronymsFromPhrases(allAcronyms, phrases)
      recursiveChild[acronym] = toLemmas(phrase[1])
      return recursiveChild
  for phrase in phrases:
    # Check for loose matches
    if is_abbrev(acronym, phrase[1]):
      phrases.remove(phrase)
      recursiveChild = extractAcronymsFromPhrases(allAcronyms, phrases)
      recursiveChild[acronym] = toLemmas(phrase[1])
      return recursiveChild
  return extractAcronymsFromPhrases(allAcronyms, phrases)
