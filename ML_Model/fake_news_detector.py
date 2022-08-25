
import pandas as pd
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.layers import Dense,LSTM,Embedding
from tensorflow.keras.models import Sequential
import re
from web_scraper import WebScraper
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
# from sklearn.feature_extraction.text import TfidfTransformer
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.feature_extraction.text import TfidfVectorizer
# import pickle

class FactChecker:
    # @staticmethod
    # def check_facts(df):
    #     stop_words = stopwords.words('english')
    #     df['total']=df['title']+' '+df['text']
    #     lemmatizer=WordNetLemmatizer()
    #     for index,row in df.iterrows():
    #         filter_sentence = ''
    #         sentence = row['total']
    #         sentence = re.sub(r'[^\w\s]','',sentence)
    #         words = nltk.word_tokenize(sentence)
    #         words = [w for w in words if not w in stop_words]
    #         for word in words:
    #             filter_sentence = filter_sentence + ' ' + str(lemmatizer.lemmatize(word)).lower()
    #         df.loc[index,'total'] = filter_sentence
    #     count_vectorizer = CountVectorizer()
    #     count_vectorizer.fit_transform(df['total'])
    #     freq_term_matrix = count_vectorizer.transform(df['total'])
    #     tfidf = TfidfTransformer(norm="l2")
    #     tfidf.fit(freq_term_matrix)
    #     tf_idf_matrix = tfidf.fit_transform(freq_term_matrix)
    #
    #     print(tf_idf_matrix.toarray())
    #
    #     model = pickle.load(open('model.pkl', 'rb'))
    #
    #     pred = model.predict(tf_idf_matrix)
    #
    #     print(pred)


    @staticmethod
    def check_fact(df):
        ps=PorterStemmer()
        corpus=[]
        for i in range(len(df)):
            review=re.sub('[^a-zA-Z]',' ',df.title[i])
            review=review.lower()
            review=review.split()
            review=[ps.stem(i) for i in review if i not in set(stopwords.words('english'))]
            review=' '.join(review)
            corpus.append(review)

        vocab_size=10000
        one_hot_repr=[one_hot(word,vocab_size) for word in corpus]

        sent_length=20
        pad_doc=pad_sequences(one_hot_repr,padding='pre',maxlen=sent_length)

        emb_vec_fea=100
        model=Sequential()
        model.add(Embedding(vocab_size,emb_vec_fea,input_length=sent_length))
        model.add(LSTM(200))
        model.add(Dense(1,activation='sigmoid'))

        model.compile(loss='binary_crossentropy',optimizer='adam',metrics='accuracy')
        model.load_weights('weights.h5')
        value = model.predict(pad_doc)
        value = value>0.5
        ret_val = {'fakeNews': value[0][0]}
        return ret_val

# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
# value = WebScraper.economic_times_scraper('https://economictimes.indiatimes.com/news/india/sc-sets-aside-mp-hc-verdict-on-discharge-of-rape-accused-says-its-utterly-incomprehensible/articleshow/93659916.cms')
#
# # # df = pd.DataFrame(columns=['title', 'text', 'subject'])
# # # df.loc[0] = ['Drunk Bragging Trump Staffer Started Russian Collusion Investigation', 'Donald Trump just couldn t wish all Americans a Happy New Year and leave it at that. Instead, he had to give a shout out to his enemies, haters and  the very dishonest fake news media.  The former reality show star had just one job to do and he couldn t do it. As our Country rapidly grows stronger and smarter, I want to wish all of my friends, supporters, enemies, haters, and even the very dishonest Fake News Media, a Happy and Healthy New Year,  President Angry Pants tweeted.  2018 will be a great year for America! As our Country rapidly grows stronger and smarter, I want to wish all of my friends, supporters, enemies, haters, and even the very dishonest Fake News Media, a Happy and Healthy New Year. 2018 will be a great year for America!  Donald J. Trump (@realDonaldTrump) December 31, 2017Trump s tweet went down about as welll as you d expect.What kind of president sends a New Year s greeting like this despicable, petty, infantile gibberish? Only Trump! His lack of decency won t even allow him to rise above the gutter long enough to wish the American citizens a happy new year!  Bishop Talbert Swan (@TalbertSwan) December 31, 2017no one likes you  Calvin (@calvinstowell) December 31, 2017Your impeachment would make 2018 a great year for America, but I ll also accept regaining control of Congress.  Miranda Yaver (@mirandayaver) December 31, 2017Do you hear yourself talk? When you have to include that many people that hate you you have to wonder? Why do the they all hate me?  Alan Sandoval (@AlanSandoval13) December 31, 2017Who uses the word Haters in a New Years wish??  Marlene (@marlene399) December 31, 2017You can t just say happy new year?  Koren pollitt (@Korencarpenter) December 31, 2017Here s Trump s New Year s Eve tweet from 2016.Happy New Year to all, including to my many enemies and those who have fought me and lost so badly they just don t know what to do. Love!  Donald J. Trump (@realDonaldTrump) December 31, 2016This is nothing new for Trump. He s been doing this for years.Trump has directed messages to his  enemies  and  haters  for New Year s, Easter, Thanksgiving, and the anniversary of 9/11. pic.twitter.com/4FPAe2KypA  Daniel Dale (@ddale8) December 31, 2017Trump s holiday tweets are clearly not presidential.How long did he work at Hallmark before becoming President?  Steven Goodine (@SGoodine) December 31, 2017He s always been like this . . . the only difference is that in the last few years, his filter has been breaking down.  Roy Schulze (@thbthttt) December 31, 2017Who, apart from a teenager uses the term haters?  Wendy (@WendyWhistles) December 31, 2017he s a fucking 5 year old  Who Knows (@rainyday80) December 31, 2017So, to all the people who voted for this a hole thinking he would change once he got into power, you were wrong! 70-year-old men don t change and now he s a year older.Photo by Andrew Burton/Getty Images.', 'News']
# v = FactChecker.check_fact(value)
# print(v)