import spacy
from spacy import displacy
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import webbrowser

nlp = spacy.load("en")

match_ents = []

def overlap(matches, start, end):
    for match in matches:
        if (not match["end"] < start) and (not match["start"] > end):
            return True
    return False


def match_adjective(matcher, doc, i, matches):
    match_id, start, end = matches[i]
    span = doc[start:end]
    if not overlap(match_ents, span.start_char, span.end_char):  
        match_ents.append({
            "start": span.start_char,
            "end": span.end_char,
            "label": "ADJECTIVE",
        })

def match_adverb(matcher, doc, i, matches):
    match_id, start, end = matches[i]
    span = doc[start:end]
    if not overlap(match_ents, span.start_char, span.end_char):  
        match_ents.append({
            "start": span.start_char,
            "end": span.end_char,
            "label": "ADVERB",
        })
    
def match_passive(matcher, doc, i, matches):
    match_id, start, end = matches[i]
    span = doc[start:end]
    if not overlap(match_ents, span.start_char, span.end_char):  
        match_ents.append({
            "start": span.start_char,
            "end": span.end_char,
            "label": "PASSIVE VOICE",
        })
    
def match_infinitive(matcher, doc, i, matches):
    match_id, start, end = matches[i]
    span = doc[start:end]
    if not overlap(match_ents, span.start_char, span.end_char):  
        match_ents.append({
            "start": span.start_char,
            "end": span.end_char,
            "label": "INFINITIVE",
        })
    
def match_pronoun(matcher, doc, i, matches):
    match_id, start, end = matches[i]
    span = doc[start:end]
    if not overlap(match_ents, span.start_char, span.end_char):  
        match_ents.append({
            "start": span.start_char,
            "end": span.end_char,
            "label": "PRONOUN",
        })
    
def match_indefinite_articles(matcher, doc, i, matches):
    match_id, start, end = matches[i]
    span = doc[start:end]
    if not overlap(match_ents, span.start_char, span.end_char):  
        match_ents.append({
            "start": span.start_char,
            "end": span.end_char,
            "label": "INDEFINITE ARTICLE",
        })
        
def match_vague_terms(matcher, doc, i, matches):
    match_id, start, end = matches[i]
    span = doc[start:end]
    if not overlap(match_ents, span.start_char, span.end_char):  
        match_ents.append({
            "start": span.start_char,
            "end": span.end_char,
            "label": "VAGUE TERM",
        })
        
def match_escape_clauses(matcher, doc, i, matches):
    match_id, start, end = matches[i]
    span = doc[start:end]
    if not overlap(match_ents, span.start_char, span.end_char):  
        match_ents.append({
            "start": span.start_char,
            "end": span.end_char,
            "label": "ESCAPE CLAUSE",
        })
        
def match_open_ended_clauses(matcher, doc, i, matches):
    match_id, start, end = matches[i]
    span = doc[start:end]
    if not overlap(match_ents, span.start_char, span.end_char):  
        match_ents.append({
            "start": span.start_char,
            "end": span.end_char,
            "label": "OPEN ENDED CLAUSE",
        })
        
def match_negations(matcher, doc, i, matches):
    match_id, start, end = matches[i]
    span = doc[start:end]
    if not overlap(match_ents, span.start_char, span.end_char):  
        match_ents.append({
            "start": span.start_char,
            "end": span.end_char,
            "label": "AVOID NOT",
        })
        
def match_universal_quantifier(matcher, doc, i, matches):
    match_id, start, end = matches[i]
    span = doc[start:end]
    if not overlap(match_ents, span.start_char, span.end_char):  
        match_ents.append({
            "start": span.start_char,
            "end": span.end_char,
            "label": "VAGUE QUANTIFIER",
        })
        
def match_temporal(matcher, doc, i, matches):
    match_id, start, end = matches[i]
    span = doc[start:end]
    if not overlap(match_ents, span.start_char, span.end_char):  
        match_ents.append({
            "start": span.start_char,
            "end": span.end_char,
            "label": "TEMPORAL DEPENDENCY",
        })
    
matcher = Matcher(nlp.vocab)
phraseMatcher = PhraseMatcher(nlp.vocab, attr="LEMMA")

adverbPattern = [{"POS": "ADV"}]
matcher.add("Adverbs", match_adverb, adverbPattern)

adjectivePattern = [{"POS": "ADJ"}]
matcher.add("Adjectives", match_adjective, adjectivePattern)

pastTenseVerbPattern1 = [{"TAG": "VBD"}]
pastTenseVerbPattern2 = [{"TAG": "VBN"}]
matcher.add("Passive Voice", match_passive, pastTenseVerbPattern1, pastTenseVerbPattern2)

infinitivePattern1 = [{"LOWER": "be"}, {"POS": "ADJ"}, {"POS": "ADP"}]
infinitivePattern2 = [{"LOWER": "to"}, {"POS": "VERB"}]
matcher.add("Infinitive", match_infinitive, infinitivePattern1, infinitivePattern2)

pronounPattern = [{"POS": "PRON"}]
matcher.add("Pronoun", match_pronoun, pronounPattern)

indefiniteArticles = ["a", "an"]
indefiniteArticlePatterns = [nlp(text) for text in indefiniteArticles]
phraseMatcher.add("Indefinite Articles", match_indefinite_articles, *indefiniteArticlePatterns)

vagueTerms = ["some", "any", "allowable", "several", "many", "lot of", "a few", "almost always", "very nearly", "nearly", "about", "close to", "almost", "approximate"]
vagueTermsPatterns = [nlp(text) for text in vagueTerms]
phraseMatcher.add("Vague Terms", match_vague_terms, *vagueTermsPatterns)

escapeClauses = ["so far as is possible", "as possible", "as little as possible", "where possible", "as much as possible", "if it should prove necessary", "if necessary", "to the extent necessary", "as appropriate", "as required", "to the extent practical", "if practicable"]
escapeClausesPatterns = [nlp(text) for text in escapeClauses]
phraseMatcher.add("Escape Clauses", match_escape_clauses, *escapeClausesPatterns)

openEndedClauses = ["including but not limitedd to", "etc", "and so on"]
openEndedPatterns = [nlp(text) for text in openEndedClauses]
phraseMatcher.add("Open Ended Clauses", match_open_ended_clauses, *openEndedPatterns)

notTerms = ["not"]
notPatterns = [nlp(text) for text in notTerms]
phraseMatcher.add("Negations", match_negations, *notPatterns)

universalQuantifiers = ["all", "any", "both", "completely", "prompt", "fast", "minimum", "maximum", "optimum"]
universalPatterns = [nlp(text) for text in universalQuantifiers]
phraseMatcher.add("Immeasurable Quantifiers", match_universal_quantifier, *universalPatterns)

temporalDependencies = ["eventually", "before", "when", "after", "as", "once", "earliest", "latest", "instantaneous", "simultaneous", "while", "at last"]
temporalPatterns = [nlp(text) for text in temporalDependencies]
phraseMatcher.add("Temporal Dependencies", match_temporal, *temporalPatterns)

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename()

f = open(filename, "r")
inputText = f.read()

doc = nlp(inputText)
matches = matcher(doc)
lowercaseDoc = nlp(inputText.lower())
phraseMatches = phraseMatcher(lowercaseDoc)

match_ents.sort(key=lambda x: x["start"])

options = {"colors": {"ADVERB": "orange", "PASSIVE VOICE": "yellow", "ADJECTIVE": "purple", "INFINITIVE": "green", "INDEFINITE ARTICLE": "blue"}}

url = 'http://0.0.0.0:5000'

webbrowser.open_new_tab(url)

# Open URL in new window, raising the window if possible.
webbrowser.open_new(url)

displacy.serve([{"text": doc.text, "ents": match_ents}], style="ent", manual=True, options = options)
