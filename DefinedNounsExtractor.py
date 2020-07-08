import spacy
from SuffixTrie import maxMatch
import en_core_web_sm
import string

nlp = en_core_web_sm.load()

def toLemmas(text):
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc])

def extract_defined_nouns(doc, strie, acronymLinks, phraseLinks):
  defined_nouns = set()
  for chunk in doc.noun_chunks:
    if chunk.root.dep_ == "nsubj" and chunk.root.head.lemma_ == "be" and doc[chunk.root.head.i + 1].pos_ == "DET":
      result_span = get_term_in_noun_chunk(strie, chunk)
      phrase = doc.char_span(result_span[0], result_span[1]).text.lower()
      lemmatizedPhrase = toLemmas(phrase)
      defined_nouns.add(lemmatizedPhrase)
      if lemmatizedPhrase in acronymLinks:
        defined_nouns.add(acronymLinks[lemmatizedPhrase])
      regToken = chunk.root.text.lower().translate(str.maketrans('', '', string.punctuation))
      if regToken in phraseLinks:
        defined_nouns.add(phraseLinks[regToken])
  return defined_nouns

def extract_defined_nouns_from_all(docs, strie, phraseLinks):
  defined_nouns = set()
  acronymLinks = {v: k for k, v in phraseLinks.items()}
  for doc in docs:
    defined_nouns = defined_nouns.union(extract_defined_nouns(doc, strie, acronymLinks, phraseLinks))
  return defined_nouns

def get_term_in_noun_chunk(trie, chunk):
  maxMatchReturn = maxMatch(trie, chunk)
  if maxMatchReturn is None:
    return (chunk.root.idx, chunk.root.idx + len(chunk.root.text))
  return maxMatchReturn
    
