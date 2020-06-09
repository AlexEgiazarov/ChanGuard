import re
import numpy as np
import pandas as pd
from pprint import pprint

#gensim
import gensim 
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

#spacy for lemmatiziation
import spacy

#plotting 
import pyLDAvis
import pyLDAvis.gensim
import matplotlib.pyplot as plt

#enable logging for gensim
import logging
logging.basicConfig(format = '%(acstime)s : %(levelname)s : %(message)s', level = logging.ERROR)

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

#NLTK stop words
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stop_words.extend(['[REPLY]', 'kek', 'lol', 'reply'])

#splitting sentences in words
def sent_to_words(sentences):
    for sentence in sentences:
        #deacc removes punctuation
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

#remove stopwords
def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

#make bigrams
def make_bigrams(texts):
    return [bigram_mod[doc] for doc in texts]

#make trigrams
def make_trigrams(texts):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]

#lemmatization function
def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out

#function used to convert mallet model to LDA
def convertLdaMalletToGen(mallet_model, gamma_threshold=0.001, iterations=50):
    print("Converting mallet model to LDA model")
    model_gensim = gensim.models.ldamodel.LdaModel(
        id2word=mallet_model.id2word, num_topics=mallet_model.num_topics,
        alpha=mallet_model.alpha, eta=0,
        iterations=iterations,
        gamma_threshold=gamma_threshold,
        dtype=np.float64  # don't loose precision when converting from MALLET
    )
    model_gensim.state.sstats[...] = mallet_model.wordtopics
    model_gensim.sync_state()
    print("Returning converted model")
    return model_gensim


#LDA considers each document as a collection of different topics. Each topic is a collection of keywords.

#loading the pol Dataset
print("Loading data")
df = pd.read_csv('dataset/pol_2020-6-6_19-19.csv', index_col='thread_num')

#converting messages to list
data = df.com.values.tolist()

print("Running data preprocessing")
#removing the newline characters maybe not necessary
data = [re.sub('\n+', ' ', str(comment)) for comment in data]

#remove distracting single quotes
data = [re.sub("\'", "", str(sent)) for sent in data]

#getting separate words
data_words = list(sent_to_words(data))

#building the bigram and trigram models
#higher threshold fewer phrases
print("Building bigrams/trigrams models")
bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100)
trigram = gensim.models.Phrases(bigram[data_words], threshold=100)

#faster way to get sentece clubbed as a trigram
bigram_mod = gensim.models.phrases.Phraser(bigram)
trigram_mod = gensim.models.phrases.Phraser(trigram)

#removing stop words
print("Removing stop words")
data_words_nostops = remove_stopwords(data_words)

#Form bigrams
print("Forming bigrams")
data_words_bigrams = make_bigrams(data_words_nostops)

#initiate spacy model, keeping only tagger component
print("Initializing spacy model")
nlp = spacy.load('en', disable=['parser', 'ner'])

#Do lemmatization keeping only noun adj vb adv
print("Performing lemmatization")
data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

#creating dictionary
print("Creating id2word dictionary")
id2word = corpora.Dictionary(data_lemmatized)

#creating corpus
print("Creating corpus")
texts = data_lemmatized

#Term document frequency
corpus = [id2word.doc2bow(text) for text in texts]

#human readable format for corpus
#[[(id2word[id], freq) for id, freq in cp] for cp in corpus[:1]]

#BUILDING TOPIC MODEL
#build LDA model
print("Creating lda model")
lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                            id2word=id2word,
                                            num_topics=20,
                                            random_state=100,
                                            update_every=1,
                                            chunksize = 100,
                                            passes=10,
                                            alpha='auto',
                                            per_word_topics=True)

#pprint(lda_model.print_topics())
doc_lda = lda_model[corpus]

#computing model perplexity and coherence score

print("Computing perplexity")
#Measuring how good model is
print('\nPerplexity: ', lda_model.log_perplexity(corpus))

print("Computing coherence score")
coherence_model_lda = CoherenceModel(model=lda_model, texts=data_lemmatized, dictionary=id2word, coherence='c_v')
coherence_lda = coherence_model_lda.get_coherence()
print('\nCoherence score: ', coherence_lda)

#visualizing the topics
print("Visualizing topics")
#pyLDAvis.enable_notebook()
vis = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
pyLDAvis.save_html(vis, 'LDA_Visualization.html')
#vis

#Checking mallet LDA
print("Loading Mallet LDA")
mallet_path = '/home/alex/Projects/miscProjects/ChanGuard/mallet-2.0.8/bin/mallet'
ldamallet = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=20, id2word=id2word)

#Show topics
pprint(ldamallet.show_topics(formatted=False))

#computing mallet coherence score
coherence_model_ldamallet = CoherenceModel(model=ldamallet, texts=data_lemmatized, dictionary=id2word, coherence='c_v')
coherence_lda_mallet = coherence_model_ldamallet.get_coherence()

print('\nCoherence score for LDA-Mallet: ', coherence_lda_mallet)

print("Visualizing Mallet topics")
vis = pyLDAvis.gensim.prepare(convertLdaMalletToGen(ldamallet), corpus, id2word)
pyLDAvis.save_html(vis, 'LDA_Mallet_Visualization.html')