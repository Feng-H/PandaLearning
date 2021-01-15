# 导入相关的库
import numpy as np
import pandas as pd
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt

pd.set_option('display.max_columns',1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth',1000)

df_credits=pd.read_csv("tmdb_5000_credits.csv")
df_credits["cast"] = df_credits["cast"].apply(json.loads)
df_credits["crew"] = df_credits["crew"].apply(json.loads)
# print(len(df_credits["cast"]))

#定义抽取函数，从df中提取演员名字和导演名字
def extract_from_name(feature):
# 确保不是空置，len
    if len(feature) == 0:
        return np.nan
    # 返回导演名字
    if 'job' in feature[0].keys():
# 遍历所有的行的数据
        for i in range(len(feature)):
# 特定的键值对
            if feature[i]['job'] == 'Director':
                return feature[i]['name']
# 这里reture针对的是有Director，如果有的话，就返回跳出。如果没有Director就继续
    res = []
    for i in range(len(feature)):
        res.append(feature[i]['name'])
    return '|'.join(res)

extract_columns = ['cast', 'crew']
df_credits[extract_columns] = df_credits[extract_columns].applymap(extract_from_name)
df_credits.rename(columns={'cast': 'actors', 'crew': 'director'}, inplace=True)
# print(df_credits.head())


df_movies=pd.read_csv("tmdb_5000_movies.csv")
extract_columns_2 = ['genres']
df_movies["genres"] = df_movies["genres"].apply(json.loads)
df_movies[extract_columns_2] = df_movies[extract_columns_2].applymap(extract_from_name)
df_movies.rename(columns={'genres': 'type'}, inplace=True)
df_movies=df_movies[['budget','type','id','release_date','vote_average','vote_count']]
# print(df_movies.head())


# credits 和 movies数据合并 以ID为目标
data = pd.merge(df_credits, df_movies, left_on='movie_id', right_on='id')
# print(data.head())




# 'float' object has no attribute 'split' --> such errors mostly caused by NaN representing empty cells
data.fillna("empty|Empty",inplace=True)


# 将人的名字合并在一个text中
# def actors_movies(df):
#     my_df = df.copy()
#
#     actor_movies = {}
#     actors_array = data['actors'].apply(lambda x: x.split('|')).values
#     for actors in actors_array:
#         for actor in actors:
#             actor_movies.setdefault(actor, 0)
#             actor_movies[actor] += 1
#
#     return actor_movies
# actor_movies = actors_movies(data)
# text = dict(sorted(actor_movies.items(), key=lambda x: x[1], reverse=True)[: 50])

actors_array = data['actors'].apply(lambda x: x.split('|')).values

def gettext(feature):
# 确保不是空置，len
    if len(feature) == 0:
        return np.nan
    text=[]
    for i in range(len(feature)):
        text.append(str(feature[i]))
    return text

text=gettext(actors_array)
text=str(text)


wordcloud = WordCloud().generate(text)

# Display the generated image:
# the matplotlib way:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

# lower max_font_size
wordcloud = WordCloud(max_font_size=40).generate(text)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
