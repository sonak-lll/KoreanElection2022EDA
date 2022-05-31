import re

# 정규표현식 이용한 전처리
def clean_tweets(text):
    # \n 공백 제거
    text = re.sub('\n', ' ', str(text))
    # URL 제거
    text = re.sub('https://[A-Za-z0-9./]*', ''. str(text))
    # 한글자 제거 (ex:ㅋㅋ, ㅜㅜ)
    text = re.sub('([ㄱ-ㅎㅏ-ㅣ])+', '', str(text))
    # 숫자 제거 (숫자 + 숫자만 제거, ex: 1인가족)
    text = re.sub('[0-9]{2}', '', str(text))
    # @알파벳 제거
    text = re.sub('@[A-Za-z0-9./]*', '', str(text))
    return str(text)
