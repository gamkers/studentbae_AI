
from streamlit_option_menu import option_menu
import requests
from bs4 import BeautifulSoup
import streamlit as st
from gtts import gTTS
from io import BytesIO
import openai
from youtubesearchpython import *
import io
import requests
import PyPDF2
from PyPDF2 import PdfReader
import langchain
langchain.verbose = False
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings



st.set_page_config(page_title="STUDENTBAE", page_icon=":tada:", layout='wide')
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: linear-gradient(to right, #000000,#00ADB5 );
opacity: 0.8;

}}
</style>
"""


#st.markdown(page_bg_img, unsafe_allow_html=True)

openai.api_key = st.secrets["api"]
start_sequence = "\nAI:"
restart_sequence = "\nHuman: "

from deta import Deta

def db(link,vectors):
    deta = Deta(st.secrets["data_key"])
    db = deta.Base("Vectors")
    db.put({"link": link, "texts": vectors})

def pdfs(s,n):
    links=[]
    try:
        from googlesearch import search
    except ImportError:
        print("No module named 'google' found")

    query = f"{s} filetype:pdf"
    for j in search(query, tld="co.in", num=1, stop=1, pause=2):
        if ".pdf" in j:
            k = j.split("/")
            print(k[-1])
            print(j)
            
            links.append(j)
    st.markdown("SEARCHING FOR THE DOCUMENTS RELATED TO "+s)
    return links


def pdftotxt(urls):
    texts=""
    for url in urls:
        st.markdown("PROCESSING: "+url)
        response = requests.get(url)

        # Create a file-like object from the response content
        pdf_file = io.BytesIO(response.content)

        # Use PyPDF2 to load and work with the PDF document
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Access the document information
        num_pages = len(pdf_reader.pages)
  

        # Perform further operations with the PDF document as needed
        # For example, extract text from each page

        for page in pdf_reader.pages:
            txt=page.extract_text()
            texts += txt
            db(url,txt)
            
    st.markdown("DATA EXTRACTION DONE")
    return texts

        # Print the extracted text
    
def chunks(texts,q):
    
    st.markdown("DATA TRANFORMATION STARTED")
    st.markdown("TRANFORMING DATA INTO CHUNKS")
    text_splitter = CharacterTextSplitter(separator = "\n",chunk_size = 1000,chunk_overlap  = 200,
    length_function = len,)
    texts = text_splitter.split_text(texts)
    embeddings = OpenAIEmbeddings(openai_api_key=st.secrets["api"])
    docsearchs = FAISS.from_texts(texts, embeddings)
    chain = load_qa_chain(OpenAI(openai_api_key=st.secrets["api"]), chain_type="stuff")
    st.markdown("DATA IS LOADED AS CHUNKS AND READY FOR ANALYTICS PURPOSE")
    query=q
    docs = docsearchs.similarity_search(query)
    title=chain.run(input_documents=docs, question="TITLE of the paper")
    query=chain.run(input_documents=docs, question=query)
    st.write(title)
    st.write(query)
    st.write("FOR REFERENCE:", *urls)
    data=f"{title},{query}"
    audio_bytes=speak(data)
    st.audio(audio_bytes, format='audio/ogg')
    
def answers(query):
    docs = docsearchs.similarity_search(query)
    st.write(chain.run(input_documents=docs, question="TITLE of the paper"))
    st.write(chain.run(input_documents=docs, question=query))
    st.write("FOR REFERENCE:", *urls)
  

def ai(prompt,n):

  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=n,
    max_tokens=2000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
  )
  data = response.choices[0].text
  st.markdown(response.choices[0].text,unsafe_allow_html=True)
  return data

openai.api_key = st.secrets["api"]
start_sequence = "\nAI:"
restart_sequence = "\nHuman: "

def sql(t,q):

  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"###{t}\n#\n### {q}\n",
    temperature=1,
    max_tokens=2000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
  )
  data = response.choices[0].text
  st.markdown(response.choices[0].text,unsafe_allow_html=True)
  return data

def pearson(my_string):
  try:
    from googlesearch import search
    import re
  except ImportError:
    print("No module named 'google' found")
  query = my_string
  pattern = "(instagram|facebook|youtube|twitter|github|linkedin|scholar|hackerrank|tiktok|maps)+\.(com|edu|net|fandom)"
  for i in search(query, tld="co.in", num=20, stop=15, pause=2):
    if (re.search(pattern, i)):
      title=ai(i+"website name in bold",1)
      st.markdown(f'<a href="{i}">view more</a>', unsafe_allow_html=True)
    else:
      print("match not found")
            
def yt(vd):
    customSearch = VideosSearch(vd,limit = 20)
    for i in range(20):
        st.video(customSearch.result()['result'][i]['link'])

def speak(text):
    mp3_fp = BytesIO()
    tts = gTTS(text, lang='en')
    tts.write_to_fp(mp3_fp)
    return mp3_fp


def pdf(s):
    try:
        from googlesearch import search
    except ImportError:
        print("No module named 'google' found")

    query = f"filetype:pdf {s}"
    for j in search(query, tld="co.in", num=10, stop=5, pause=2):
        if ".pdf" in j:
            k = j.split("/")
            for i in k:
                if ".pdf" in i:
                    st.write(i)
            #title=ai(j+" Explain the title and content in short in this link. the title should be in bold",1)
#             st.components.v1.iframe(j)
            st.markdown(f'<a href="{j}">DOWNLOAD</a>', unsafe_allow_html=True)

def webscrap_mcq(command): 
    links=[]
    search = command
    url = "https://www.sanfoundry.com/1000-mysql-database-questions-answers/"
    r = requests.get(url)
    data = BeautifulSoup(r.text, "html.parser")
    for link in data.find_all('a'):
        links.append((link.get('href')))
    sql_mcq=[]
    for text in links:
        if command in str(text):
            if 'http' in str(text):
                url=text
                r = requests.get(url)
                data = BeautifulSoup(r.text, "html.parser")
                temp = data.find("div", class_="entry-content").text
                temp=temp.replace("advertisement","")
                temp=temp.replace("Take MySQL Tests Now!","")
                temp=temp.replace("AnswerAnswer","Answers")
                temp=temp.replace("Subscribe Now: MySQL Newsletter | Important Subjects Newsletters","")
                temp=temp.replace("Check this: Programming MCQs | Information Technology Books","")
                temp=temp.replace("Note: Join free Sanfoundry classes at Telegram or Youtube","")
                temp=temp.replace("Sanfoundry Certification Contest of the Month is Live. 100+ Subjects. Participate Now!","")
                temp=temp.replace("Sanfoundry Global Education & Learning Series – MySQL Database.To practice all areas of MySQL Database, here is complete set of 1000+ Multiple Choice Questions and Answers.","")
                clean=temp.split("«")
                clean1=clean[0]
                clean2=clean1.split("Take MySQL Practice Tests")
                
                st.markdown(clean2[0],unsafe_allow_html=True)
def ppt(s):
    try:
        from googlesearch import search
    except ImportError:
        print("No module named 'google' found")

    query = f"filetype:ppt {s}"
   
    for j in search(query, tld="co.in", num=10, stop=5, pause=2):
        if ".ppt" in j:
            k = j.split("/")

            title=ai(j+" Explain the title and content in short in this link. the title should be in bold",1)
#             st.components.v1.iframe(j)
            st.markdown(f'<a href="{j}">DOWNLOAD</a>', unsafe_allow_html=True)


def torrent_download(search):
    url = f"https://1377x.xyz/fullsearch?q={search}"
    r = requests.get(url)
    data = BeautifulSoup(r.text, "html.parser")
    links = data.find_all('a', style="font-family:tahoma;font-weight:bold;")

    torrent = []
    ogtorrent = []
    for link in links:
        st.write(link.text)
        torrent.append(f"https://ww4.1337x.buzz{link.get('href')}")
        url = f"https://ww4.1337x.buzz{link.get('href')}"
        r = requests.get(url)
        data = BeautifulSoup(r.text, "html.parser")
        links = data.find_all('a')
        for link in links:
            link = link.get('href')
            if "magnet" in str(link):
                st.markdown(f'<a href="{str(link)}">DOWNLOAD</a>', unsafe_allow_html=True)
            if "torrents.org" in str(link):
                ogtorrent.append(str(link))


#                 st.markdown(f'<a href="{str(link)}">DOWNLOAD</a>',unsafe_allow_html=True)



hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden; }
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

def display(data):
  
  st.image("search1.png")
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
  if submit:
    if "PDF" in data:
      pdf(selected)
    elif "PPT" in data:
      ppt(selected)
    elif "Courses" in data:
      st.write('''Fair Use Act Disclaimer
         This site is for educational purposes only!!
                            **FAIR USE**
      Copyright Disclaimer under section 107 of the Copyright Act 1976, allowance 
      is made for “fair use” for purposes such as criticism, comment, news reporting, teaching, 
      scholarship, education and research.Fair use is a use permitted by copyright statute that might
      otherwise be infringing. Non-profit, educational or personal use 
      tips the balance in favor of fair use. ''')
      torrent_download(selected)
      
                  

    elif "Research papers" in data:
      selected = f"{selected} research papers"
      pdf(selected)
    elif "Question Papers" in data:
      selected = f"{selected} Question Papers"
      pdf(selected)
    elif "E-BOOKS" in data:
      selected = f"{selected} BOOK"
      pdf(selected)
    elif "Hacker Rank" in data:
      st.write(f"[OPEN >](https://www.hackerrank.com/domains/{selected})")
    elif "MCQ's" in data:
      webscrap_mcq(selected)


    



    

    


def webscrape_MainNews(type):
    info = ["HEAD LINES", "NEWS", "AUTHOR", "DATE", "COUNTRY", "CATEGORY"]
    Date = []
    news = []
    authors = []
    catogory = []
    headlines = []
    country = []
    images=[]
    for i in range(0, 5):
        url = f"https://www.ndtv.com/{type}/page-{i}"
        r = requests.get(url)
        data = BeautifulSoup(r.text, "html.parser")
        hl = data.find_all('h2', class_="newsHdng")
        new = data.find_all('p', class_="newsCont")
        author = data.find_all('span', class_="posted-by")
        image = data.find_all('div', class_="news_Itm-img")
        for h in hl:
            headlines.append(h.text)
        for i in new:
            i = i.text.replace("\n", "")
            news.append(i)
        for j in author:
            j = j.text.split("|")
            j = j[0]
            if "by" in j:
                s = j.split("by")
                j = s[-1]
            authors.append(j[:-3])
        for k in author:
            k = k.text.split("|")
            k = k[-1]
            k = k.split(",")
            if len(k) == 2:
                Date.append(",".join(k[0:2])[:-112])
            else:
                Date.append(",".join(k[0:2]))
        for l in new:
            catogory.append(type)
        for m in author:
            m = m.text.split("|")
            m = m[-1]
            m = m.split(",")
            m = m[-1]
            country.append(m[:-112].replace("2022", "NA"))

        for im in image:
            link =im.find('img').get('src')
            
            images.append(link)

    data = [list(item) for item in list(zip(headlines, news, authors, Date, country, catogory,images))]

    return data

def webscrape_News(cat,n):
    Date = []
    news = []
    authors = []
    catogory = []
    headlines = []
    country = []
    images=[]
    for i in range(1, 5):
        url = f"https://www.ndtv.com/page/topic-load-more/from/allnews/type/news/page/{i}/query/{cat}"
        r = requests.get(url)
        data = BeautifulSoup(r.text, "html.parser")
        hl = data.find_all('div', class_="src_itm-ttl")
        new = data.find_all('div', class_="src_itm-txt")
        author = data.find_all('span', class_="src_itm-stx")
        image =data.find_all('img', class_="img_brd marr10")

        for h in hl:
            headlines.append(h.text)
        for i in new:
            i = i.text
            news.append(i[25:-20])
        for j in author:
            j = j.text.split("|")
            j = j[0]
            if "by" in j:
                s = j.split("by")
                j = s[-1]
                authors.append(j)
            else:
                authors.append(j[25:])
        for k in author:
            k = k.text.split("|")
            k = k[-1]
            Date.append(k[:-20])
        for l in new:
            catogory.append("Sports")
        for m in author:
            country.append("India")
        for im in image:
            link = im.get('src')
            images.append(link)

    data = [list(item) for item in list(zip(headlines, news, authors, Date, country, catogory,images))]

    return data



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


import streamlit as st

def register():
    st.title("User Registration")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        # Check if passwords match
        if password == confirm_password:
            # TODO: Add code to store username and password in the database
            st.success("Registration Successful. Please log in.")
        else:
            st.error("Passwords do not match")

def login():
    st.title("User Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # TODO: Add code to check username and password in the database
        if valid_credentials(username, password):
            st.success("Login Successful")
            # TODO: Add code to redirect to the user's dashboard
                        
            with st.sidebar:
              
            
            
            def lottieurl(url):
                r = requests.get(url)
                if r.status_code != 200:
                    return None
                return r.json()
            
            lottie_coding = lottieurl("https://assets10.lottiefiles.com/packages/lf20_i9mtrven.json")
            lottie_coding2 = lottieurl("https://assets8.lottiefiles.com/packages/lf20_2LdLki.json")
            lottie_coding3 = lottieurl("https://assets8.lottiefiles.com/packages/lf20_oyi9a28g.json")
            
            if selected2 == 'Home':
                st.image("logofinal.png")
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
                        st.image("hero.png")
            
                with st.container():
                    st.write("---")
                    left_coloumn, right_coloumn = st.columns(2)
                    with left_coloumn:
                        st.image("hero3.png")
            
                    with right_coloumn:
                        st.header("WHY STUDENTBAE?")
                        st.write("##")
                        st.write(
                            """
                            There is a huge dataflow on the internet and it makes deficult to search notes or resources for students so we collect notes from all over the internet and categorised the resorces provide them to the users, we constantly try to update more features fix issues faced by students. The features listed belowr""")
            
            
            
            
            elif selected2 == 'Search':
                st.image("search1.png")
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
                    elif "MCQ's" in options:
                        
                        webscrap_mcq(selected)
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
            elif selected2 == "SQL":
              st.image("search1.png")
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
              t = st.text_input("TABLE DETAILS", "")
              q = st.text_input("What you want?", "")
              submit = st.button("SEARCH")
              if submit:
                sql(t,q)
            elif selected2 == 'OSINT':
              st.image("search1.png")
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
                st.image("colab.png")
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
                    cnt=ai(selected,1.0)
                  
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
                    elif "MCQ's" in options:
                        
                        webscrap_mcq(selected)
            elif selected2 == 'AdvanceGPT':
                st.image("colab.png")
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
                st.image("colab.png")
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
                
                st.image("colab.png")
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

        else:
            st.error("Invalid username or password")

def valid_credentials(username, password):
    # TODO: Add code to validate username and password against the database
    # Return True if the credentials are valid, False otherwise
    return True

def main():
    st.header("User Authentication System")
    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)
    selected2 = option_menu(None, ["Home","Assistant",'Search','AdvanceGPT','PDF', 'PPT', 'Courses', 'Research papers','Question Papers', 'E-BOOKS',"SQL",'OSINT',"DOCSGPT",'NEWSIFY'],
                                      icons=['house','robot','files'],
                                      menu_icon="cast", default_index=2, orientation="vertical")

    if choice == "Login":
        login(selected2)
    elif choice == "Register":
        register()

if __name__ == "__main__":
    main()


            

    
   
        



