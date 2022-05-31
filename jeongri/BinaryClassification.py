!pip install transformers

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
import torch
from transformers import TrainingArguments, Trainer
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import EarlyStoppingCallback
from keras.preprocessing.sequence import pad_sequences
import matplotlib.pyplot as plt
import string

import nltk
from nltk.corpus import stopwords

if torch.cuda.is_available():    
    device = torch.device("cuda")

    print('There are %d GPU(s) available.' % torch.cuda.device_count())
    print('We will use the GPU:', torch.cuda.get_device_name(0))

else:
    print('No GPU available, using the CPU instead.')
    device = torch.device("cpu")

from google.colab import drive
drive.mount('/content/drive')

model_name = "beomi/kcbert-base"
tokenizer = BertTokenizer.from_pretrained(model_name)
model_path = "/content/drive/MyDrive/Colab Notebooks/kaggle/president election/data/checkpoint-1500"
model = BertForSequenceClassification.from_pretrained(model_path, num_labels=2)

def convert_input_data(sentences):

    tokenized_texts = [tokenizer.tokenize(sent) for sent in sentences]
    MAX_LEN = 64

    # 토큰을 숫자 인덱스로 변환
    input_ids = [tokenizer.convert_tokens_to_ids(x) for x in tokenized_texts]
    
    # 문장을 MAX_LEN 길이에 맞게 자르고, 모자란 부분을 패딩 0으로 채움
    input_ids = pad_sequences(input_ids, maxlen=MAX_LEN, dtype="long", truncating="post", padding="post")

    # 어텐션 마스크 초기화
    attention_masks = []

    # 어텐션 마스크를 패딩이 아니면 1, 패딩이면 0으로 설정
    for seq in input_ids:
        seq_mask = [float(i>0) for i in seq]
        attention_masks.append(seq_mask)
        
    inputs = torch.tensor(input_ids)
    masks = torch.tensor(attention_masks)

    return inputs, masks

def test_sentences(sentences):
 
    # 평가모드로 변경!!!!!
    model.eval()

    inputs, masks = convert_input_data(sentences)

    # 데이터를 GPU에 넣음
    b_input_ids = inputs.to(device)
    b_input_mask = masks.to(device)
            
    # 그래디언트 계산 안함
    with torch.no_grad():     
        # Forward 수행
        outputs = model(b_input_ids, 
                        token_type_ids=None, 
                        attention_mask=b_input_mask)

    # 로스 구함
    logits = outputs[0]

    # CPU로 데이터 이동
    logits = logits.detach().cpu().numpy()

    return logits

def preprocessing(df):

    df.document=df.Text.replace('[^A-Za-zㄱ-ㅎㅏ-ㅣ가-힣]+','')

    return df

def make_predicted_label(df):
    sens =[]
    for sen in number.Text:
        sens.append(sen)
    sen = [sens]
    score = test_sentences(sen)
    result = np.argmax(score)

    if result == 0:   # negative 
        return 0
    else:
        return 1   # positive

model.to(device)

scores_data=[]
for sen in sens:
    scores_data.append(make_predicted_label(sen))
