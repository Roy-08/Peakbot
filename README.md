# Peakbot
PEAKBOT is an intelligent chatbot that recommends songs based on the user’s emotional tone. It uses IBM Watson Tone Analyzer to detect emotions from user text and suggests personalized music through the Last.fm API. The chatbot simulates human-like conversation and provides an engaging way to discover music that fits your mood.

Tech Stack:
Frontend: HTML, CSS, Anvil framework
Backend: Google Colab (Python), Flask
APIs:  Last.fm API
Tools: POSTMAN, XAMPP

Key Features:
Emotion detection through text input
Dynamic music recommendations
User-friendly chat interface
No login required for interaction

How to use 
After downloading the project use following commands using vs code :
$ git clone https://github.com/python-engineer/chatbot-deployment.git

$ cd chatbot-deployment

$ python3 -m venv venv

$ . venv/bin/activate

(venv) pip install Flask torch torchvision nltk

(venv) python

>>> import nltk
>>> nltk.download('punkt')

Then train your chatbot 
train.py
app.py

When your chatbot trained succesfully then add your project in xampp/htdocs folder
Open xampp activate Apache and mysql 
Go to the chrome and type :
localhost/peakbot/music.php

