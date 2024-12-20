import streamlit as st
import pickle
import pandas as pd
import requests
import creds

def fetch_poster(movie_id):

    api_key = creds.API_KEY
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US".format(
        movie_id, api_key))

    data = response.json()
    print(data)
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        # fetch poster from API
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


with open('movies_dict.pkl', 'rb') as file:
    movies_dict = pickle.load(file)

with open('similarity.pkl', 'rb') as file:
    similarity = pickle.load(file)

movies = pd.DataFrame(movies_dict)

st.title('Movie Recommender System')
selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for i in range(5):
        if i < len(names):
            with cols[i]:
                st.text(names[i])
                st.image(posters[i])