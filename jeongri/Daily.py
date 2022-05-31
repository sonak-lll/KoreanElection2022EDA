!curl -s https://raw.githubusercontent.com/teddylee777/machine-learning/master/99-Misc/01-Colab/mecab-colab.sh | bash

# tokenizing
# stopwords list
# 한국불용어100.txt와 불용어 추가 단어는 1차 분석에 있어요
stop_words = pd.read_csv('/data/한국어불용',
                         sep = "\t", engine='python', header = None)
stop_words = list(stop_words[0])

mecab = Mecab()

def preprocessing_mecab(sentence):
    #### Tokenize
    morphs = mecab.pos(str(sentence))

    JOSA = ["JKS", "JKC", "JKG", "JKO", "JKB", "JKV", "JKQ", "JX", "JC"] # 조사
    SIGN = ["SF", "SE", "SSO", "SSC", "SC", "SY"] # 문장 부호
    TERMINATION = ["EP", "EF", "EC", "ETN", "ETM"] # 어미
    SUPPORT_VERB = ["VX"] # 보조 용언
    NUMBER = ["SN"]

    # Remove JOSA, EOMI, etc
    morphs[:] = (morph for morph in morphs if morph[1] not in JOSA+SIGN+TERMINATION+SUPPORT_VERB)

    # Remove length-1 words
    morphs[:] = (morph for morph in morphs if not (len(morph[0]) == 1))

    # Remove Numbers
    morphs[:] = (morph for morph in morphs if morph[1] not in NUMBER)

    # Result pop-up
    result = []
    for morph in morphs:
        result.append(morph[0])

    return result

def common_words(words, k):
    c = Counter(words)
    cw = c.most_common(k)
    return c, cw

def add_value_labels(ax, spacing=5):
    for idx, rect in enumerate(ax.patches):
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2
        space = spacing
        va = 'bottom'
        if y_value < 0:
            space *= -1
            va = 'top'

        label = "{0}".format(df['word'][idx])

        ax.annotate(
            label,                      # Use `label` as label
            (x_value, y_value),         # Place label at end of the bar
            xytext=(0, space),          # Vertically shift label by `space`
            textcoords="offset points", # Interpret `xytext` as offset in points
            ha='center',                # Horizontally center label
            va=va)

# 날짜별 가장 많이 언급된 단어와 단어의 갯수를 dict형태로 가져와서 dataframe으로 만들어주는 과정
date = []
word_list = []
count_list = []

for i in df['date_re'].unique():
    tokenizing = sum(df[df['date_re'] == i]['tokenized'],[])
    # 첫 번째 단어는 제거 (안철수, 박지현)
    c, cw = common_words(tokenizing, 2)
    word = cw[1][0]
    count = cw[1][1]
    date.append(i)
    word_list.append(word)
    count_list.append(count)

dateworddict = {'date' : date, 'word' : word_list, 'count' : count_list}
df = pd.DataFrame(dateworddict, columns=['date', 'word', 'count'])

# graph
fig, ax = plt.subplots(1, figsize=(20,10))
plot = sns.barplot(data = df, x = 'date', y = 'count')
add_value_labels(ax)
plot.set_xticklabels(plot.get_xticklabels(), rotation=45, horizontalalignment='right')
plt.title('most common word by date', fontsize=20)
plt.legend(fontsize=15)
save_fig("most common word by date")
