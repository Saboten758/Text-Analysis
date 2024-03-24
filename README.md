# Text-Analysis

This Streamlit application aims to perform perform text analysis tasks such as sentiment analysis and text generation using various models. It also provides functionality for generating music based on text prompts. It is made using huggingface Transformers.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Screenshots](#screenshots)
- [Usage](#usage)
- [Credits](#credits)

## Features

### Text Generation
- Utilizes GPT-2 model to generate text based on user input.
- Users can select the model variant (e.g., gpt2, gpt2-medium) and specify the size of the generated text.
- Supports downloading the generated text as a text file and audio file.
- Provides an option to download all generated files as a zip archive.

### Sentiment Analysis
- Performs sentiment analysis on user-provided text using the BERTweet model.
- Displays the sentiment label (positive, negative, neutral) along with the confidence score.

### Music Generation
- Generates music from text prompts using the Musicgen model.
- Users can input text prompts and specify the duration of the generated music.
- Supports downloading the generated music as an audio file.

## Installation

To run the app locally, follow these steps:

1. Install the required dependencies:
```
pip install requirements.txt
```
2. Run the StreamLit appliation:
```
streamlit run Text_GEn.py
```
3. Access the app in your web browser at the provided URL.

## Screenshots
Some Screenshots:<br/>
<div style="text-align:center"><img src="https://i.imgur.com/puHLZyv.png" style="display: block; margin: 0 auto" >
Text Gen Page<br/>
<div style="text-align:center"><img src="https://i.imgur.com/PnAkPb9.png" style="display: block; margin: 0 auto" >
Sentiment Analysis Page<br/>
<img src="https://i.imgur.com/5dlQdF7.png" style="display: block; margin: 0 auto" ><br/>
Music Gen Page<br/>
<div style="text-align:left">

## Usage

Navigate to the desired section using the sidebar:
- Text Generation
- Sentiment Analysis
- Music Generation
- About

## Credits

- Streamlit: For building the interactive web application.
- Hugging Face Transformers: For providing pre-trained models for text analysis and generation.
- Facebook AI Research: For the Musicgen model used for music generation.</div>