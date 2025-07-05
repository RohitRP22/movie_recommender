import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=YOUR_API_KEY&language=en-US"
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Will raise HTTPError for bad status

        data = response.json()
        poster_path = data.get('poster_path')

        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"

    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/500x750?text=Error"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System')
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])



# # app.py
# import pickle
# import requests
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel

# # Load your pickled data
# movies = pickle.load(open('movie_list.pkl', 'rb'))
# similarity = pickle.load(open('similarity.pkl', 'rb'))

# # Create the FastAPI app
# app = FastAPI(
#     title="Movie Recommender API",
#     description="A simple Movie Recommender System using FastAPI",
#     version="1.0.0"
# )

# # Input model
# class MovieRequest(BaseModel):
#     title: str

# # Helper function to fetch poster
# def fetch_poster(movie_id):
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=0de236871092eab9ac0738cb0747fc79&language=en-US"
#     response = requests.get(url)
#     if response.status_code != 200:
#         return None
#     data = response.json()
#     poster_path = data.get('poster_path')
#     if not poster_path:
#         return None
#     full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
#     return full_path

# # Recommender logic
# def recommend(movie):
#     if movie not in movies['title'].values:
#         raise HTTPException(status_code=404, detail="Movie not found in dataset.")
#     index = movies[movies['title'] == movie].index[0]
#     distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
#     recommended_movie_names = []
#     recommended_movie_posters = []

#     for i in distances[1:6]:
#         movie_id = movies.iloc[i[0]].movie_id
#         poster = fetch_poster(movie_id)
#         recommended_movie_names.append(movies.iloc[i[0]].title)
#         recommended_movie_posters.append(poster)

#     return recommended_movie_names, recommended_movie_posters

# # Root endpoint
# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the Movie Recommender API!"}

# # Recommendation endpoint
# @app.post("/recommend")
# def get_recommendations(request: MovieRequest):
#     recommended_movie_names, recommended_movie_posters = recommend(request.title)
#     results = []
#     for name, poster in zip(recommended_movie_names, recommended_movie_posters):
#         results.append({
#             "title": name,
#             "poster_url": poster
#         })
#     return {"recommendations": results}


