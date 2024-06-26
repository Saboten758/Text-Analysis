import streamlit as st
import requests
from streamlit_lottie import st_lottie
from gtts import gTTS
from fpdf import FPDF
from transformers import pipeline, set_seed,AutoProcessor, MusicgenForConditionalGeneration
import zipfile
import scipy
import os
from PIL import Image
print("LOADING...")

st.set_page_config(page_title="Text Analysis", page_icon="📖", layout="wide")
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
lemon=Image.open("Images/Lp.png")
retro=Image.open("Images/rp.png")
brr=Image.open("Images/br.png")
fr=Image.open("Images/Action.png")

def tts_service(data,name):
    lang = 'en-us'
    tts = gTTS(text=data, lang=lang, slow=False)
    tts.save(f"{name}.mp3")

def generate(txt,z,mod):
    try:
        generator = pipeline('text-generation', model=mod,device_map="auto")
        set_seed(42)

        x = generator(txt, max_length=z,  truncation=True)
        #x = generator(txt, max_length=z, num_return_sequences=5, truncation=True)
        output = x[0]['generated_text']
        try:
            tts_service(output,"output")
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
            st.success("Both audio and text file generated! Click the links below to download!")
            st.download_button("Download Text", data=output, key="file_download",file_name="text_gen_out.txt")
        except:
            st.warning("ERROR GENERATING FILE")

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

def cleanup():
    try:
        # Delete temporary files
        os.remove("output.mp3")
        os.remove("output.txt")
        os.remove("output.zip")
        os.remove("musicgen_out.wav")

        del generator
        del context_analyzer

        print("Cleanup complete.")
    except Exception as e:
        print(f"Error during cleanup: {e}")

def gen_page():
    cleanup()
    st.write("""
    # Welcome To Text Generation!:wave:
    This uses a GPT-2 Model to generate text from context
    """)
    
    out=None
    with st.container():
        left_column, right_column = st.columns(2)
        with right_column:
            option = st.selectbox(
            'Which Model to use?',
            ('gpt2','gpt2-medium'))

            st.write('You selected:', option)
            if lottie_anim:
                st_lottie(lottie_anim, height=200, key='anim')
            else:
                st.error("Failed to load animation")

        with left_column:
            
            user_input = st.text_area("Start by typing the context here:", "")
            z= 10
            z= st.slider("Generation Size:", 10, 1000)
            if st.button("Generate Now"):
                if user_input:
                    st.write("---")
                    with st.spinner("Generating..."):
                        if lottie_anim2:
                            st_lottie(lottie_anim2, height=60, key='anim2')
                        else:
                            st.error("Failed to load animation")
                        out = generate(user_input,z,option)
                        if out:
                            st.write("The Result:")
                            st.write(f"{out}")
                            st.write("---")

def analysis_page():
    cleanup()
    st.title("Sentiment Analysis")
    st.write("Enter the text you want to analyze:")
    user_input = st.text_area("Input Text", "")

    if st.button("Analyze"):
        st.write("Analyzing...")
        with st.spinner("Analyzing..."):
            
            context_analyzer = pipeline("sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis")
            analysis_result = context_analyzer(user_input)

        label=str(analysis_result[0]["label"])
        score=analysis_result[0]['score']
        print(label)
        st.write("Analysis Result:")
        if label=='NEG':
            st.warning(f"NEGATIVE with a score of {score}")
        elif label=='POS':
            st.success(f"POSITIVE with a score of {score}")
        else:
            st.write(f"NEUTRAL with a score of {score}")

def about_page():
    cleanup()
    st.title("About Me:")
    st.write(" Hi!  I am Saboten & I like Machine Learning Stuff🙂")
   
    with st.container():
        st.write("# Check out some other work:")
        img_col,txt_col=st.columns((1,2))
        with img_col:
            st.image(lemon)
        with txt_col:
            st.write("## Lemon Player")
            st.write("This is an android based online radio player along with support for rss feeds and web games & comics all integrated into one! Check out More info on [Github](https://github.com/Saboten758/Lemon_Player)")
            st.markdown("[Checkout Releases...](https://github.com/Saboten758/Lemon_Player/releases)")
        with st.container():
            img_col,txt_col=st.columns((1,2))
            with img_col:
                st.image(fr)
            with txt_col:
                st.write("## Human Action Recognition")
                st.write("This a collection of jupyter ipynbs which aims to recognize human actions (running,jumping,crawling,etc). Check out More info on [Github](https://github.com/Saboten758/Human_Action_Detection)")
        

        with st.container():
            img_col,txt_col=st.columns((1,2))
            with img_col:
                st.image(retro)
            with txt_col:
                st.write("## Retro Pulse")
                st.write("This is also an android based application that has automatic glow-in-dark flashlight support,sensor data analysis,device info,camera,weather, and much more.. Check out More info on [Github](https://github.com/Saboten758/Retro-Pulse)")
        with st.container():
            img_col,txt_col=st.columns((1,2))
            with img_col:
                st.image(brr)
            with txt_col:
                st.write("## Braillification")
                st.write("This was build to aid the blind people. It is a Flask based web app that allows you to convert text from PDF files to Braille formatted pds and audio. Check out More info on [Github](https://github.com/Saboten758/Braillification)")
        
        st.write("## Maybe some games too:")
        st.markdown(
        '<iframe frameborder="0" src="https://itch.io/embed/2606101?linkback=true&amp;border_width=2&amp;bg_color=a8e3a9&amp;fg_color=000000&amp;link_color=ad3338&amp;border_color=34a729" width="554" height="169"><a href="https://debjit-daw.itch.io/frog-in-exile">Frog in exile by Saboten123</a></iframe>',
        unsafe_allow_html=True)
        st.markdown(
        '<iframe frameborder="0" src="https://itch.io/embed/2170857?linkback=true&amp;bg_color=a4b9d3&amp;fg_color=000000&amp;link_color=4061d7&amp;border_color=333333" width="552" height="167"><a href="https://debjit-daw.itch.io/the-unyielding-mind">The Unyielding Mind by Saboten123</a></iframe>',
        unsafe_allow_html=True)
    
    st.write("---")
    st.write("### Other Socials:")
    with st.container():
        l,r,z=st.columns(3)
    with l:
        st.write("[Github](https://github.com/Saboten758)")
    with r:
        st.write("[Itch.io](https://debjit-daw.itch.io/)")
    with z:
        st.write("[Gmail](mailto:debjitdaw03@gmail.com)")

def music_gen(txt,time_given):
    processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
    model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")

    inputs = processor(
        text=txt,
        padding=True,
        return_tensors="pt",
    )
    new_tokens=int(51.2*time_given)
    audio_values = model.generate(**inputs, max_new_tokens=new_tokens)

    sampling_rate = model.config.audio_encoder.sampling_rate
    scipy.io.wavfile.write("musicgen_out.wav", rate=sampling_rate, data=audio_values[0, 0].numpy())
    st.write("Click Here to play:")
    st.audio("musicgen_out.wav", format="audio/wav")
    with open("musicgen_out.wav", "rb") as f:
        d = f.read()
        st.download_button("Download Audio", data=d, key="audio_download", file_name='music_gen_out.wav')

def music_page():
    cleanup()
    st.write("# This Page Generates Music from Text🎵")
    st.write("Enter your prompt below to generate some music:")
    prompt = st.text_area("Enter Here:", "")
    time_given= 5
    time_given= st.slider("How Many Seconds to generate (Note: Increasing this may lead to longer generation times):", 5, 6)
    #time_given= st.slider("How Many Seconds to generate (Note: Increasing this may lead to longer generation times):", 5, 10)
    if st.button("Generate"):
        with st.spinner("Generating..."):
            st.write("---")
            music_gen(prompt,time_given)


st.sidebar.title("Navigation")
selected_page = st.sidebar.radio("Go to:", ("Text Generation", "Sentiment Analysis","Music Generation","About"))


if selected_page == "Text Generation":
    gen_page()

elif selected_page=="Sentiment Analysis":
    analysis_page()

elif selected_page=="Music Generation":
    music_page()

elif selected_page == "About":
    about_page()