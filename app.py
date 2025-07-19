import nltk
nltk.download('popular')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
from keras.models import load_model
model = load_model('model.h5')
import json
import random
intents = json.loads(open('data.json').read())
words = pickle.load(open('texts.pkl','rb'))
classes = pickle.load(open('labels.pkl','rb'))

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

import database
database.create_tables()
user_sessions = {}

def chatbot_response(msg, user_id="default_user"):
    if user_id not in user_sessions:
        user_sessions[user_id] = {"name": None, "email": None, "inquiry_type": None, "state": "new_user"}

    session = user_sessions[user_id]
    response = ""

    if session["state"] == "new_user":
        session["state"] = "collecting_name"
        response = "Hello! What is your name?"
    elif session["state"] == "collecting_name":
        session["name"] = msg
        session["state"] = "collecting_email"
        response = f"Nice to meet you, {msg}! What is your email address?"
    elif session["state"] == "collecting_email":
        session["email"] = msg
        session["state"] = "collecting_inquiry_buttons"
        response = "What type of inquiry do you have?"
    elif session["state"] == "collecting_inquiry":
        session["inquiry_type"] = msg
        session["state"] = "chatting"
        response = "Thank you! How can I help you today?"
    elif session["state"] == "collecting_inquiry_buttons":
        buttons = [
            {"type": "reply", "reply": {"id": "pricing", "title": "Pricing"}},
            {"type": "reply", "reply": {"id": "support", "title": "Support"}},
            {"type": "reply", "reply": {"id": "other", "title": "Other"}},
        ]
        from whatsapp_handler import send_whatsapp_message_with_buttons
        send_whatsapp_message_with_buttons(user_id, "Please select an inquiry type:", buttons)
        return ""
    else:
        ints = predict_class(msg, model)
        response = getResponse(ints, intents)

    database.save_interaction(user_id, msg, response)
    return response


from flask import Flask, render_template, request

app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return chatbot_response(userText, "web_user")


if __name__ == "__main__":
    app.run()

import whatsapp_handler

@app.route("/whatsapp", methods=['GET', 'POST'])
def whatsapp_webhook():
    if request.method == 'GET':
        # WhatsApp verification
        if request.args.get('hub.verify_token') == 'YOUR_VERIFY_TOKEN':
            return request.args.get('hub.challenge')
        return 'Error, wrong validation token'
    return whatsapp_handler.handle_whatsapp_message(request)