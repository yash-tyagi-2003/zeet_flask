from flask import Flask, request, jsonify
import main
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        movie_title = data['movie_title']

        similar_movies = main.find_similar(movie_title)

        # Fetch movie details from the MovieDB API in the backend
        movie_details = []
        for movie_id in similar_movies:
            response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=cef4366e188e22031754054cd680ec34&language=en-US")
            movie_details.append(response.json())

        return jsonify({'recommendations': movie_details})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)