import spacy
from spacy import displacy
from pathlib import Path
from Validator import get_validator_matches, all_labels
from tkinter import *
from tkinter import filedialog
import sys
import os
import codecs
from rake_nltk import Metric, Rake
import pygtrie
from SuffixTrie import insertSuffixes
from DefinedNounsExtractor import extract_defined_nouns_from_all
from AcronymExtractor import extractAcronymsAndPhrases, extractAllAcronyms, extractAcronymsFromPhrases
from DocExtractor import getTextFromDoc
import en_core_web_sm
import copy 
import re

root = Tk()
root.withdraw()
folder_selected = filedialog.askdirectory()

nlp = en_core_web_sm.load()
all_match_ents = []
metrics = []
matches = dict()
all_metrics = dict()
total_words = 0
total_matches = 0
texts = []
minimum_keyword_score = 2

for path in Path(folder_selected).rglob('*'):
    if path.is_file() and not(os.path.basename(path).startswith('.')) and not(os.path.basename(path) == 'RQT_report.html'):
      if path.suffix == ".docx":
        doc_texts = getTextFromDoc(path)
        texts.append((doc_texts, path))
        continue
      with codecs.open(path, 'r', encoding='utf-8',
                 errors='ignore') as f:
        inputText = f.read()
        texts.append((inputText, path))

all_text = " ".join(map(lambda x: x[0], texts))
r = Rake(min_length=2, max_length=4)
r.extract_keywords_from_text(all_text)
acronyms = extractAllAcronyms(all_text)
phrasesWithScores = r.get_ranked_phrases_with_scores()
phraseAcronymsLinks = extractAcronymsFromPhrases(acronyms, copy.deepcopy(phrasesWithScores))
phraseAcronymsLinks.update(extractAcronymsAndPhrases(all_text))
phrasesWithScores.reverse()
keySuffixTrie = pygtrie.StringTrie()
for phraseWithScore in phrasesWithScores:
  score = phraseWithScore[0]
  phrase = phraseWithScore[1].lower().split()
  insertSuffixes(keySuffixTrie, phrase, score)
docs = map(lambda x: nlp(x[0]), texts)
defined_nouns = extract_defined_nouns_from_all(docs, keySuffixTrie, phraseAcronymsLinks)

for inputText, reqPath in texts:
  requirements = inputText.split('\n')
  filteredReqs = list(filter(lambda x: len(x.strip()) != 0, requirements))
  total_words += len(inputText.split())
  for i in range(len(filteredReqs)):
    req = filteredReqs[i]
    file_match_ents, match_count, match_metrics = get_validator_matches(req, keySuffixTrie, defined_nouns)
    total_matches += match_count
    for key in match_metrics: 
      if key in all_metrics: 
        all_metrics[key] = all_metrics[key] + match_metrics[key] 
      else:
        all_metrics[key] = match_metrics[key]
    for match in file_match_ents:
      label = match["label"]
      matches[label] = matches.get(label, 0) + 1
    all_match_ents.append({"text": req, "ents": file_match_ents.copy(), "title": str(reqPath) + " " + str(i+1)})


print(all_metrics)
metricsText = "Out of " + str(total_words) + " words, " + str(total_matches) + " potential ambiguities were detected."
metrics.append({"text": metricsText, "ents": [], "title": "Metrics"})

colors = dict()

for label in all_labels():
  colors[label] = "yellow"

options = {"colors": colors}
html = displacy.render(metrics + all_match_ents, style="ent", manual=True, page=True, options = options)

filename = 'RQT_report.html'
file_path = os.path.join(folder_selected, filename) 
with open(file_path, 'w') as file:
  file.write(html)
