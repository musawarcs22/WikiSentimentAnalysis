# import required modules
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import spacy
from spacy import displacy
nlp = spacy.load('en_core_web_sm')
import csv
import pandas as pd



def getWikiPage(url):
    # Specify url of the web page
    source = urlopen(url).read()


    # Make a soup 
    soup = BeautifulSoup(source,'lxml')
    #print(set([text.parent.name for text in soup.find_all(text=True)]))
    return soup

def extractParagraphsFromPage(page):
    # Extracting the plain text content from paragraphs
    text = ''
    for paragraph in page.find_all('p'):
        text += paragraph.text

    #print(text)

    #Initial Cleaning
    text = re.sub(r'\[.*?\]+', '', text) #Droping footnote superscripts in brackets 
    text = text.replace('\n', '') # Replace ‘\n’ (a new line) with ‘’ (an empty string)
    return text

def convertTextToSentencesAndStore(text):
    #Convert the Text into Sentences
    sentences = [[i] for i in nlp(text).sents]
    #print(sentences)


    #Storing sentences in a csv file
    myheaders = ['sentence']
    myvalues = sentences
    filename = 'wiki_text.csv'
    with open(filename, 'w',newline='') as myfile:
        writer = csv.writer(myfile)
        writer.writerow(myheaders)
        writer.writerows(myvalues)

    

def main():
    
    #The below code was just used for initial testing
    page = getWikiPage('https://en.wikipedia.org/wiki/Imran_Khan')
    title = page.find(id="firstHeading")
    print(title.string)
    
    text = extractParagraphsFromPage(page)
    convertTextToSentencesAndStore(text)
    print(text)

if __name__ == "__main__":
    main()














"""

#Convert the Text into Sentences
for i in nlp(text).sents:
    print([i])
"""




"""

csv_sentences = pd.read_csv("wiki_text.csv")
#print(csv_sentences)

print(csv_sentences.shape)
print(csv_sentences['sentence'].sample(5)) #returns random samples of items from an axis of an object 

print("***************")

#Sentense Segmentation

doc = nlp("My name is Hami.")

for tok in doc:
  print(tok.text, "...", tok.dep_)

"""







