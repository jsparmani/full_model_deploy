from flask import Flask,render_template,url_for,request
import tweepy
import numpy as np
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer

#import image

import requests

url = 'http://localhost:5000/predict_api?value=modi'

sid_obj = SentimentIntensityAnalyzer()
pos=0
neg=0
app = Flask(__name__)

@app.route('/predict_api/', methods=["GET","POST"])
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
    plt.savefig('static/image/new_plot.png')
    with open("static/image/new_plot.png", "rb") as f:
      data = f.read()
      result=data.encode("base64")
    return result
if __name__ == '__main__':
	app.run(debug=True)

    
