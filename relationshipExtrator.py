# importing required modules
import spacy
from spacy import displacy
nlp = spacy.load('en_core_web_sm')
import pandas as pd
from tqdm import tqdm
from spacy.matcher import Matcher 
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import streamlit as st


# The following function reads sentence and return two entities (entity pair)
def get_entities(sent):
      ## chunk 1
  ent1 = ""
  ent2 = ""

  prv_tok_dep = ""    # dependency tag of previous token in the sentence
  prv_tok_text = ""   # previous token in the sentence

  prefix = ""
  modifier = ""

  
  for tok in nlp(sent):
    ## chunk 2
    # if token is a punctuation mark then move on to the next token
    if tok.dep_ != "punct":
      # check: token is a compound word or not
      if tok.dep_ == "compound":
        prefix = tok.text
        # if the previous word was also a 'compound' then add the current word to it
        if prv_tok_dep == "compound":
          prefix = prv_tok_text + " "+ tok.text
      
      # check: token is a modifier or not
      if tok.dep_.endswith("mod") == True:
        modifier = tok.text
        # if the previous word was also a 'compound' then add the current word to it
        if prv_tok_dep == "compound":
          modifier = prv_tok_text + " "+ tok.text
      
      ## chunk 3
      if tok.dep_.find("subj") == True:
        ent1 = modifier +" "+ prefix + " "+ tok.text
        prefix = ""
        modifier = ""
        prv_tok_dep = ""
        prv_tok_text = ""      

      ## chunk 4
      if tok.dep_.find("obj") == True:
        ent2 = modifier +" "+ prefix +" "+ tok.text
        
      ## chunk 5  
      # update variables
      prv_tok_dep = tok.dep_
      prv_tok_text = tok.text

  return [ent1.strip(), ent2.strip()]


def getEntityPairsList():
    
    entity_pairs = []
    csv_sentences = pd.read_csv("wiki_text.csv")

    for i in tqdm(csv_sentences["sentence"]):
        entity_pairs.append(get_entities(i))
    
    #print(entity_pairs)
    return entity_pairs


#Geting relations for each entity pairs of the article
def get_relation(sent):
    
  doc = nlp(sent)

  # Matcher class object 
  matcher = Matcher(nlp.vocab)

  #define the pattern 
  pattern = [{'DEP':'ROOT'}, 
            {'DEP':'prep','OP':"?"},
            {'DEP':'agent','OP':"?"},  
            {'POS':'ADJ','OP':"?"}] 

  matcher.add("matching_1",[pattern]) 

  matches = matcher(doc)
  k = len(matches) - 1

  span = doc[matches[k][1]:matches[k][2]] 

  return(span.text)



def plotEntityPairsGraph():
    
    csv_sentences = pd.read_csv("wiki_text.csv")
    relations = [get_relation(i) for i in tqdm(csv_sentences['sentence'])]
    
    #print(pd.Series(relations).value_counts()[:50])
    
    # extract subject
    source = [i[0] for i in getEntityPairsList()]
    # extract object
    target = [i[1] for i in getEntityPairsList()]
    kg_df = pd.DataFrame({'source':source, 'target':target, 'edge':relations})

    #############################################################

    #Creating a directed-graph from a dataframe
    #The following code shows all relations which makes a clutter on the screen.

    """
    G=nx.from_pandas_edgelist(kg_df, "source", "target", 
                            edge_attr=True, create_using=nx.MultiDiGraph())

    matplotlib.use('TkAgg')
    plt.figure(figsize=(12,12))
    pos = nx.spring_layout(G)
    nx.draw(G, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos = pos)
    plt.show()
    """
    #############################################################
    #The following code shows only four relations that are "said", "has", "became", "nominated".


    G=nx.from_pandas_edgelist(kg_df[(kg_df['edge']=="said") | (kg_df['edge']=="has") | (kg_df['edge']=="became") | (kg_df['edge']=="nominated")], "source", "target", 
                            edge_attr=True, create_using=nx.MultiDiGraph())

    matplotlib.use('TkAgg')
    plt.figure(figsize=(20,10))
    pos = nx.spring_layout(G, k = 0.5) # k regulates the distance between nodes
    nx.draw(G, with_labels=True, node_color='lightgreen', node_size=2500, edge_cmap=plt.cm.Blues, pos = pos)
    #st.header('Charts')
    st.pyplot(plt)
    

def main():
    
    pass

if __name__ == "__main__":
    main()
