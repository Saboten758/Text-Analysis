from transformers import pipeline, set_seed
import os
from gtts import gTTS
print("LOADING...")
generator = pipeline('text-generation', model='gpt2')
set_seed(41)
os.system('cls')
val=input("Enter the Starting of the sentence:")
x=generator(val, max_length=1000, num_return_sequences=5,truncation=True)
with open('save.txt','w') as s:
    s.write(x[0]['generated_text'])
print(x[0]['generated_text'])

lang='en'
myobj = gTTS(text=x[0]['generated_text'], lang=lang, slow=False) 
  

myobj.save("generated.mp3") 