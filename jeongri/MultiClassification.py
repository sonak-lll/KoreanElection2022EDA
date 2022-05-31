!apt-get update
!apt-get install -y fonts-nanum
!fc-cache -fv
!rm ~/.cache/matplotlib -rf

import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import re
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['axes.unicode_minus'] = False

plt.rc('font', family = 'NanumBarunGothic')

!pip install transformers

from transformers import TextClassificationPipeline, BertForSequenceClassification, AutoTokenizer
model_name = 'smilegate-ai/kor_unsmile'
model = BertForSequenceClassification.from_pretrained(model_name)

tokenizer = AutoTokenizer.from_pretrained(model_name, model_max_length = 600)

pipe = TextClassificationPipeline(
        model = model,
        tokenizer = tokenizer,
        device = 0,   # cpu: -1, gpu: gpu number
        return_all_scores = True,
        function_to_apply = 'sigmoid'
    )

# model

def smile(df):
    result = []
    for t in df['Text'].astype(str):
        result.extend(pipe(t))
    # dict -> list로 정리
    score = [[item['score'] for item in i] for i in result]

    label =  ['여성/가족', '남성', '성소수자', '인종/국적', '연령', '지역', '종교', '기타 혐오', '악플/욕설', 'clean']
    new_df = pd.DataFrame(score, columns=label)
    new_df['result'] = new_df.idxmax(axis = 1)
    return(new_df)

plt.figure(figsize = (8,6))
plt.pie(new_df['result'].value_counts()/len(new_df),
        labels = ['clean', '악플/욕설', '여성/가족', '남성', '지역', '성소수자',
                  '인종/국적', '기타 혐오', '연령', '종교'],
        autopct = '%.1f%%')
plt.show()
