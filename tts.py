from gtts import gTTS
import os
mytext='Welcome GUYS'
lang='en-us'
myobj = gTTS(text=mytext, lang=lang, slow=False) 
  

myobj.save("welcome.mp3") 
  