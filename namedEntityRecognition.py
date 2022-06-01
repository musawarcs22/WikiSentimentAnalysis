import spacy
from spacy import displacy
nlp = spacy.load("en_core_web_sm")
import streamlit as st

import matplotlib.pyplot as plt
import pandas as pd


def visulizeSentences(text,choice):
    csv_sentences = pd.read_csv("wiki_text.csv")
    senString=""
    for i in range(0,5):
        senString += csv_sentences.at[i,'sentence']
    #Visualizing Sentences line by line
    
    
    if choice =="ent":
        html = displacy.render(nlp(senString), style="ent", minify=True)
        st.components.v1.html(html, width=600, height=600, scrolling=True)
    else: #choice =="dep"
        html = displacy.render(nlp(senString), style="dep", page=True, minify=True)
        
        st.markdown(html, unsafe_allow_html=True)
        #st.components.v1.html(html, width=600, height=1200, scrolling=True)
    
    #Viewing Specific Entities
    #options = {'ents': ['ORG', 'PRODUCT']}
    #displacy.serve(text,style="ent", options=options)
    
            
def visualizeNamedEntities(text):
    doc = nlp(text)

    """
    ent.text	The original entity text
    ent.label	The entity type’s hash value
    ent.label_	The entity type’s string description
    ent.start	The token span’s start index position in the Doc
    ent.end	The token span’s stop index position in the Doc
    ent.start_char	The entity text’s start index position in the Doc
    ent.end_char	The entity text’s stop index position in the Doc
    """
    if doc.ents:
        entList=[]
        for ent in doc.ents:
            entList.append([ent.text, ent.start_char, str(ent.end_char), ent.label_, spacy.explain(ent.label_)])
            
        entDF = pd.DataFrame(entList, columns =["Text", "Start", "End", "Lable", "Description"])
        st.dataframe(entDF, width=1200)  
    else:
        print('No named entities found.')
        
       


def partsOfSpeechTagingVisualization(text):
    doc = nlp(text)
    pofList=[]
    for token in doc:
        pofList.append([token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop])
        
    pofDF = pd.DataFrame(pofList, columns =["Text", "Lemma", "POS", "TAG", "DEP", "SHAPE", "ALPHA", "STOP"])
    st.dataframe(pofDF, width=1200)

#spacy.explain("GPE")    


def main():
    
    #The below code was just used for initial testing.

    raw_text = "Imran Ahmed Khan Niazi HI(M) PP (Urdu/Pashto: عمران احمد خان نیازی; born 5 October 1952) is a Pakistani politician and former cricketer who served as the 22nd prime minister of Pakistan from August 2018 until April 2022, when he was ousted through a no-confidence motion."
    visualizeNamedEntities(raw_text)
    text = nlp(raw_text)
    visulizeSentences(text)
    
    
if __name__ == "__main__":
    main()