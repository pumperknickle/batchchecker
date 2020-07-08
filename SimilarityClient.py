import spacy
from pathlib import Path
from tkinter import *
from tkinter import filedialog
import sys
import os
import codecs
from DocExtractor import getTextFromDoc
import en_core_web_lg
import copy
import re

filename = 'Similarity_report.txt'

root = Tk()
root.withdraw()
folder_selected = filedialog.askdirectory()

nlp = en_core_web_lg.load()
texts = []

for path in Path(folder_selected).rglob('*'):
    if path.is_file() and not(os.path.basename(path).startswith('.')) and not(os.path.basename(path) == 'RQT_report.html') and not(os.path.basename(path) == filename):
      if path.suffix == ".docx":
        doc_texts = getTextFromDoc(path)
        texts.append((doc_texts, path))
        continue
      with codecs.open(path, 'r', encoding='utf-8',
                 errors='ignore') as f: 
        inputText = f.read()
        texts.append((inputText, path))

all_reqs = []
for inputText, reqPath in texts:
  requirements = inputText.split('\n')
  filteredReqs = list(filter(lambda x: len(x.strip()) != 0, requirements))
  for req in filteredReqs:
    all_reqs.append((req, reqPath))

similarity_threshold = 0.95
similar_requirements = []
all_rec_docs = list(map(lambda x: (nlp(x[0]),x[1]), all_reqs))
all_filtered_req_docs = list(map(lambda x: (nlp(' '.join([str(t) for t in x[0] if not t.is_stop])), x[1]), all_rec_docs))
for i in range(len(all_filtered_req_docs) - 1):
  for j in range(i+1, len(all_filtered_req_docs)):
    left_req = all_filtered_req_docs[i]
    right_req = all_filtered_req_docs[j]
    full_left_req = all_rec_docs[i]
    full_right_req = all_rec_docs[j]
    if left_req[0].similarity(right_req[0]) > similarity_threshold:
      similarity_str = str(full_left_req[1]) + "\n" + full_left_req[0].text + "\n\n" + str(full_right_req[1]) + "\n" + full_right_req[0].text
      similar_requirements.append(similarity_str)

full_text = "\n\n\n\n\n".join(similar_requirements)
file_path = os.path.join(folder_selected, filename)
with open(file_path, 'w') as file:
  file.write(full_text)


