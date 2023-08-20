import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity

movies=pd.read_csv("tmdb_5000_movies.csv")
credits=pd.read_csv("tmdb_5000_credits.csv")

movies=movies.merge(credits,on='title')

movies=movies[['id','title','overview','genres','keywords','cast','crew']]

movies.dropna(inplace=True)

def conv1(obj):
    fin=[]
    for i in ast.literal_eval(obj):
        fin.append(i['name'])
    return fin

movies['genres']=movies['genres'].apply(conv1)
movies['keywords']=movies['keywords'].apply(conv1)
movies['cast']=movies['cast'].apply(conv1)

def conv2(obj):
    fin=[]
    c=0
    for i in obj:
        if c!=3:
            fin.append(i)
            c+=1
        else:
            break
    return fin

movies['cast']=movies['cast'].apply(conv2)

def find_dir(obj):
    for i in ast.literal_eval(obj):
        if i['job']=="Director":
            return [i['name']]
    return ''

movies['crew']=movies['crew'].apply(find_dir)
movies['overview']=movies['overview'].apply(lambda x:x.split())
movies['genres']=movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast']=movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew']=movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords']=movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])

movies['tags']=movies['cast']+movies['crew']+movies['keywords']+movies['overview']+movies['genres']
df=movies[['id','title','tags']]
df['tags']=df['tags'].apply(lambda x:[i.lower() for i in x])
df['tags']=df['tags'].apply(lambda x:' '.join(x))

cv=CountVectorizer(max_features=5000,stop_words="english")

vectors=cv.fit_transform(df['tags']).toarray()
ps=PorterStemmer()

def stem(text):
    l=[]
    for i in text.split():
        l.append(ps.stem(i))
    return ' '.join(l)

df['tags']=df['tags'].apply(stem)
sml=cosine_similarity(vectors)
sorted(list(enumerate(sml[0])),reverse=True,key=lambda x:x[1])[1:6]


def find_similar(movie):
    ind = df[df['title'] == movie].index[0]
    deviations = sml[ind]
    movies = sorted(list(enumerate(deviations)), reverse=True, key=lambda x: x[1])[1:7]
    sim=[]

    for i in movies:
        sim.append(str(df['id'][i[0]]))
    return sim