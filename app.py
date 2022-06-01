import streamlit as st
import validators
import lexicalAnalysis
import wikipediaScraper
import relationshipExtrator
import namedEntityRecognition


def isWikiURL(inputUrl): #This functions checks wheather URL belongs to  Wikipedia or not
    inputUrl = inputUrl[0:30]
    WIKI_URL = "https://en.wikipedia.org/wiki/"
    if(inputUrl==WIKI_URL):
        return True
    else:
        return False

def customizeUI(): #This function is for customization the UI of the interface

    #Set the page title and icon
    st.set_page_config(
        page_title="WikiSemAnalysis",
        page_icon="🔥", 
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items=None
    )

    #For Hiding the menu button
    st.markdown(""" <style> 
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style> """, unsafe_allow_html=True)

    #For Condensing the layout: Reducing the padding between components using the following snippet 
    padding = 1
    st.markdown(f""" <style>
        .reportview-container .main .block-container{{
            padding-top: {padding}rem;
            padding-right: {padding}rem;
            padding-left: {padding}rem;
            padding-bottom: {padding}rem;
        }} </style> """, unsafe_allow_html=True)

    st.image('headerimg.jpg') # Img Reference:https://erpinnews.com/wp-content/uploads/2017/12/amazonai-hiring-banner-1440x425-1-1.jpg

# Main Function

def main():
    customizeUI()
    st.title("Wikipedia Semantic Analysis System")
    st.markdown("**Welcome** 😊")
    
    menu = ["Semantic Analysis", "About"]
    selectedTab = st.sidebar.selectbox("Menu", menu)
    
    if selectedTab == "Semantic Analysis": 
        st.subheader("Semantic Analysis")
        # Form
        with st.form(key='wikiLinkForm'):
            inputWikiLink = st.text_area("-->Paste Wikipedia Article URL here:")
            fetchTweetsBtn = st.form_submit_button(label='Submit')
            if fetchTweetsBtn:
                if validators.url(inputWikiLink):
                    # URL is valid
                    if isWikiURL(inputWikiLink):
                        # URL is of Wikipedia only
                        
                        st.info("Fetching Article :hourglass:")

                        #WikiPedia Article Scraping
                        page = wikipediaScraper.getWikiPage(inputWikiLink)
                        title = page.find(id="firstHeading")
                        st.sidebar.markdown("**Article Title: **"+title.string)
                        
                        text = wikipediaScraper.extractParagraphsFromPage(page)
                        tokens = lexicalAnalysis.tokenization(text)
                        
                        # layout
                        col1,col2= st.columns(2) # 2 columns
                        with col1:
                            
                            st.info("Word Cloud")
                            lexicalAnalysis.drawWordClud(tokens)
                            
                            st.info("Top most frequently occuring words")
                            lexicalAnalysis.mostCommonWords(tokens)
                            
                            st.info("Named Entity Recognition")
                            namedEntityRecognition.visualizeNamedEntities(text)
                            namedEntityRecognition.visulizeSentences(text,"ent")
                            
                        with col2:
                            
                            st.info("Entity Relationship Graph")
                            relationshipExtrator.plotEntityPairsGraph()
                            
                            st.info("POS Tagging")
                            namedEntityRecognition.partsOfSpeechTagingVisualization(text)
                            
                            st.info("Dependency Parsing")
                            namedEntityRecognition.visulizeSentences(text,"dep")
                    else:
                        # Valid URL doesn't belong to wikipedia
                        st.error("Please Enter a Valid URL of Wikipedia Article only")     
                else:
                    # URL is invalid
                    st.error("Please Enter a Valid URL")
    elif selectedTab == "About":
        st.subheader("About")
        st.markdown("This application performs semantic analysis of wikipedia (https://www.wikipedia.org/) articles.")
    else:
        pass 
                    
                    
if __name__ == "__main__":
    main()