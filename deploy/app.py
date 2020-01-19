from flask import Flask,render_template,url_for,request
from flask import send_file
import tweepy
import numpy as np
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import io
import random
from flask import Response
import nltk
nltk.download('vader_lexicon')
sid_obj = SentimentIntensityAnalyzer()
pos=0
neg=0
app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/predict',methods=['POST'])
def predict():
 if request.method == 'POST':
  message = request.form['message']
  consumerKey = '667OOi8BcK8R2gNOJNecmuOra'
  consumerSecret = 'Wxhhv1dH5TAyrtBVKBjNg52vGyzL3YGbYRVGkZ0ChfFpsXJyR6'
  accessToken = '1193971945764769793-sCKnrMI4zFyrUY20uK5IssFXGVgyZI'
  accessTokenSecret = 'fzYut9SWq7ZbeIlJwuLYeoe370enzwktM4vQlHK0UtsgM'
  auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
  auth.set_access_token(accessToken, accessTokenSecret)
  api = tweepy.API(auth)

  global pos , neg
  searchTerm=message

    # input for term to be searched and how many tweets to search
    #searchTerm = input("Enter Keyword/Tag to search about: ")
  NoOfTerms = 200

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
  pos1=(pos/pos+neg)*100
  neg1=(neg/pos+neg)*100
  objects = ('Positive','Negative')
  y_pos = np.arange(len(objects))
  performance =[pos1,neg1]
  plt.bar(y_pos, performance, align='center', alpha=0.5)
  plt.xticks(y_pos, objects)
  plt.ylabel('% of people')
  plt.title('sentiment')
  plt.savefig('/home/growwithai/full_model_deploy/deploy/static/image/new_plot.png')
  #plt.savefig('plot.png')
  #output = io.BytesIO()

   #mimetype='image/png')


  return render_template('result.html', name = 'new_plot', url ='static/image/new_plot.png')
#eturn render_template('untitled1.html', name = plt.show())

"""@app.route('/get_image',methods=['POST'])
def get_image():
    if request.args.get('type') == '1':
       filename = 'ok.gif'
    else:
       filename = 'error.gif'
    return send_file(filename, mimetype='image/gif')"""
if __name__ == '__main__':
	app.run()
