#!/usr/bin/env python
# -*- coding: utf-8 -*-
import spacy
from spacy.lang.en import English
from uncertainty_recogniser import UncertatintyRecognizer
from spacy.pipeline import EntityRecognizer
import plac


def main(text="I think this is a test phrase", *uncertainties, ents):
    # For simplicity, we start off with only the blank English Language class
    # and no model or pre-defined pipeline loaded.
    nlp = spacy.load('en')

    if not uncertainties:  
        uncertainties = [
    "think", "thought", "thinking", "almost", 
    "apparent", "apparently", "appear", "appeared", "appears", "approximately", "around",
    "assume", "assumed", "certain amount", "certain extent", "certain level", "claim",
    "claimed", "doubt", "doubtful", "essentially", "estimate",
    "estimated", "feel", "felt", "frequently", "from our perspective", "generally", "guess",
    "in general", "in most cases", "in most instances", "in our view", "indicate", "indicated",
    "largely", "likely", "mainly", "may", "maybe", "might", "mostly", "often", "on the whole",
    "ought", "perhaps", "plausible", "plausibly", "possible", "possibly", "postulate",
    "postulated", "presumable", "probable", "probably", "relatively", "roughly", "seems",
    "should", "sometimes", "somewhat", "suggest", "suggested", "suppose", "suspect", "tend to",
    "tends to", "typical", "typically", "uncertain", "uncertainly", "unclear", "unclearly",
    "unlikely", "usually", "broadly", "tended to", "presumably", "suggests",
    "from this perspective", "from my perspective", "in my view", "in this view", "in our opinion",
    "in my opinion", "to my knowledge", "fairly", "quite", "rather", "argue", "argues", "argued",
    "claims", "feels", "indicates", "supposed", "supposes", "suspects", "postulates"
    ] 
    if not ents:  
        ents = ['UNCERTAINTY']
    component = UncertatintyRecognizer(nlp, uncertainties)  # initialise component
    nlp.add_pipe(component, last=True)  # add last to the pipeline
    doc = nlp(text)

    # for ent in doc.ents:
    #     print(ent.text, ent.start_char, ent.end_char, ent.label_)

    colors = {'UNCERTAINTY': 'linear-gradient(90deg, #aa9cfc, #fc9ce7)'}
    options = {'ents': ents, 'colors': colors}

    spacy.displacy.render(doc, style='ent', jupyter=True, options=options)
    # spacy.displacy.serve(doc, style='ent')


if __name__ == '__main__':
    plac.call(main)

