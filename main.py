from streamlit_option_menu import option_menu
import requests
from bs4 import BeautifulSoup
import streamlit as st
from gtts import gTTS
from io import BytesIO
import openai

st.set_page_config(page_title="STUDENTBAE", page_icon=":tada:", layout='wide')
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: linear-gradient(to right, #EE5166, #F08EFC );
opacity: 0.8;

}}
</style>
"""


st.markdown(page_bg_img, unsafe_allow_html=True)


openai.api_key = st.secrets["api"]


start_sequence = "\nAI:"
restart_sequence = "\nHuman: "

def ai(prompt,n):

  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=n,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
  )
  st.markdown(response.choices[0],unsafe_allow_html=True)


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

    query = f"{s} filetype:pdf"
    for j in search(query, tld="co.in", num=10, stop=5, pause=2):
        if ".pdf" in j:
            k = j.split("/")

            st.header(k[-1])
            st.markdown(f'<a href="{j}">DOWNLOAD</a>', unsafe_allow_html=True)


def ppt(s):
    try:
        from googlesearch import search
    except ImportError:
        print("No module named 'google' found")

    query = f"{s} filetype:ppt"
    for j in search(query, tld="co.in", num=10, stop=5, pause=2):
        if ".ppt" in j:
            k = j.split("/")

            st.header(k[-1])
            st.markdown(f'<a href="{j}">DOWNLOAD</a>', unsafe_allow_html=True)


def torrent_download(search):
    url = f"https://ww4.1337x.buzz/srch?search={search}"
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


selected2 = option_menu(None, ["Home",'File Search',"AI Assistant"],
                        icons=['house', 'files','robot'],
                        menu_icon="cast", default_index=0, orientation="horizontal")


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




elif selected2 == 'File Search':
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
        ['PDF', 'PPT', 'Courses', 'Research papers', 'Question Papers', 'E-BOOKS']
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


elif selected2 == 'AI Assistant':
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
    
    #n = st.slider('number of lines', 0.0, 1,0, 0.1)
    
    if submit:
        ai(selected,1.0)
