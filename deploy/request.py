from flask import Flask,render_template,url_for,request
from flask_cors import CORS, cross_origin
import tweepy
import numpy as np
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')
import base64
#import image

import requests

url = 'https://growwithai.pythonanywhere.com/predict_api?value=modi'

sid_obj = SentimentIntensityAnalyzer()
pos=0
neg=0
app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/predict_api/', methods=["GET","POST"])
@cross_origin()
def predict_api():
    '''
    For direct API calls trought request
    '''
    message = request.args.get('value')
    consumerKey = '667OOi8BcK8R2gNOJNecmuOra'
    consumerSecret = 'Wxhhv1dH5TAyrtBVKBjNg52vGyzL3YGbYRVGkZ0ChfFpsXJyR6'
    accessToken = '1193971945764769793-sCKnrMI4zFyrUY20uK5IssFXGVgyZI'
    accessTokenSecret = 'fzYut9SWq7ZbeIlJwuLYeoe370enzwktM4vQlHK0UtsgM'
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    api = tweepy.API(auth)

    global pos , neg
    searchTerm=message


    NoOfTerms = 100

    # searching for tweets
    tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)
    for tweet in tweets:
     each=tweet.text
     sentiment_dict = sid_obj.polarity_scores(each)
     k=sentiment_dict['compound']
     if k>=0:
      pos=pos+1
     else:
      neg=neg+1
    pos1=(pos/NoOfTerms)*100
    neg1=(neg/NoOfTerms)*100
    objects = ('Positive','Negative')
    y_pos = np.arange(len(objects))
    performance =[pos1,neg1]
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('% of people')
    plt.title('sentiment')
    plt.savefig('/home/growwithai/full_model_deploy/deploy/static/image/new_plot.png')
    with open("/home/growwithai/full_model_deploy/deploy/static/image/new_plot.png", "rb") as f:
      data = f.read()
      result=base64.b64encode(data)
    return result
if __name__ == '__main__':
	app.run(debug=True)


