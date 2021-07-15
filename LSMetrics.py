import json
from tkinter import *
import sys
import os
from tkinter.filedialog import askopenfilename

label_frequencies = dict()
total_reqs = 0
total_ambs = 0

filename = askopenfilename()
with open(filename) as f:
  tasks = json.load(f)
  total_reqs = len(tasks)
  for task in tasks:
    completions = task["completions"]
    for completion in completions:
      results = completion["result"]
      for result in results:
        anno_type = result["type"]
        annos = result["value"][anno_type]
        for anno in annos:
          total_ambs += 1
          label_frequencies[anno] = label_frequencies.get(anno, 0) + 1

print("Total Requirements")
print(total_reqs)
print("------------------")
print("Total Ambiguities")
print(total_ambs)
print("------------------")
print("Requirement Ambiguity Index")
print(float(total_ambs)/float(total_reqs))
print("------------------")
print(label_frequencies)
