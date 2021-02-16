import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import count
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from matplotlib.animation import FuncAnimation
import spacy
import os 

sns.set() 
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2,  figsize=(16,8))
fig.suptitle('Live Tweet Monitor')

# vals for ax2
x_vals = []
y_vals = []
index = count()

# variables for ax3
doc = []
size = 0

# file name of the incoming data 
filename = 'stream_data.csv'

def count_words(df):
	'''
	Creates df showing word count
	'''
	global size
	# tokenize only the new tweets
	df_new = df.iloc[size:,:]
	print("new df size: {}".format(df_new.shape[0]))
	# Connect sentences in the list to one big string
	text = ' '.join(df_new['tweet'].astype(str).tolist())
	# Initialize Spacy
	nlp = spacy.load('en_core_web_sm')
	# Tokenize the text

	for token in nlp(text):
		doc.append(token)
	# Create a Pandas dataframe to store data for visualization
	data = [token.lemma_ for token in doc if not (token.is_stop or token.is_space)]
	df_tokens = pd.DataFrame(data)
	df_word_count = df_tokens[df_tokens[0].str.len() > 2][0].value_counts()[:20]
	
	size = df.shape[0]
	return df_word_count

def animate1(i):

	df = pd.read_csv(filename)

	# ax1
	xs = df['subjectivity']
	ys = df['sentiment']
	ax1.cla()
	sns.scatterplot(x=xs, y=ys, ax=ax1)
	ax1.set_xlabel('Subjectivity', labelpad=0.2, fontsize=10) 
	ax1.set_ylabel('Sentiment', labelpad=0.2, fontsize=10) 
	ax1.set_title("Sentiment and Subjectivity of Individual Tweets")

	# ax2
	x_vals.append(df.shape[0])
	y_vals.append(df['sentiment'].sum())
	ax2.cla()
	sns.lineplot(x=x_vals, y=y_vals, ax=ax2)
	ax2.set_title("Overall Sentiment")

	# ax4
	df = count_words(df)
	ax4.cla() 	
	sns.barplot(df.values, df.index, ax=ax4)
	ax4.set_title('Word Frequency')
	ax4.set_xlabel("count", labelpad=0.2)

def animate2(i):

	df = pd.read_csv(filename)	

	# ax3
	# Limit to the recent 100 tweets 
	recent = 100
	text = " ".join(df['tweet'][(-1)*recent:].astype(str))
	wordcloud = WordCloud(background_color="white", prefer_horizontal=0.5).generate(text)
	ax3.imshow(wordcloud, interpolation='bilinear')
	ax3.axis("off")
	ax3.set_title("Word Cloud of Recent {} Tweets".format(recent),  y=-0.05)

def main():

	print('Waiting for incoming data... ')

	while not os.path.isfile(path):
		time.sleep(5)

	ani1 = FuncAnimation(plt.gcf(), animate1, interval = 1_000)
	ani2 = FuncAnimation(plt.gcf(), animate2, interval = 3_000)

	plt.tight_layout()
	plt.show()


if __name__ == '__main__':
	main()