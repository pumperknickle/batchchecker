import spacy
from spacy import displacy
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
from Describer import describe
from quantulum3 import parser
from DefinedNounsExtractor import get_term_in_noun_chunk
import en_core_web_sm
import re
import string
from spellchecker import SpellChecker

nlp = en_core_web_sm.load()
match_ents = []
definitions = []
total_matches = dict()
quantity_spans = []
comparator_spans = []
all_matches = 0
acronymPattern = re.compile("\b[A-Z](?=([&.]?))(?:\1[A-Za-z])*(?:\1[A-Z])\b")


def all_labels():
  return ["UNDEFINED TERM", "OBLIQUE", "MISSPELLING", "NO VALUE RANGE", "MISSING UNIT", "BRACKETS", "PARANTHESES", "MULTIPLE SENTENCES", "UNIVERSAL QUANTIFIER", "VAGUE ADJECTIVE", "VAGUE ADVERB", "PASSIVE VOICE", "INFINITIVE", "PRONOUN", "INDEFINITE ARTICLE", "ESCAPE CLAUSE", "OPEN ENDED CLAUSE", "AVOID NOT", "VAGUE QUANTIFIER", "TEMPORAL DEPENDENCY", "COMBINATOR", "UNACHIEVABLE ABSOLUTE"]


def overlap(matches, start, end):
    for match in matches:
        if start < match["end"] and match["start"] < end:
            return True
    return False

def spell_check(doc, raw_terms):
    global all_matches
    spell = SpellChecker()
    spell.word_frequency.load_words(raw_terms)
    for token in doc:
        word = token.text
        misspelled = spell.unknown([word])
        if len(misspelled) != 0 and not word.startswith("'"):
            all_matches += 1
            total_matches["MISSPELLING"] = total_matches.get("MISSPELLING", 0) + 1
            start = token.idx
            end = token.idx + len(token.text)
            if not overlap(match_ents, start, end) and not overlap(definitions, start, end) and not overlap(quantity_spans, start, end):
                match_ents.append({
                    "start": start,
                    "end": end,
                    "label": "MISSPELLING",
                })


def match_adverb(matcher, doc, i, matches):
    global all_matches
    match_id, start, end = matches[i]
    span = doc[start:end]
    all_matches += 1
    total_matches["VAGUE ADVERB"] = total_matches.get("VAGUE ADVERB", 0) + 1
    if not overlap(match_ents, span.start_char, span.end_char) and not overlap(definitions, span.start_char, span.end_char):
        match_ents.append({
            "start": span.start_char,
            "end": span.end_char,
            "label": "VAGUE ADVERB",
        })
    
def match_passive(matcher, doc, i, matches):
    global all_matches
    match_id, start, end = matches[i]
    span = doc[start:end]
    all_matches += 1
    total_matches["PASSIVE VOICE"] = total_matches.get("PASSIVE VOICE", 0) + 1
    if not overlap(match_ents, span.start_char, span.end_char) and not overlap(definitions, span.start_char, span.end_char):
        match_ents.append({
            "start": span.start_char,
            "end": span.end_char,
            "label": "PASSIVE VOICE",
        })
    
def match_infinitive(matcher, doc, i, matches):
    global all_matches
    match_id, start, end = matches[i]
    span = doc[start:end]
    all_matches += 1
    total_matches["INFINITIVE"] = total_matches.get("INFINITIVE", 0) + 1
    if not overlap(match_ents, span.start_char, span.end_char) and not overlap(definitions, span.start_char, span.end_char):
        match_ents.append({
            "start": span.start_char,
            "end": span.end_char,
            "label": "INFINITIVE",
        })
    
def match_pronoun(matcher, doc, i, matches):
    global all_matches
    match_id, start, end = matches[i]
    span = doc[start:end]
    all_matches += 1
    total_matches["PRONOUN"] = total_matches.get("PRONOUN", 0) + 1
    if not overlap(match_ents, span.start_char, span.end_char) and not overlap(definitions, span.start_char, span.end_char):
        match_ents.append({
            "start": span.start_char,
            "end": span.end_char,
            "label": "PRONOUN",
        })
    
def match_indefinite_articles(matcher, doc, i, matches):
    global all_matches
    match_id, start, end = matches[i]
    span = doc[start:end]
    all_matches += 1
    total_matches["INDEFINITE ARTICLE"] = total_matches.get("INDEFINITE ARTICLE", 0) + 1
    if not overlap(match_ents, span.start_char, span.end_char) and not overlap(definitions, span.start_char, span.end_char):
        match_ents.append({
            "start": span.start_char,
            "end": span.end_char,
            "label": "INDEFINITE ARTICLE",
        })

def match_vague_adjectives(matcher, doc, i, matches):
    global all_matches
    match_id, start, end = matches[i]
    span = doc[start:end]
    all_matches += 1
    total_matches["VAGUE ADJECTIVE"] = total_matches.get("VAGUE ADJECTIVE", 0) + 1
    if not overlap(match_ents, span.start_char, span.end_char) and not overlap(definitions, span.start_char, span.end_char):
        match_ents.append({
            "start": span.start_char,
            "end": span.end_char,
            "label": "VAGUE ADJECTIVE",
        })

def match_escape_clauses(matcher, doc, i, matches):
    global all_matches
    match_id, start, end = matches[i]
    span = doc[start:end]
    all_matches += 1
    total_matches["ESCAPE CLAUSE"] = total_matches.get("ESCAPE CLAUSE", 0) + 1
    if not overlap(match_ents, span.start_char, span.end_char) and not overlap(definitions, span.start_char, span.end_char):
        match_ents.append({
            "start": span.start_char,
            "end": span.end_char,
            "label": "ESCAPE CLAUSE",
        })
        
def match_open_ended_clauses(matcher, doc, i, matches):
    global all_matches
    match_id, start, end = matches[i]
    span = doc[start:end]
    all_matches += 1
    total_matches["OPEN ENDED CLAUSE"] = total_matches.get("OPEN ENDED CLAUSE", 0) + 1
    if not overlap(match_ents, span.start_char, span.end_char) and not overlap(definitions, span.start_char, span.end_char):
        match_ents.append({
            "start": span.start_char,
            "end": span.end_char,
            "label": "OPEN ENDED CLAUSE",
        })
        
def match_negations(matcher, doc, i, matches):
    global all_matches
    match_id, start, end = matches[i]
    span = doc[start:end]
    all_matches += 1
    total_matches["AVOID NOT"] = total_matches.get("AVOID NOT", 0) + 1
    if not overlap(match_ents, span.start_char, span.end_char) and not overlap(definitions, span.start_char, span.end_char):
        match_ents.append({
            "start": span.start_char,
            "end": span.end_char,
            "label": "AVOID NOT",
        })
        
def match_vague_quantifier(matcher, doc, i, matches):
    global all_matches
    match_id, start, end = matches[i]
    span = doc[start:end]
    all_matches += 1
    total_matches["VAGUE QUANTIFIER"] = total_matches.get("VAGUE QUANTIFIER", 0) + 1
    if not overlap(match_ents, span.start_char, span.end_char) and not overlap(definitions, span.start_char, span.end_char):
        match_ents.append({
            "start": span.start_char,
            "end": span.end_char,
            "label": "VAGUE QUANTIFIER",
        })

def match_universal_quantification(matcher, doc, i, matches):
    global all_matches
    match_id, start, end = matches[i]
    span = doc[start:end]
    all_matches += 1
    total_matches["UNIVERSAL QUANTIFIER"] = total_matches.get("UNIVERSAL QUANTIFIER", 0) + 1
    if not overlap(match_ents, span.start_char, span.end_char) and not overlap(definitions, span.start_char, span.end_char):
        match_ents.append({
            "start": span.start_char,
            "end": span.end_char,
            "label": "UNIVERSAL QUANTIFIER",
        })

def match_temporal(matcher, doc, i, matches):
    global all_matches
    match_id, start, end = matches[i]
    span = doc[start:end]
    all_matches += 1
    total_matches["TEMPORAL DEPENDENCY"] = total_matches.get("TEMPORAL DEPENDENCY", 0) + 1
    if not overlap(match_ents, span.start_char, span.end_char) and not overlap(definitions, span.start_char, span.end_char):
        match_ents.append({
            "start": span.start_char,
            "end": span.end_char,
            "label": "TEMPORAL DEPENDENCY",
        })

def match_combinator(matcher, doc, i, matches):
    global all_matches
    match_id, start, end = matches[i]
    span = doc[start:end]
    if overlap(quantity_spans, span.start_char, span.end_char):
        return
    all_matches += 1
    total_matches["COMBINATOR"] = total_matches.get("COMBINATOR", 0) + 1
    if not overlap(match_ents, span.start_char, span.end_char) and not overlap(definitions, span.start_char, span.end_char):
        match_ents.append({
            "start": span.start_char,
            "end": span.end_char,
            "label": "COMBINATOR",
        })

def match_unachievable_absolutes(matcher, doc, i, matches):
    global all_matches
    match_id, start, end = matches[i]
    span = doc[start:end]
    all_matches += 1
    total_matches["UNACHIEVABLE ABSOLUTE"] = total_matches.get("UNACHIEVABLE ABSOLUTE", 0) + 1
    if not overlap(match_ents, span.start_char, span.end_char) and not overlap(definitions, span.start_char, span.end_char):
        match_ents.append({
            "start": span.start_char,
            "end": span.end_char,
            "label": "UNACHIEVABLE ABSOLUTE",
        })

def match_parantheses(matcher, doc, i, matches):
    global all_matches
    match_id, start, end = matches[i]
    span = doc[start:end]
    all_matches += 1
    total_matches["PARANTHESES"] = total_matches.get("PARANTHESES", 0) + 1
    if not overlap(match_ents, span.start_char, span.end_char) and not overlap(definitions, span.start_char, span.end_char):
        match_ents.append({
            "start": span.start_char,
            "end": span.end_char,
            "label": "PARANTHESES",
        })

def match_brackets(matcher, doc, i, matches):
    global all_matches
    match_id, start, end = matches[i]
    span = doc[start:end]
    all_matches += 1
    total_matches["BRACKETS"] = total_matches.get("BRACKETS", 0) + 1
    if not overlap(match_ents, span.start_char, span.end_char) and not overlap(definitions, span.start_char, span.end_char):
        match_ents.append({
            "start": span.start_char,
            "end": span.end_char,
            "label": "BRACKETS",
        })

def match_oblique(matcher, doc, i, matches):
    global all_matches
    match_id, start, end = matches[i]
    span = doc[start:end]
    if overlap(quantity_spans, span.start_char, span.end_char):
        return
    all_matches += 1
    total_matches["OBLIQUE"] = total_matches.get("OBLIQUE", 0) + 1
    if not overlap(match_ents, span.start_char, span.end_char) and not overlap(definitions, span.start_char, span.end_char):
        match_ents.append({
            "start": span.start_char,
            "end": span.end_char,
            "label": "OBLIQUE",
        })

def detect_ind_article(text):
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    terms = ["a", "an"]
    patterns = [nlp.make_doc(text) for text in terms]
    matcher.add("indefinite articles", None, *patterns)
    doc = nlp(text)
    matches = matcher(doc)
    return len(matches) > 0

def is_num_mod(text, start):
    doc = nlp("text")
    for token in doc:
        if token.idx == start:
            return token.dep_ == 'nummod'

def toLemmas(text):
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc]).lower()

def detect_undefined_terms(doc, strie, defined_nouns):
    global all_matches
    for token in doc:
      regToken = token.text.lower().translate(str.maketrans('', '', string.punctuation))
      if acronymPattern.match(token.text) and (not regToken in defined_nouns):
        start_term = token.idx
        end_term = token.idx + len(token.text)
        all_matches += 1
        total_matches["UNDEFINED TERM"] = total_matches.get("UNDEFINED TERM", 0) + 1
        if not overlap(match_ents, start_term, end_term) and not overlap(quantity_spans, start_term, end_term):
          match_ents.append({
            "start": start_term,
            "end": end_term,
            "label": "UNDEFINED TERM"
          })
    for chunk in doc.noun_chunks:
      term_in_noun_chunk = get_term_in_noun_chunk(strie, chunk, doc)
      start_term = term_in_noun_chunk[0]
      end_term = term_in_noun_chunk[1]
      if not toLemmas(doc.char_span(start_term, end_term).text.lower()) in defined_nouns:
        all_matches += 1
        total_matches["UNDEFINED TERM"] = total_matches.get("UNDEFINED TERM", 0) + 1
        if not overlap(match_ents, start_term, end_term) and not overlap(quantity_spans, start_term, end_term):
          match_ents.append({
            "start": start_term,
            "end": end_term,
            "label": "UNDEFINED TERM"
          })

def match_unit_ambiguities(text):
    global all_matches
    previous_start = -1
    for quant in quantity_spans:
        if detect_ind_article(quant["word"]):
            continue
        if quant["entity"] == 'dimensionless' and (not is_num_mod(text, quant["start"])):
            all_matches += 1
            total_matches["MISSING UNIT"] = total_matches.get("MISSING UNIT", 0) + 1
            if not overlap(match_ents, quant["start"], quant["end"]):
                match_ents.append({
                    "start": quant["start"],
                    "end": quant["end"],
                    "label": "MISSING UNIT"
                })
        if quant["uncertainty"] == None and (not overlap(comparator_spans, previous_start, quant["start"])):
            all_matches += 1
            total_matches["NO VALUE RANGE"] = total_matches.get("NO VALUE RANGE", 0) + 1
            if not overlap(match_ents, quant["start"], quant["end"]):
                match_ents.append({
                    "start": quant["start"],
                    "end": quant["end"],
                    "label": "NO VALUE RANGE"
                })
        previous_start = quant["start"]

def find_quantities(text):
    quants = parser.parse(text)
    for quant in quants:
        quantity_spans.append({
            "start": quant.span[0],
            "end": quant.span[1],
            "word": quant.surface,
            "entity": quant.unit.entity.name,
            "uncertainty": quant.uncertainty
        })

def match_definitions(matcher, doc, i, matches):
    match_id, start, end = matches[i]
    span = doc[start:end]
    definitions.append({
        "start": span.start_char,
        "end": span.end_char,
        "label": "DEFINITION",
    })

def match_comparator(matcher, doc, i, matches):
    match_id, start, end = matches[i]
    span = doc[start:end]
    comparator_spans.append({
        "start": span.start_char,
        "end": span.end_char,
    })
        
def get_validator_matches(text, strie, defined_nouns, raw_terms):
    global all_matches
    match_ents.clear()
    total_matches.clear()
    all_matches = 0
    quantity_spans.clear()
    comparator_spans.clear()
    definitions.clear()

    find_quantities(text)

    definitionMatcher = PhraseMatcher(nlp.vocab, attr="LEMMA")
    definitionPatterns = [nlp(text) for text in list(defined_nouns)]
    definitionMatcher.add("Definition", match_definitions, *definitionPatterns)

    matcher = Matcher(nlp.vocab, validate=True)
    phraseMatcher = PhraseMatcher(nlp.vocab, attr="LEMMA")
    exactMatcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    
    comparatorPattern1 = [{"ORTH": {"REGEX": "\w+er"}}, {"LOWER": "than"}]
    comparatorPattern2 = [{"LOWER": "less"}, {"LOWER": "than"}]
    comparatorPattern3 = [{"LOWER": "more"}, {"LOWER": "than"}]
    comparatorPattern4 = [{"LOWER": "maximum"}]
    comparatorPattern5 = [{"LOWER": "minimum"}]
    comparatorPattern6 = [{"LOWER": "over"}]
    matcher.add("Comparator", match_comparator, comparatorPattern1, comparatorPattern2, comparatorPattern3, comparatorPattern4, comparatorPattern5)
   
    adverbPattern = [{"POS": "ADV", "ORTH": {"REGEX": "\w+ly"}}]
    matcher.add("Adverbs", match_adverb, adverbPattern)

    pastTenseVerbPattern1 = [{"LEMMA": "be"}, {"TAG": "VBD"}]
    matcher.add("Passive Voice", match_passive, pastTenseVerbPattern1)

    infinitivePattern1 = [{"LOWER": "be"}, {"POS": "ADJ"}, {"POS": "ADP"}]
    infinitivePattern2 = [{"LOWER": "to"}, {"POS": "VERB"}]
    matcher.add("Infinitive", match_infinitive, infinitivePattern1, infinitivePattern2)

    pronounPattern = [{"POS": "PRON"}]
    matcher.add("Pronoun", match_pronoun, pronounPattern)

    indefiniteArticles = ["a", "an"]
    indefiniteArticlePatterns = [nlp(text) for text in indefiniteArticles]
    phraseMatcher.add("Indefinite Articles", match_indefinite_articles, *indefiniteArticlePatterns)

    vagueAdjectives = ["ancillary", "relevant", "routine", "common", "generic", "significant", "flexible", "expandable", "typical", "sufficient", "adequate", "appropriate", "efficient", "effective", "proficient", "reasonable", "customary"]
    vagueAdjectivePatterns = [nlp(text) for text in vagueAdjectives]
    phraseMatcher.add("Vague Adjectives", match_vague_adjectives, *vagueAdjectivePatterns)

    escapeClauses = ["greater than", "so far as is possible", "as possible", "as little as possible", "where possible", "as much as possible", "if it should prove necessary", "if necessary", "to the extent necessary", "as appropriate", "as required", "to the extent practical", "if practicable"]
    escapeClausesPatterns = [nlp(text) for text in escapeClauses]
    phraseMatcher.add("Escape Clauses", match_escape_clauses, *escapeClausesPatterns)

    openEndedClauses = ["including but not limited to", "etc", "and so on"]
    openEndedPatterns = [nlp(text) for text in openEndedClauses]
    phraseMatcher.add("Open Ended Clauses", match_open_ended_clauses, *openEndedPatterns)

    notTerms = ["not"]
    notPatterns = [nlp(text) for text in notTerms]
    phraseMatcher.add("Negations", match_negations, *notPatterns)

    vagueQuantifiers = ["allowable", "completely", "prompt", "fast", "minimum", "maximum", "optimum", "some"]
    vagueQuantifiersPatterns = [nlp(text) for text in vagueQuantifiers]
    exactMatcher.add("Vague Quantifiers", match_vague_quantifier, *vagueQuantifiersPatterns)

    universalQuantifiers =  ["both", "any", "all"]
    universalPatterns = [nlp(text) for text in universalQuantifiers]
    exactMatcher.add("Universal Quantifiers", match_universal_quantification, *universalPatterns)
    
    obliques = ["/"]
    obliquePatterns = [nlp(text) for text in obliques]
    exactMatcher.add("Obliques", match_oblique, *obliquePatterns)

    temporalDependencies = ["eventually", "before", "when", "after", "as", "once", "earliest", "latest", "instantaneous", "simultaneous", "while", "at last"]
    temporalPatterns = [nlp(text) for text in temporalDependencies]
    phraseMatcher.add("Temporal Dependencies", match_temporal, *temporalPatterns)

    combinators = ["and", "or", "then", "unless", "but", "as well as", "but also", "however", "whether", "meanwhile", "whereas", "on the other hand", "otherwise"]
    combinatorPatterns = [nlp(text) for text in combinators]
    phraseMatcher.add("Combinators", match_combinator, *combinatorPatterns)
    
    unachievableAbsolutes = ["100%", "always", "never"]
    unachievableAbsolutePatterns = [nlp(text) for text in unachievableAbsolutes]
    phraseMatcher.add("Unachievable Absolutes", match_unachievable_absolutes, *unachievableAbsolutePatterns)

    parantheses = ["(", ")"]
    paranthesesPatterns = [nlp(text) for text in parantheses]
    exactMatcher.add("Parantheses", match_parantheses, *paranthesesPatterns)

    brackets = ["{", "}", "[", "]"]
    bracketsPatterns = [nlp(text) for text in brackets]
    exactMatcher.add("Brackets", match_brackets, *bracketsPatterns)

    doc = nlp(text)
    lowercaseDoc = nlp(text.lower())
    definitionMatches = definitionMatcher(lowercaseDoc)
    matches = matcher(doc)
    phraseMatches = phraseMatcher(lowercaseDoc)
    exactMatches = exactMatcher(lowercaseDoc)
    match_unit_ambiguities(text)
    detect_undefined_terms(doc, strie, defined_nouns)
    match_ents.sort(key=lambda x: x["start"])
    return match_ents, all_matches, total_matches
