import pickle
import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time

st.set_page_config(
    page_title="🎬 CineMatch - Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 3rem;
    }
    
    .movie-card {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
    }
    
    .movie-title {
        font-weight: bold;
        font-size: 1.1rem;
        margin: 1rem 0;
        color: #333;
    }
    
    .stats-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 1rem;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    
    .recommendation-container {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
    }
    
    .search-container {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load movie data and similarity matrix"""
    try:
        movies = pickle.load(open('movies.pkl','rb'))
        similarity = pickle.load(open('similarity.pkl','rb'))
        return movies, similarity
    except FileNotFoundError:
        st.error("❌ Data files not found! Please make sure 'movies.pkl' and 'similarity.pkl' are in the same directory.")
        st.stop()

@st.cache_data
def fetch_poster(movie_id):
    """Fetch movie poster from TMDB API"""
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        if 'poster_path' in data and data['poster_path']:
            poster_path = data['poster_path']
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            return "https://via.placeholder.com/500x750/cccccc/666666?text=No+Image"
    except:
        return "https://via.placeholder.com/500x750/cccccc/666666?text=No+Image"

@st.cache_data
def fetch_movie_details(movie_id):
    """Fetch additional movie details from TMDB API"""
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        return {
            'overview': data.get('overview', 'No overview available'),
            'release_date': data.get('release_date', 'Unknown'),
            'vote_average': data.get('vote_average', 0),
            'runtime': data.get('runtime', 0),
            'genres': [genre['name'] for genre in data.get('genres', [])]
        }
    except:
        return {
            'overview': 'Details not available',
            'release_date': 'Unknown',
            'vote_average': 0,
            'runtime': 0,
            'genres': []
        }

def recommend(movie, movies, similarity):
    """Get movie recommendations"""
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        
        recommended_movies = []
        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]].id
            movie_title = movies.iloc[i[0]].title
            similarity_score = distances[i[0]][1]
            
            recommended_movies.append({
                'id': movie_id,
                'title': movie_title,
                'similarity': similarity_score,
                'poster': fetch_poster(movie_id),
                'details': fetch_movie_details(movie_id)
            })
        
        return recommended_movies
    except IndexError:
        st.error("Movie not found in database!")
        return []

def main():
    st.markdown('<h1 class="main-header">🎬 CineMatch</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Discover your next favorite movie with AI-powered recommendations</p>', unsafe_allow_html=True)
    
    with st.spinner("Loading movie database..."):
        movies, similarity = load_data()
    
    with st.sidebar:
        st.header("📊 Database Stats")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Movies", len(movies))
        with col2:
            st.metric("Recommendations", "AI-Powered")
        
        st.markdown("---")
        
        st.header("🎯 How it works")
        st.write("1. Select a movie you enjoyed")
        st.write("2. Our AI analyzes movie features")
        st.write("3. Get personalized recommendations")
        st.write("4. Discover new movies to watch!")
        
        st.markdown("---")
        
        st.header("🔍 Search Tips")
        st.write("• Type the exact movie title")
        st.write("• Use the dropdown for suggestions")
        st.write("• Popular movies work best")
        
        st.markdown("---")
        st.caption("Made with ❤️ using Streamlit")
    
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("🔍 Select a Movie")
        movie_list = movies['title'].values
        selected_movie = st.selectbox(
            "Type or select a movie from the dropdown",
            movie_list,
            help="Start typing to search for movies"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        recommend_button = st.button('✨ Get Recommendations', use_container_width=True, type="primary")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if selected_movie:
        selected_movie_id = movies[movies['title'] == selected_movie]['id'].iloc[0]
        selected_movie_details = fetch_movie_details(selected_movie_id)
        
        with st.expander(f"📽️ About '{selected_movie}'", expanded=False):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                poster_url = fetch_poster(selected_movie_id)
                st.image(poster_url, width=200)
            
            with col2:
                st.write(f"**Release Date:** {selected_movie_details['release_date']}")
                st.write(f"**Rating:** ⭐ {selected_movie_details['vote_average']}/10")
                if selected_movie_details['runtime'] > 0:
                    st.write(f"**Runtime:** {selected_movie_details['runtime']} minutes")
                if selected_movie_details['genres']:
                    st.write(f"**Genres:** {', '.join(selected_movie_details['genres'])}")
                st.write(f"**Overview:** {selected_movie_details['overview'][:200]}...")
    
    if recommend_button and selected_movie:
        st.markdown('<div class="recommendation-container">', unsafe_allow_html=True)
        st.subheader(f"🎬 Movies Similar to '{selected_movie}'")
        
        with st.spinner("Finding perfect matches for you..."):
            time.sleep(1) 
            recommended_movies = recommend(selected_movie, movies, similarity)
        
        if recommended_movies:
            cols = st.columns(5)
            
            for idx, movie in enumerate(recommended_movies):
                with cols[idx]:
                    st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                    
                    st.image(movie['poster'], use_column_width=True)
                    
                    st.markdown(f'<div class="movie-title">{movie["title"]}</div>', unsafe_allow_html=True)
                    
                    similarity_percentage = round(movie['similarity'] * 100, 1)
                    st.progress(movie['similarity'])
                    st.caption(f"Match: {similarity_percentage}%")
                    
                    if movie['details']['vote_average'] > 0:
                        st.caption(f"⭐ {movie['details']['vote_average']}/10")
                    
                    if st.button(f"Details", key=f"details_{idx}", use_container_width=True):
                        st.session_state[f'show_details_{idx}'] = not st.session_state.get(f'show_details_{idx}', False)
                    
                    if st.session_state.get(f'show_details_{idx}', False):
                        st.write(f"**Release:** {movie['details']['release_date']}")
                        if movie['details']['genres']:
                            st.write(f"**Genres:** {', '.join(movie['details']['genres'][:2])}")
                        st.write(f"**Overview:** {movie['details']['overview'][:100]}...")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🔄 Get Different Recommendations", use_container_width=True):
                    st.cache_data.clear()
                    st.experimental_rerun()
            
            with col2:
                if st.button("⭐ Rate These Recommendations", use_container_width=True):
                    st.balloons()
                    st.success("Thank you for your feedback!")
            
            with col3:
                if st.button("📱 Share Recommendations", use_container_width=True):
                    movie_titles = [movie['title'] for movie in recommended_movies]
                    share_text = f"Check out these movies similar to '{selected_movie}': {', '.join(movie_titles)}"
                    st.code(share_text, language=None)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 2rem;'>
            <p>🎬 CineMatch uses advanced machine learning to analyze movie features and provide personalized recommendations.</p>
            <p>Powered by The Movie Database (TMDB) API | Built with Streamlit</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()