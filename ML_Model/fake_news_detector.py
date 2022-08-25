from keras_preprocessing.sequence import pad_sequences
from keras_preprocessing.text import one_hot
from keras.layers import Dense, LSTM, Embedding
from keras.models import Sequential
import re
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords


class FactChecker:
    @staticmethod
    def check_fact(df):
        ps = PorterStemmer()
        corpus = []
        for i in range(len(df)):
            review = re.sub('[^a-zA-Z]', ' ', df.title[i])
            review = review.lower()
            review = review.split()
            review = [ps.stem(i) for i in review if i not in set(stopwords.words('english'))]
            review = ' '.join(review)
            corpus.append(review)

        vocab_size = 10000
        one_hot_repr = [one_hot(word, vocab_size) for word in corpus]

        sent_length = 20
        pad_doc = pad_sequences(one_hot_repr, padding='pre', maxlen=sent_length)

        emb_vec_fea = 100
        model = Sequential()
        model.add(Embedding(vocab_size, emb_vec_fea, input_length=sent_length))
        model.add(LSTM(200))
        model.add(Dense(1, activation='sigmoid'))

        model.compile(loss='binary_crossentropy', optimizer='adam', metrics='accuracy')
        model.load_weights(filepath='./ML_Model/weights.h5')
        val = model.predict(pad_doc)
        del model
        val = val > 0.5
        if val[0][0]:
            value = 1
        else:
            value = 0
        ret_val = {"fakeNews": value}
        return ret_val
