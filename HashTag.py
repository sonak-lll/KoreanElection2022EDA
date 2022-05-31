def hashtag(df):
    df.Text.replace('#', ' #', regex=True, inplace=True)
    df.Text.replace(',', ' ', regex=True, inplace=True)

    Texts = df[df['Text'].str.contains('#') == True]
    Texts['Text'] = Texts['Text'].str.split()

    word_of_Bag = sum(Texts['Text'], [])
    word_of_Bag = [word for word in word_of_Bag if word.startswith('#') != False]
    word_of_Bag = [word for word in word_of_Bag if not (len(word) ==0)]

    set_wob = set(word_of_Bag)
    list_wob = list(set_wob)
    key = list_wob
    value = [word_of_Bag.count(i) for i in list_wob]
    data = pd.DataFrame({'key':key, 'value':value})
    data = data[data['value'] > 1]
    data = data.sort_values(by = 'value')

    plt.figure(figsize=(20, 10))
    plot = sns.barplot(data['key'], data['value'])
    plot.set_xticklabels(plot.get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.title('most common hashtag', fontsize = 20)
    plt.legend(fontsize = 15)
