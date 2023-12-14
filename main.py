
from streamlit_option_menu import option_menu
import requests
import streamlit as st
import openai
from youtubesearchpython import *
import requests
from PyPDF2 import PdfReader
import langchain
langchain.verbose = False
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from scripts.news import *
from scripts.login import *

st.set_page_config(page_title="STUDENTBAE", page_icon=":tada:", layout='wide')
from scripts.functions  import *


def displays(data):
    voice = []
    for i in range(5):
        data1 = data[i][1].split(":")
        voice.append(f"news number{str(i + 1)}," + data1[0] + '.')
    audio_bytes = speak('.'.join(map(str, voice)))
    st.audio(audio_bytes, format='audio/ogg')
    if submit:
        for i in data:
            for j in i:
                if selected in j:
                    st.header(f' {i[0]}')

                    original_title = f'<p style="font-family:Times New Roman; font-size: 18px;">{i[1]}</p>'
                    st.markdown(original_title, unsafe_allow_html=True)

                    st.write(f'AUTHOR & DATE: {i[2]} | {i[3]}')
                    st.write("_______________________________________________________________________________")
                break

    for i in range(n):
        data1 = data[i][0].split(";")
        st.header(f'{data1[0]}')
        with st.container():
            left_coloumn, right_coloumn = st.columns(2)
            with left_coloumn:
                st.image(data[i][6], width=355)
            with right_coloumn:
                st.write("                                                                                ")
                st.write("                                                                                ")
                original_title = f'<p style="font-family:Times New Roman;  font-size: 18px;">{data[i][1]}</p>'
                st.markdown(original_title, unsafe_allow_html=True)
                st.write(f'AUTHOR & DATE: {data[i][2]} | {data[i][3]}')

        st.write("_______________________________________________________________________________")

def answers(query):
    docs = docsearchs.similarity_search(query)
    st.write(chain.run(input_documents=docs, question="TITLE of the paper"))
    st.write(chain.run(input_documents=docs, question=query))
    st.write("FOR REFERENCE:", *urls)


with st.sidebar:
  selected2 = option_menu(None, ["Login","Register","Home","Assistant",'AdvanceGPT',"Interview",'OSINT',"DOCSGPT",'NEWSIFY','About'],
                          icons=['person-fill', 'person-plus-fill', 'house-fill', 'robot', 'book-half', "code-slash", 'globe2', "file-earmark-richtext-fill", 'newspaper','person-fill'],
                          menu_icon="cast", default_index=2, orientation="vertical")


def lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json() 


page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: linear-gradient(to right, #000000, #000000);
opacity: 0.8;

}}
.stButton>button {{
    color: #FFFFFF;
    border-radius: 10%;
    height: 3em;
    width: 6em;
    background:	#6528F7;
    border-radius: 16px;
    box-shadow: 0 4px 30px #000000;
    backdrop-filter: blur(12.1px);
    -webkit-backdrop-filter: blur(12.1px);
    border: 1px solid #FF00FF;
}}
</style>
"""



st.markdown(page_bg_img, unsafe_allow_html=True)

openai.api_key = st.secrets["api"]
start_sequence = "\nAI:"
restart_sequence = "\nHuman: "


lottie_coding = lottieurl("https://assets10.lottiefiles.com/packages/lf20_i9mtrven.json")
lottie_coding2 = lottieurl("https://assets8.lottiefiles.com/packages/lf20_2LdLki.json")
lottie_coding3 = lottieurl("https://assets8.lottiefiles.com/packages/lf20_oyi9a28g.json")
try:
    if selected2 == 'Login':
        login()
    elif selected2 == 'Register':
        register()
    elif selected2 == 'About':
        st.image("images/logofinal.png")
        with st.container():
            st.write("---")
            left_coloumn, right_coloumn = st.columns(2)
            with left_coloumn:
                st.subheader("LEARNING The Journey Of The Life Time")
                st.title("STUDENTBAE")
                st.write(
                    "STUDENTBAE is a web-based application that helps students assist with their tasks and make their lives easier. in recent eras, the educational system evolved a lot and most organisations moved from pen and paper method to totally to online mode, So we help students to get their resources easily and quickly. We provide our users with a personalized search engine for studies, there students can get PDFs, Slides, Notes, Courses, Research  papers, Question Papers, and E-books.")
                st.write("[DOWNLOAD NOW >](https://newsify.en.uptodown.com/android)")

            with right_coloumn:
                st.image("images/hero.png")

        with st.container():
            st.write("---")
            left_coloumn, right_coloumn = st.columns(2)
            with left_coloumn:
                st.image("images/hero3.png")

            with right_coloumn:
                st.header("WHY STUDENTBAE?")
                st.write("##")
                st.write(
                    """
                    There is a huge dataflow on the internet and it makes deficult to search notes or resources for students so we collect notes from all over the internet and categorised the resorces provide them to the users, we constantly try to update more features fix issues faced by students. The features listed belowr""")




    elif selected2 == 'Home':
    

        st.image("images/search1.png")
        def local_css(file_name):
            with open(file_name) as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


        def remote_css(url):
            st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)


        def icon(icon_name):
            st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)


        local_css("style.css")
        remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')
        
        st.write('''Explore seamlessly with our advanced search! Find PDFs, PPTs, question papers, research papers, and ebooks effortlessly. 
        Simplify your learning journey with precise searches – discover, learn, excel!!''')

        form = st.form(key='my-form')

        selected = form.text_input("What are you Looking for?", "")
        submit = form.form_submit_button("SEARCH")

        options = st.multiselect(
            'What you Looking for?',
            ['PDF', 'PPT', 'Courses', 'Research papers','Hacker Rank',"MCQ's",'Question Papers', 'E-BOOKS']
        )

        n = st.slider('File Count', 0, 130, 25)

        if submit:
            if "PDF" in options:
                pdf(selected)
            elif "PPT" in options:
                ppt(selected)
            elif "Courses" in options:
                st.write('''Fair Use Act Disclaimer
            This site is for educational purposes only!!
                                **FAIR USE**
        Copyright Disclaimer under section 107 of the Copyright Act 1976, allowance 
        is made for “fair use” for purposes such as criticism, comment, news reporting, teaching, 
        scholarship, education and research.Fair use is a use permitted by copyright statute that might
        otherwise be infringing. Non-profit, educational or personal use 
        tips the balance in favor of fair use. ''')
                torrent_download(selected)
            elif "Research papers" in options:
                selected = f"{selected} research papers"
                pdf(selected)
            elif "Question Papers" in options:
                selected = f"{selected} Question Papers"
                pdf(selected)
            elif "E-BOOKS" in options:
                selected = f"{selected} BOOK"
                pdf(selected)
            elif "Hacker Rank" in options:
                st.write(f"[OPEN >](https://www.hackerrank.com/domains/{selected})")
        
    elif selected2 == "PDF":
        display("PDF")
    elif selected2 == "PPT":
        display("PPT")
    elif selected2 == "Courses":
        display("Courses")
    elif selected2 == "Research papers":
        display("Research papers")
    elif selected2 == "Question Papers":
        display("Question Papers")
    elif selected2 == "Hacker Rank":
        display("Hacker Rank")
    elif selected2 == "MCQ's":
        display("MCQ's")
    elif selected2 == 'E-BOOKS':
        display('E-BOOKS')
    elif selected2 == "Interview":
        st.image("images/search1.png")
        def local_css(file_name):
                with open(file_name) as f:
                    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        def remote_css(url):
                st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)
        def icon(icon_name):
                st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)
            
        local_css("style.css")
        remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')
        #   form = st.form(key='my-form')
        t = st.text_input("Mention your job Role", "")
        submit = st.button("SEARCH")
        if submit:
            ai_HR(t)
    elif selected2 == 'OSINT':
        st.image("images/search1.png")
        def local_css(file_name):
                with open(file_name) as f:
                    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        def remote_css(url):
                st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)
        def icon(icon_name):
                st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)
            
        local_css("style.css")
        remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')
        #   form = st.form(key='my-form')
        t = st.text_input("USERNAME", "")
        submit = st.button("SEARCH")
        if submit:
            pearson(t)
        
    
    elif selected2 == 'Assistant':
        st.image("images/colab.png")
        def local_css(file_name):
            with open(file_name) as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


        def remote_css(url):
            st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)


        def icon(icon_name):
            st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)


        local_css("style.css")
        remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')


        form = st.form(key='my-form')

        selected = form.text_input("", "")

        submit = form.form_submit_button("SEARCH")
        options = st.multiselect(
            'ASSIST WITH',
            ['PDF', 'PPT', 'Research papers','Question Papers', 'E-BOOKS','Videos'])
        
        #n = st.slider('number of lines', 0.0, 1,0, 0.1)
        
        if submit:
            #cnt=ai(selected,1.0)
            cnt=selected
            content=ai_palm(selected)
            if "PDF" in options:
                pdf(cnt)
            elif "PPT" in options:
                ppt(cnt)
            elif "Videos" in options:
                yt(cnt)
            elif "Courses" in options:
                st.write('''Fair Use Act Disclaimer
            This site is for educational purposes only!!
                                **FAIR USE**
        Copyright Disclaimer under section 107 of the Copyright Act 1976, allowance 
        is made for “fair use” for purposes such as criticism, comment, news reporting, teaching, 
        scholarship, education and research.Fair use is a use permitted by copyright statute that might
        otherwise be infringing. Non-profit, educational or personal use 
        tips the balance in favor of fair use. ''')
                torrent_download(selected)
            elif "Research papers" in options:
                selected = f"research papers {cnt}"
                pdf(selected)
            elif "Question Papers" in options:
                selected = f"Question Papers {cnt}"
                pdf(selected)
            elif "E-BOOKS" in options:
                selected = f"BOOK {cnt}"
                pdf(selected)
            elif "Hacker Rank" in options:
                st.write(f"[OPEN >](https://www.hackerrank.com/domains/{selected})")
            
    elif selected2 == 'AdvanceGPT':
        st.image("images/colab.png")
        def local_css(file_name):
            with open(file_name) as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


        def remote_css(url):
            st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)


        def icon(icon_name):
            st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)


        local_css("style.css")
        remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

        selected = st.text_input("Document Searcher", "")
        selected1 = st.text_input("question", key="widget2")
        submit = st.button("SEARCH")

        n = st.slider('number of documents', 1, 1, 10, 1)

        if submit:
            urls = pdfs(selected, 1)
            texts = pdftotxt(urls)
            chunks(texts,selected1)
    
    elif selected2 == "DOCSGPT":
        st.image("images/colab.png")
        def local_css(file_name):
            with open(file_name) as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


        def remote_css(url):
            st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)


        def icon(icon_name):
            st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)


        local_css("style.css")
        remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')
    
        from PyPDF2 import PdfReader
        options = st.multiselect(
            'file type',
            ['CSV', 'PDF'])
        if "PDF" in options:
            uploaded_file = st.file_uploader("Upload PDF", type="pdf")
            pdf_readed = '' 
            if uploaded_file is not None:
                # Process the uploaded PDF file
                # You can save it, read its content, or perform any other necessary operations
                # For example, if you want to read the content using PyPDF2:
                reader = PdfReader(uploaded_file)

                raw_text = ''
                for i, page in enumerate(reader.pages):
                    text = page.extract_text()
                    if text:
                        raw_text += text

                text_splitter = CharacterTextSplitter(        
                separator = "\n",
                chunk_size = 1000,
                chunk_overlap  = 200,
                length_function = len,
                )
                texts = text_splitter.split_text(raw_text)
                embeddings = OpenAIEmbeddings(openai_api_key=st.secrets["api"])
                docsearchs = FAISS.from_texts(texts, embeddings)
                chain = load_qa_chain(OpenAI(openai_api_key=st.secrets["api"]), chain_type="stuff")

        elif "CSV" in options:
            import pandas as pd
            uploaded_file = st.file_uploader("Upload PDF", type="csv")
            if uploaded_file is not None:
                # Read the CSV file into a pandas DataFrame
                df = pd.read_csv(uploaded_file)
                # Convert DataFrame to text
                text = df.to_string(index=False)
                data = text
                embeddings = OpenAIEmbeddings(openai_api_key=st.secrets["api"])
                docsearchs = FAISS.from_texts(data, embeddings)
                chain = load_qa_chain(OpenAI(openai_api_key=st.secrets["api"]), chain_type="stuff")

            
        form = st.form(key='my-form')

        selected = form.text_input("TYPE YOUR QUESTION", "")
        submit = form.form_submit_button("SEARCH")
        if submit:
            query = selected
            docs = docsearchs.similarity_search(query)
            st.write(chain.run(input_documents=docs, question=query))

    elif selected2 == 'NEWSIFY':
        
        st.image("images/colab.png")
        def local_css(file_name):
            with open(file_name) as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


        def remote_css(url):
            st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)


        def icon(icon_name):
            st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)


        local_css("style.css")
        remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')
    
        st.header("Explore The World")
        form = st.form(key='my-form')
        selected = form.text_input("", "")
        submit = form.form_submit_button("SEARCH")
        options = st.multiselect(
                'What you Looking for?',
                ['Latest','Global','South Indian','Sports', 'Political', 'Technology','Science', 'Music', 'LifeStyle', "Entertainment", 'Crime', 'Food', 'Business']
                )

        n = st.slider('News Count', 0, 130, 25)
        
        
        if submit:
        
                data = webscrape_News(selected, n)
                voice = []
                for i in range(n):
                    data1 = data[i][0].split(":")
                    voice.append(f"news number{str(i + 1)}," + data1[0] + '.')
                audio_bytes = speak('.'.join(map(str, voice)))
                st.audio(audio_bytes, format='audio/ogg')
                for i in range(n):
                    data1 = data[i][0].split(":")
                    st.header(f'{data1[0]}')
                    with st.container():
                        left_coloumn, right_coloumn = st.columns(2)
                        with left_coloumn:
                            st.image(data[i][6], width=355)
                        with right_coloumn:
                            st.write("                                                                                ")
                            st.write("                                                                                ")
                            original_title = f'<p style="font-family:Times New Roman;  font-size: 18px;">{data[i][1]}</p>'
                            st.markdown(original_title, unsafe_allow_html=True)
                            st.write(f'AUTHOR & DATE: {data[i][2]} | {data[i][3]}')

                    st.write("_______________________________________________________________________________")



        if "Global" in options:
            data=webscrape_MainNews("world-news")
            displays(data)

        elif "LifeStyle" in options:
            data=webscrape_News("life-style",n)
            displays(data)
        elif "Sports" in options:
            data=webscrape_News("Sports",n)
            displays(data)
        elif "Political" in options:
            data=webscrape_News("politics",n)
            displays(data)
        elif "Crime" in options:

            data=webscrape_News("crime",n)
            displays(data)
        elif "Music" in options:
            data=webscrape_News("music",n)
            displays(data)
        elif "Technology" in options:
            data = webscrape_News("technology",n)
            displays(data)

        elif "Food" in options:
            data = webscrape_News("food",n)
            displays(data)
        elif "Business" in options:
            data = webscrape_News("business",n)
            displays(data)
        elif "Entertainment" in options:
            data = webscrape_News("entertainment",n)
            displays(data)
            
        elif "Latest" in options:
            data = webscrape_MainNews("latest")
            displays(data)
            
        elif "Indian" in options:
            data = webscrape_MainNews("indian")
            displays(data)
        elif "South Indian" in options:
            data = webscrape_MainNews("south")
            displays(data)
        elif "Science" in options:
            data = webscrape_MainNews("science")
            displays(data)
except Exception as e:
    st.error(f"An error occurred: {e}")
 
    


            

    
   
        


