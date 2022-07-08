import streamlit as st

# from models.kgner import score

import pandas as pd
import numpy as np
import os
# import pymysql as mariadb

import spacy
from spacy import displacy
nlp = spacy.load('en_core_web_sm')

HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""


##SQL CONNECTION

def sanitize_kgner(text):
    docx = nlp(text)
    redacted_sentence = []
    with docx.retokenize() as retokenizer:
        for ent in docx.ents:
            retokenizer.merge(ent)
    for token in docx:
        print(f"{token}: {token.ent_type_}")
        if token.ent_type_ == "PERSON":
            redacted_sentence.append("[PERSON]")
        elif token.ent_type_ == "GPE":
            redacted_sentence.append("[PLACE]")
        else:
            redacted_sentence.append(token.text)
    return " ".join(redacted_sentence)

def extract_entities(text):
    docx = nlp(text)
    redacted_sentence = []
    with docx.retokenize() as retokenizer:
        for ent in docx.ents:
            retokenizer.merge(ent)
    for token in docx:
        print(f"{token}: {token.ent_type_}")
        if token.ent_type_ == "PERSON":
            redacted_sentence.append("[PERSON]")
        elif token.ent_type_ == "GPE":
            redacted_sentence.append("[PLACE]")
        else:
            redacted_sentence.append(token.text)
    return " ".join(redacted_sentence)

# @st.cache(allow_output_mutation=True)
def render_entities(raw_text):
    docx = nlp(raw_text)
    html = displacy.render(docx, style='ent')
    html = html.replace("\n\n", "\n")
    result = HTML_WRAPPER.format(html)
    return result

def main():
    st.title("Entity Extraction Local App")
    # st.text("Built with Spacy and Kgner")

    tasks = ["Extract Entities - Spacy", "Extract Entities - KGNER", "SQL-Connection test", "Sentiment Analysis", "Emotion Detection"]
    choice = st.sidebar.selectbox("Select task", tasks)

    if choice == "Extract Entities - Spacy":
        raw_text = st.text_area("Enter your Text", "Type Here")
        if st.button("Submit"):
            result = extract_entities(raw_text)
            st.subheader("Original Text")
            new_docx = render_entities(raw_text)
            st.markdown(new_docx, unsafe_allow_html=True)

            st.write(result)

if __name__ == '__main__':
    main()