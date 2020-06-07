import re
import numpy as np
import pandas as pd
from pprint import pprint

#gensim
import gensim 
import gnesim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

#spacy for lemmatiziation
import spacy

#plotting 
import pyLDAvis
import pyLDAvis.gensim
import matplotlib.pyplot as plt
%matplotlib inline

#enable logging for gensim
import logging
logging.basicConfig(format = '%(acstime)s : %(levelname)s : %(message)s', level = logging.ERROR)