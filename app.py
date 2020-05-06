from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import io
import random
import string  # to process standard python strings
import warnings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.stem import WordNetLemmatizer
import warnings
from youtube_transcript_api import YouTubeTranscriptApi

nltk.download('popular', quiet=True)  # for downloading packages
nltk.download('punkt')  # first-time use only
nltk.download('wordnet')  # first-time use only
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app, support_credentials=True)
app.config["DEBUG"] = True


def get_transcript(video_id):
    try:
        return YouTubeTranscriptApi.get_transcript(video_id)

    except:
        print("Something went wrong!")


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/response', methods=['POST'])
def get_everything():
    video_id = request.form.get('video_id')
    x = get_transcript(video_id)
    raw = ''
    for i in range(len(x)):
        raw += (x[i]['text']) + ". "
    raw = raw.lower()
    sent_tokens = nltk.sent_tokenize(raw)  # converts to list of sentences
    word_tokens = nltk.word_tokenize(raw)  # converts to list of words
    lemmer = nltk.stem.WordNetLemmatizer()

    # WordNet is a semantically-oriented dictionary of English included in NLTK.
    def LemTokens(tokens):
        return [lemmer.lemmatize(token) for token in tokens]

    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

    def LemNormalize(text):
        return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

    GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey",)
    GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

    def greeting(sentence):

        for word in sentence.split():
            if word.lower() in GREETING_INPUTS:
                return random.choice(GREETING_RESPONSES)

    def response(user_response):
        robo_response = ''
        sent_tokens.append(user_response)
        TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
        tfidf = TfidfVec.fit_transform(sent_tokens)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        if req_tfidf == 0:
            robo_response = robo_response + "I am sorry! I don't understand you"
            return robo_response
        else:
            robo_response = robo_response + sent_tokens[idx]
            # print(idx)
            return robo_response

    user_response = request.form.get('question')
    user_response = user_response.lower()
    if user_response != 'bye':
        if user_response == 'thanks' or user_response == 'thank you':

            return jsonify([])
        else:
            if greeting(user_response) is not None:
                return jsonify([])
            else:
                answer = response(user_response)
                sent_tokens.remove(user_response)
                if answer != "I am sorry! I don't understand you":
                    l = answer.split('. ')
                    for i in range(len(l)):
                        l[i] = l[i].strip('. ')
                    l1 = [i for i in range(len(x)) for j in l if j in x[i]['text'].lower()]
                    # print(l1)
                else:
                    return jsonify([])

    data_list = [x[temp] for temp in l1]
    return jsonify(data_list)


if __name__ == '__main__':
    app.run()
