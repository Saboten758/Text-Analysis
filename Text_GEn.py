import streamlit as st
import requests
from streamlit_lottie import st_lottie
from gtts import gTTS
from fpdf import FPDF
from transformers import pipeline, set_seed
import zipfile

print("LOADING...")
generator = pipeline('text-generation', model='gpt2')
set_seed(41)

st.set_page_config(page_title="Text Generation", page_icon="📖", layout="wide")
def load_url(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        else:
            return r.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching URL: {e}")
        return None

lottie_anim = load_url("https://lottie.host/502b1b25-0fa6-41ca-a9c2-ad0b12947ae8/uoZ79rCdmU.json")
lottie_anim2=load_url("https://lottie.host/654b0be8-0faf-4b11-94c2-aa0a6a1aa417/f8Nr08Bedw.json")
def generate(txt,z):
    try:
        x = generator(txt, max_length=z, num_return_sequences=5, truncation=True)
        output = x[0]['generated_text']
        try:
            lang = 'en-us'
            tts = gTTS(text=output, lang=lang, slow=False)
            tts.save("output.mp3")
            st.write("Click Here to play:")
            st.audio("output.mp3", format="audio/mp3")
            with open("output.mp3", "rb") as f:
                d = f.read()
                st.download_button("Download Audio", data=d, key="audio_download", file_name='text_gen_out.mp3')
        except:
            st.warning("ERROR GENERATING AUDIO!")
        try:
            with open("output.txt", "w") as f:
                f.write(output)
            st.success("Text file generated! Click the link below to download:")
            st.download_button("Download Text", data=output, key="file_download",file_name="text_gen_out.txt")
        except:
            st.warning("ERROR GENERATING PDF")

        with zipfile.ZipFile("output.zip", "w") as zip_file:
            zip_file.write("output.mp3")
            zip_file.write("output.txt")
        with open("output.zip", "rb") as f:
            d = f.read()
            st.download_button("Download All", data=d,file_name="text_gen_out.zip", key="zip_download")

        return output
    except Exception as e:
        st.error(f"Error generating text: {e}")
        return None


def home_page():

    st.write("""
    # Welcome To Text Generation!:wave:
    This uses a GPT-2 Model to generate text from context
    """)
    out=None
    with st.container():
        left_column, right_column = st.columns(2)
        with left_column:
            user_input = st.text_input("Start by typing the context here:")
            z= 10
            z= st.slider("Generation Size:", 10, 1000)
            if st.button("Generate Now"):
                if user_input:
                    st.write("---")
                    st.write("GENERATING....")
                    if lottie_anim2:
                        st_lottie(lottie_anim2, height=70, key='anim2')
                    else:
                        st.error("Failed to load animation")
                    out = generate(user_input,z)
                    if out:
                        st.write("The Result:")
                        st.write(f"{out}")
                        st.write("---")
                    
        with right_column:
            if lottie_anim:
                st_lottie(lottie_anim, height=200, key='anim')
            else:
                st.error("Failed to load animation")


def about_page():
    st.title("About Us")
    st.write("We are a team of AI developers.")
    st.write("Our mission is to make AI accessible to everyone.")


st.sidebar.title("Navigation")
selected_page = st.sidebar.radio("Go to:", ("Home", "About"))


if selected_page == "Home":
    home_page()
elif selected_page == "About":
    about_page()