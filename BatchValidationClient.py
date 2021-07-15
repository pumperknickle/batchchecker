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
from DefinedNounsExtractor import extract_defined_nouns_from_all, defined_nouns_from_av2, extract_definitions
from AcronymExtractor import extractAcronymsAndPhrases, extractAllAcronyms, extractAcronymsFromPhrases
from DocExtractor import getTextFromDoc
import en_core_web_sm
import copy
import re
from tqdm import tqdm
import PySimpleGUI as sg
import json

root = Tk()
root.withdraw()
folder_selected = filedialog.askdirectory()

nlp = en_core_web_sm.load() # Assigns the spacy model to the variable "nlp"
all_match_ents = []
metrics = []
matches = dict()
all_metrics = dict()
total_words = 0
total_requirements = 0
total_matches = 0
texts = []
minimum_keyword_score = 2
av2file = 'AV-2.xlsx'
av2path = os.path.join(folder_selected, av2file)

# This is extracting python strings from directory

for path in Path(folder_selected).rglob('*'):
    if path.is_file() and not(os.path.basename(path).startswith('.')) and not(os.path.basename(path) == 'RQT_report.html') and not(os.path.basename(path) == "RQT_Statistics.txt") and not(path.suffix == ".xlsx") and not(path.suffix == ".json"):
      # print(path)
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
raw_terms = []
if os.path.exists(av2path):
  defined_nouns = defined_nouns.union(defined_nouns_from_av2(av2path, phraseAcronymsLinks))
  for definition in extract_definitions(av2path):
    doc = nlp(definition)
    for token in doc:
      raw_terms.append(token.text.lower())

for inputText, reqPath in texts:
  requirements = inputText.split('\n')
  filteredReqs = list(filter(lambda x: len(x.strip()) != 0, requirements)) # "filteredReqs" is a list of refined requirements
  total_requirements += len(filteredReqs) # The total number of requirements is updated based on the length of the "filteredReqs" list
  total_words += len(inputText.split())

  # --------------------------------------------------------------------
  layout = [[sg.Text('Analyzing requirements... please wait.')],
            [sg.ProgressBar(len(filteredReqs), orientation='h', size=(20, 20), key='progressbar')],
            [sg.Cancel()]]
  window = sg.Window('RQT', layout)
  progress_bar = window['progressbar']
  # --------------------------------------------------------------------
labelStudArr = []
for i in tqdm(range(len(filteredReqs))): # Added tqdm here...
    #--------------------------------------------------------------------------------------------------------------------------------------------
    event, values = window.read(timeout=10)
    if event == 'Cancel' or event == sg.WIN_CLOSED:
      break
    #--------------------------------------------------------------------------------------------------------------------------------------------
    req = filteredReqs[i].strip() # Strip the whitespace off the beginning and end of each requirement
    file_match_ents, match_count, match_metrics = get_validator_matches(req, keySuffixTrie, defined_nouns, raw_terms)
    total_matches += match_count
    for key in match_metrics:
      all_metrics[key] = all_metrics.get(key, 0) + match_metrics[key]
    labelStudObj = {}
    reqTextObject = {}
    reqTextObject["text"] = req
    labelStudObj["data"] = reqTextObject
    predictionsArr = []
    predictionObj = {}
    predictionObj["model_version"] = "RQT 1.0"
    resultArr = []
    matched_passive = False
    matched_multiple = False
    for match in file_match_ents:
      label = match["label"]
      matches[label] = matches.get(label, 0) + 1
      resultObj = {}
      if label == "PASSIVE VOICE" or label == "MULTIPLE SENTENCES":
        if label == "PASSIVE VOICE":
          matched_passive = True
        else:
          matched_multiple = True
#        resultObj["from_name"] = "sentiment"
#        resultObj["to_name"] = "text"
#        resultObj["type"] = "choices"
      else:
        resultObj["from_name"] = "Ambiguity"
        resultObj["to_name"] = "text"
        resultObj["type"] = "labels"
      valueObj = {}
      if label == "PASSIVE VOICE" or label == "MULTIPLE SENTENCES":
         # print("matched passive or multiple")
       valueObj["choices"] = [label]
      else:
        startIdx = match["start"]
        endIdx = match["end"]
        valueObj["start"] = startIdx
        valueObj["end"] = endIdx
        valueObj["text"] = req[startIdx:endIdx]
        valueObj["score"] = 1.0
        labelsArr = [label]
        valueObj["labels"] = labelsArr
        resultObj["value"] = valueObj
        resultArr.append(resultObj)
    if matched_passive or matched_multiple:
      resultObj = {}
      resultObj["from_name"] = "sentiment"
      resultObj["to_name"] = "text"
      resultObj["type"] = "choices"
      valueObj = {}
      if matched_passive and matched_multiple:
        valueObj["choices"] = ["PASSIVE VOICE", "MULTIPLE SENTENCES"]
      else:
        if matched_multiple:
          valueObj["choices"] = ["MULTIPLE SENTENCES"]
        else:
          valueObj["choices"] = ["PASSIVE VOICE"]
      valueObj["score"] = 1.0
      resultObj["value"] = valueObj
      resultArr.append(resultObj)
    predictionObj["result"] = resultArr
    predictionsArr.append(predictionObj)
    labelStudObj["predictions"] = predictionsArr
    labelStudArr.append(labelStudObj)
    all_match_ents.append({"text": req, "ents": file_match_ents.copy(), "title": str(reqPath) + " " + str(i+1)})
    # --------------------------------------------------------------------
    progress_bar.UpdateBar(i + 1)
    # --------------------------------------------------------------------
window.close()
labelStudJSON = json.dumps(labelStudArr)


metrics.append({"text": "generated by RQT", "ents": [], "title": "Metrics"})

rai = float(total_matches)/float(total_requirements)
metrics.append({"text": str(total_requirements), "ents": [], "title": "Total Requirements Count"})
metrics.append({"text": str(total_matches), "ents": [], "title": "Total Detected Ambiguities"})
metrics.append({"text": str(round(rai, 4)), "ents": [], "title": "Requirements Ambiguity Index"})
sorted_metrics = {k: v for k, v in sorted(all_metrics.items(), key=lambda item: item[1], reverse=True)}
for key, value in sorted_metrics.items():
  metrics.append({"text": str(value), "ents": [], "title": key})

colors = dict()

for label in all_labels():
  colors[label] = "yellow"

options = {"colors": colors}
html = displacy.render(metrics + all_match_ents, style="ent", manual=True, page=True, options = options)

filename = 'RQT_report.html'
file_path = os.path.join(folder_selected, filename)
file = codecs.open(file_path, "w", "utf-8")
file.write(html)
file.close()

filename = 'RQT_1_predictions.json'
file_path = os.path.join(folder_selected, filename)
secondFile = codecs.open(file_path, "w", "utf-8")
secondFile.write(labelStudJSON)
secondFile.close()

sg.popup('Requirements analysis complete.')
