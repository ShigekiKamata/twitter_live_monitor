import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set() # Setting seaborn as default style even if use only matplotlib
from itertools import count
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from matplotlib.animation import FuncAnimation
import spacy

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2,  figsize=(16,8))
fig.suptitle('Live Tweet Monitor')

# vals for ax2
x_vals = []
y_vals = []
index = count()

def count_words(df):
	'''
	Creates df showing word count
	'''
	# Connect sentences in the list to one big string
	text = ' '.join(df['tweet'].tolist())
	# Initialize Spacy
	nlp = spacy.load('en_core_web_sm')
	# Tokenize the text
	doc = nlp(text)

	# Create a Pandas dataframe to store data for visualization
	data = [token.lemma_ for token in doc if not (token.is_stop or token.is_space)]
	df = pd.DataFrame(data)
	df = df[df[0].str.len() > 2][0].value_counts()[:20]
	
	return df


def animate1(i):

	df = pd.read_csv('stream_data.csv')

	# ax1
	xs = df['subjectivity']
	ys = df['sentiment']
	ax1.cla()
	sns.scatterplot(x=xs, y=ys, ax=ax1)
	ax1.set_xlabel('Subjectivity', labelpad=0.2, fontsize=10) 
	ax1.set_ylabel('Sentiment', labelpad=0.2, fontsize=10) 
	ax1.set_title("Sentiment and Subjectivity of Individual Tweets")

	# ax2
	x_vals.append((next(index)))
	y_vals.append(df['sentiment'].sum())
	ax2.cla()
	sns.lineplot(x=x_vals, y=y_vals, ax=ax2)
	ax2.set_title("Overall Sentiment")

def animate2(i):

	df = pd.read_csv('stream_data.csv')	

	# ax3
	recent = 100
	text = " ".join(df['tweet'][(-1)*recent:])
	wordcloud = WordCloud(background_color="white", prefer_horizontal=0.5).generate(text)
	ax3.imshow(wordcloud, interpolation='bilinear')
	ax3.axis("off")
	ax3.set_title("Word Cloud of Recent {} Tweets".format(recent))

	# ax4
	df = count_words(df)
	ax4.cla() 	
	sns.barplot(df.values, df.index, ax=ax4)
	ax4.set_title('Word Frequency')

def main():

	ani1 = FuncAnimation(plt.gcf(), animate1, interval = 1_000)
	ani2 = FuncAnimation(plt.gcf(), animate2, interval = 10_000)

	plt.tight_layout()
	plt.show()


if __name__ == '__main__':
	main()