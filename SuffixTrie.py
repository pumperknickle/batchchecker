import pygtrie

def insertSuffixes(trie, keys, value):
  for i in range(len(keys)):
    if i >= len(keys) - 1:
      break
    prefixArray = keys[i:len(keys)]
    prefix = "/".join(prefixArray)
    trie[prefix] = value

def maxMatch(trie, chunk):
  max_match_return = None
  max_score = 0
  for i in range(len(chunk)):
    if i >= len(chunk) - 1:
      break
    prefixArray = chunk[i:len(chunk)].text.lower().split()
    prefix = "/".join(prefixArray)
    if trie.has_node(prefix):
      results = trie.items(prefix=prefix)
      for result in results:
        if result[1] > max_score:
          max_match_return = i
    if not max_match_return is None:
      break
  if max_match_return is None:
    return None
  return (chunk[max_match_return].idx, chunk[len(chunk) - 1].idx + len(chunk[len(chunk) - 1].text))
    
