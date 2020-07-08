from Validator import get_validator_matches
from pathlib import Path
from tkinter import filedialog
from tkinter import *

root = Tk()
root.withdraw()
folder_selected = filedialog.askdirectory()
matches = dict()
total_words = 0
total_matches = 0

for path in Path(folder_selected).rglob('*'):
  if path.is_file():
     f = open(path, "r")
     inputText = f.read()
     total_words += len(inputText.split())
     file_match_ents, descriptions = get_validator_matches(inputText)
     total_matches += len(file_match_ents)
     for match in file_match_ents:
       label = match["label"]
       matches[label] = matches.get(label, 0) + 1
print("Total Matches")
print(total_matches)
print(matches)
print("Total Words")
print(total_words)
