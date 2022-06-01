import spacy
import streamlit as st
from collections import Counter #Counts item frequencies in a list
from tabulate import tabulate #Organizes data in a table view
#nlp = spacy.load('en_core_web_sm')
nlp = spacy.load('en_core_web_md')
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd



def tokenization(text):
    #Tokenizes the text
    
    tokens = nlp(text)

    #Print a small selection of tokens
    #print("Tokens: ", tokens)

    #Print the attributes
    table = []
    for token in tokens[100:200]: #For the table, only taking some tokens
        table.append([token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop])

    #Using tabulate to show a formatted table
    #print(tabulate(table, headers=['Text', 'Lemma', 'POS', 'Tag', 'Dep', 'Shape', 'Is Alpha', 'Is Stop']))
    
    return tokens

def mostCommonWords(tokens):
    """
    Working of this Fun:
    iterating through all the tokens, 
    converting tokens to lowercase text, 
    adding all text that is not punctuation,white space, stop word to a list 
    counting top words
    """
    words = []
    for token in tokens:
        if(not token.is_punct and " " not in token.text and not token.is_stop):
            words.append(token.text.lower())

    topWords = []
    topWords = Counter(words).most_common()
    #print("TopWords")
    #print(topWords)
    #print(type(topWords))
    
    wordCountDF = pd.DataFrame(topWords, columns =['Word', 'Frequency'])
    #st.sidebar.dataframe(wordCountDF, width=900)
    st.dataframe(wordCountDF, width=2200)
    #print(tabulate(topWords, headers=['Word', 'Count']))
    


def drawWordClud(tokens):
    wordList = ""
    for token in tokens:
        if(not token.is_punct and " " not in token.text and not token.is_stop):
            wordList= wordList + ", " + token.text.lower()
    #print(wordList)
            
    # Create and generate a word cloud image:
    wordcloud = WordCloud(width=800, height=400).generate(wordList)


    # Display the generated image:
    fig, ax = plt.subplots(figsize = (20, 10))
    ax.imshow(wordcloud)
    plt.axis("off")
    st.pyplot(fig)
    
        

def main():
    pass

if __name__ == "__main__":
    main()