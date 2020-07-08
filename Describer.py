def describe(label, text):
  if label == 'PASSIVE VOICE':
    return text.capitalize() + " is a past tense verb indicating passive voice. Use active voice in the requirement with the responsible entity clearly identified as the subject."
  if label == 'INFINITIVE':
    return text.capitalize() + " is a superflous infinitive. Requirements containing such superfluous verbs can cause problems in verification."
  if label == 'VAGUE ADVERB':
    return text.capitalize() + " is an vague adverb. Vague adverbs can lead to ambiguous, unverifiable requirements that do not accurately reflect the stakeholder expectations."
  if label == 'PRONOUN':
    return text.capitalize() + " is a pronoun. Pronouns are effectively cross-references to nouns and are ambiguous and should be avoided."
  if label == 'INDEFINITE ARTICLE':
    return text.capitalize() + " is the indefinite article. When referring to entities, use of the indefinite article can lead to ambiguity." 
  if label == 'VAGUE TERM':
    return text.capitalize() + " is a vague term. Vague words and phrases tend to make requirements imprecise and ambiguous. They leave room for multiple interpretations, which increases risk."
  if label == 'ESCAPE CLAUSE':
    return text.capitalize() + " is a escape clause. Escape clauses give an excuse to the developer of the system at lower levels to not bother with a requirement."
  if label == 'OPEN ENDED CLAUSE':
    return text.capitalize() + " is an open ended clause. Opened ended requirements can lead to serious interpretation problems concerning what is in or out of scope of the contract"
  if label == 'AVOID NOT':
    return text.capitalize() + " is a negation. The presence of negations in a requirement, especially in combination with the imperative, can lead to problems in verification."
  if label == 'VAGUE QUANTIFIER':
    return text.capitalize() + " is a vague quantifier. Vague quantifiers indicate quantities that cannot be objectively measured. Such terms are inherently ambiguous and must be replaced by specific, measurable quantities."
  if label == 'UNACHIEVABLE ABSOLUTE':
    return text.capitalize() + " is an unachievable absolute. A requirement with unachievable absolutes cannot be objectively verified"
  if label == 'UNIVERSAL QUANTIFIER':
    return text.capitalize() + " is a universal quantifier."
  if label == 'TEMPORAL DEPENDENCY':
    return text.capitalize() + " is a temporal dependency. Some words and phrases signal non-specific timing and should be replaced by specific timing constraints."
  if label == 'COMBINATOR':
    return text.capitalize() + " is a combinator. Combinators are conjunctions and other words and phrases that combine clauses. Their presence in requirements often indicates that the statement contains more than one requirement and should be broken up."
