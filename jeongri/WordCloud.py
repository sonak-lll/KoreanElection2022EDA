!apt-get update
!apt-get install -y fonts-nanum
!fc-cache -fv
!rm ~/.cache/matplotlib -rf

!curl -s https://raw.githubusercontent.com/teddylee777/machine-learning/master/99-Misc/01-Colab/mecab-colab.sh | bash

!pip install --upgrade plotly
!pip install konlpy
!pip install swifter

import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['axes.unicode_minus'] = False

plt.rc('font', family = 'NanumBarunGothic')

import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from plotly import graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff
from collections import Counter
import seaborn as sns

from wordcloud import WordCloud
from konlpy.tag import Okt
from konlpy.tag import Twitter
import re

from datetime import datetime
from tqdm import tqdm
import swifter
from konlpy.tag import Kkma, Komoran, Mecab

def wordcloud(data):
    okt = Okt()
    word_list = []
    word_list = data['Text'].dropna()

    sentences_tag = []
    for sentence in word_list:
        morph = okt.pos(sentence)
        sentences_tag.append(morph)

    noun_list = []
    for sentence in sentences_tag:
        for word, tag in sentence:
            if tag in ['Noun']:
                noun_list.append(word)
    noun_list = [n for n in noun_list if len(n) > 1]
    counts = Counter(noun_list)
    tags = counts.most_common(1000)
    wordcloud = WordCloud('/data/NANUMGOTHIC.TTF',
                          width = 1000, height = 1000)
    print(dict(tags))
    # tags 몇 번째부터 할 지 선택 (안철수 1, 박지현 1, 추적단 불꽃 2, 4번 0)
    cloud = wordcloud.generate_from_frequencies(dict(tags[3:]))
    plt.figure(figsize = (10, 10))
    plt.axis('off')
    plt.imshow(cloud)
    plt.show()
