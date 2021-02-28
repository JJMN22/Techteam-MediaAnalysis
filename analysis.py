import nltk
import pandas as pd
from textblob import TextBlob
from textblob import Blobber
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob.sentiments import NaiveBayesAnalyzer
from transformers import pipeline
import matplotlib.pyplot as plt

df = pd.read_csv("data.csv") #read in your cleaned data

def sentiment_scores_vader(texts):
    scores = []
    analyzer = SentimentIntensityAnalyzer()
    for text in texts:
        sentiment_dict = analyzer.polarity_scores(text)
        scores.append(sentiment_dict['compound'])
    return scores

def sentiment_scores_transformer(texts):
    scores = []
    classifier = pipeline('sentiment-analysis')
    for text in texts:
        sentiment_dict = classifier(text)
        score = (sentiment_dict[0])['score']
        if (sentiment_dict[0])['label'] == "NEGATIVE":
          score *= -1
        scores.append(score)
    return scores

def textblob(df):
  df['sentiment_textblob'] = df['text'].apply(lambda x: TextBlob(x).sentiment[0])

def textblob_bayes(df):
  blobber = Blobber(analyzer=NaiveBayesAnalyzer())
  df['sentiment_bayes'] = df['text'].apply(lambda x: blobber(x).sentiment[0])

textblob(df)
textblob_bayes(df)

# Plots histogram of the sentiments and prints the mean
df.hist('sentiment_textblob')
print(df['sentiment_textblob'].mean())

# Plots average monthly sentiment
df['date'] = pd.to_datetime(df['date'])
df['yearmon'] = pd.DatetimeIndex(df['date']).to_period('M')
mean_sentiment_byday = pd.DataFrame(df.groupby(['yearmon'])['sentiment_textblob'].mean())
mean_sentiment_byday.reset_index(level=0, inplace=True)
mean_sentiment_byday.plot(x='yearmon',y='sentiment_textblob')

plt.show()